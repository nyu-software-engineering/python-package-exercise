from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timedelta
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from threading import Barrier

import pytest

from quest_manager import change_quest_duration, create_quest
import storage


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "quests.db"
    storage.initialize_database(path)
    for quest_id, title, minutes in [("q1", "Study math", 60), ("q2", "Do laundry", 50)]:
        quest = create_quest([], title, minutes)[0]
        quest["id"] = quest_id
        storage.insert_quest(path, quest)
    with closing(sqlite3.connect(path)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()
    return path


def test_complete_saves_quest_and_progress(database):
    before = storage.load_quests(database)
    result = storage.complete_quest(database, "q1")
    completed_at = result["quest"]["completedAt"]
    expected = {**before[0], "status": "completed", "completedAt": completed_at}

    assert datetime.fromisoformat(completed_at).utcoffset() == timedelta(0)
    assert result == {"quest": expected, "totalXP": 150, "level": 2, "awardedXP": 60}
    assert storage.load_quests(database) == [expected, before[1]]
    assert storage.load_progress(database) == {"totalXP": 150}


def test_retry_preserves_timestamp_and_does_not_award_again(database):
    first = storage.complete_quest(database, "q1")
    retry = storage.complete_quest(database, "q1")

    assert retry == {**first, "awardedXP": 0}
    assert storage.load_progress(database) == {"totalXP": 150}


def test_retry_from_a_new_process(database):
    first = storage.complete_quest(database, "q1")
    code = (
        "import json, sys; sys.path.insert(0, sys.argv[1]); "
        "from storage import complete_quest; "
        "print(json.dumps(complete_quest(sys.argv[2], sys.argv[3])))"
    )
    process = subprocess.run(
        [sys.executable, "-I", "-c", code,
         str(Path(storage.__file__).parent), str(database), "q1"],
        capture_output=True, text=True, check=True, timeout=10,
    )

    assert json.loads(process.stdout) == {**first, "awardedXP": 0}
    assert storage.load_progress(database) == {"totalXP": 150}


@pytest.mark.parametrize("duration, total, level", [(1, 91, 1), (10, 100, 2), (250, 340, 4)])
def test_completion_uses_latest_saved_duration(database, duration, total, level):
    changed = change_quest_duration(storage.load_quests(database), "q1", duration)[0]
    storage.update_pending_quest(database, changed)

    result = storage.complete_quest(database, "q1")

    assert result["awardedXP"] == duration
    assert result["totalXP"] == total
    assert result["level"] == level
    assert result["quest"]["xpReward"] == duration
    assert storage.load_progress(database) == {"totalXP": total}


def test_separate_quests_and_retry_return_current_progress(database):
    first = storage.complete_quest(database, "q1")
    second = storage.complete_quest(database, "q2")
    retry = storage.complete_quest(database, "q1")

    assert second["awardedXP"] == 50
    assert second["totalXP"] == 200
    assert second["level"] == 3
    assert retry["quest"] == first["quest"]
    assert retry["awardedXP"] == 0
    assert retry["totalXP"] == 200
    assert retry["level"] == 3


def test_concurrent_completion_awards_once(database):
    start = Barrier(4)

    def finish():
        start.wait(timeout=5)
        return storage.complete_quest(database, "q1")

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(finish) for _ in range(4)]
        results = [future.result(timeout=10) for future in futures]

    assert sorted(result["awardedXP"] for result in results) == [0, 0, 0, 60]
    assert {result["totalXP"] for result in results} == {150}
    assert len({result["quest"]["completedAt"] for result in results}) == 1
    assert storage.load_progress(database) == {"totalXP": 150}


def test_concurrent_different_quests_keep_both_rewards(database):
    start = Barrier(2)

    def finish(quest_id):
        start.wait(timeout=5)
        return storage.complete_quest(database, quest_id)

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(finish, quest_id) for quest_id in ["q1", "q2"]]
        results = [future.result(timeout=10) for future in futures]

    assert sorted(result["awardedXP"] for result in results) == [50, 60]
    assert max(result["totalXP"] for result in results) == 200
    assert storage.load_progress(database) == {"totalXP": 200}
    assert [quest["status"] for quest in storage.load_quests(database)] == ["completed", "completed"]


@pytest.mark.parametrize("table", ["quests", "progress"])
def test_failed_save_rolls_back_and_retry_works(database, table):
    before = storage.load_quests(database)
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            f"CREATE TRIGGER fail_completion AFTER UPDATE ON {table} "
            "BEGIN SELECT RAISE(ABORT, 'forced save failure'); END"
        )
        connection.commit()

    with pytest.raises(sqlite3.IntegrityError):
        storage.complete_quest(database, "q1")

    assert storage.load_quests(database) == before
    assert storage.load_progress(database) == {"totalXP": 90}
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("DROP TRIGGER fail_completion")
        connection.commit()

    assert storage.complete_quest(database, "q1")["awardedXP"] == 60
    assert storage.load_progress(database) == {"totalXP": 150}


@pytest.mark.parametrize("table", ["quests", "progress"])
def test_ignored_write_cannot_create_half_completion(database, table):
    before = storage.load_quests(database)
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            f"CREATE TRIGGER ignore_completion BEFORE UPDATE ON {table} "
            "BEGIN SELECT RAISE(IGNORE); END"
        )
        connection.commit()

    with pytest.raises(sqlite3.IntegrityError):
        storage.complete_quest(database, "q1")

    assert storage.load_quests(database) == before
    assert storage.load_progress(database) == {"totalXP": 90}


def test_retry_does_not_write_quest_or_progress(database):
    first = storage.complete_quest(database, "q1")
    with closing(sqlite3.connect(database)) as connection:
        for table in ["quests", "progress"]:
            connection.execute(
                f"CREATE TRIGGER block_{table} BEFORE UPDATE ON {table} "
                "BEGIN SELECT RAISE(ABORT, 'retry must not write'); END"
            )
        connection.commit()

    assert storage.complete_quest(database, "q1") == {**first, "awardedXP": 0}


def test_completed_quest_cannot_be_edited_or_deleted(database):
    pending = storage.load_quests(database)[0]
    result = storage.complete_quest(database, "q1")

    with pytest.raises(ValueError):
        storage.update_pending_quest(database, {**pending, "title": "Changed title"})
    with pytest.raises(ValueError):
        storage.delete_pending_quest(database, "q1")

    assert storage.load_quests(database)[0] == result["quest"]
    assert storage.load_progress(database) == {"totalXP": 150}


@pytest.mark.parametrize("quest_id", ["missing", " q1 ", "q1' OR '1'='1"])
def test_unknown_id_does_not_change_saved_data(database, quest_id):
    before = storage.load_quests(database)

    with pytest.raises(KeyError):
        storage.complete_quest(database, quest_id)

    assert storage.load_quests(database) == before
    assert storage.load_progress(database) == {"totalXP": 90}


@pytest.mark.parametrize("quest_id", [None, 1, True, False, 1.5, [], {}])
def test_invalid_id_type(database, quest_id):
    with pytest.raises(TypeError):
        storage.complete_quest(database, quest_id)


@pytest.mark.parametrize("quest_id", ["", " ", "\t\n"])
def test_blank_id(database, quest_id):
    with pytest.raises(ValueError):
        storage.complete_quest(database, quest_id)


@pytest.mark.parametrize("path, error", [(None, TypeError), (123, TypeError), (b"db", TypeError), ("", ValueError), (":memory:", ValueError), ("file:quests.db", ValueError)])
def test_invalid_database_path(path, error):
    with pytest.raises(error):
        storage.complete_quest(path, "q1")


def test_missing_database_is_not_created(tmp_path):
    path = tmp_path / "missing.db"

    with pytest.raises(sqlite3.OperationalError):
        storage.complete_quest(path, "q1")

    assert not path.exists()


def test_missing_progress_leaves_quest_pending(database):
    before = storage.load_quests(database)
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("DELETE FROM progress")
        connection.commit()

    with pytest.raises(ValueError):
        storage.complete_quest(database, "q1")

    assert storage.load_quests(database) == before


def test_xp_overflow_does_not_complete_quest(database):
    before = storage.load_quests(database)
    maximum = 2**63 - 1
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = ? WHERE id = 1", (maximum,))
        connection.commit()

    with pytest.raises(ValueError):
        storage.complete_quest(database, "q1")

    assert storage.load_quests(database) == before
    assert storage.load_progress(database) == {"totalXP": maximum}


def test_largest_valid_saved_total(database):
    maximum = 2**63 - 1
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = ? WHERE id = 1", (maximum - 60,))
        connection.commit()

    result = storage.complete_quest(database, "q1")

    assert result["totalXP"] == maximum
    assert result["level"] == 92233720368547759
    assert storage.load_progress(database) == {"totalXP": maximum}


def test_returned_data_does_not_change_storage(database):
    result = storage.complete_quest(database, "q1")
    result["quest"]["title"] = "Changed"
    result["totalXP"] = 0

    assert storage.load_quests(database)[0]["title"] == "Study math"
    assert storage.load_progress(database) == {"totalXP": 150}
