from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
import sqlite3
from threading import Barrier

import pytest

from quest_manager import change_quest_duration, create_quest
import storage


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "quests.db"
    storage.initialize_database(path)

    for quest_id, title, minutes in [
        ("q1", "Study math", 60),
        ("q2", "Water plants", 20),
    ]:
        quest = create_quest([], title, minutes)[0]
        quest["id"] = quest_id
        storage.insert_quest(path, quest)

    with closing(sqlite3.connect(path)) as connection:
        # A reader can block COMMIT in this journal mode.
        mode = connection.execute("PRAGMA journal_mode = DELETE").fetchone()
        assert mode == ("delete",)
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()

    return path


@pytest.fixture
def no_lock_wait(monkeypatch):
    original_connect = storage._connect_existing

    def connect_without_wait(path, *, readonly=False):
        connection = original_connect(path, readonly=readonly)
        # Keep the real database connection, but fail immediately on a lock.
        connection.execute("PRAGMA busy_timeout = 0")
        return connection

    monkeypatch.setattr(storage, "_connect_existing", connect_without_wait)


def run_together(first, second):
    start = Barrier(2)

    def run(operation):
        start.wait(timeout=10)
        try:
            return operation(), None
        except (KeyError, ValueError) as error:
            return None, error

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [
            pool.submit(run, first),
            pool.submit(run, second),
        ]
        return [future.result(timeout=15) for future in futures]


@pytest.mark.parametrize(
    "minutes, edited_total, edited_level",
    [
        (10, 100, 2),
        (45, 135, 2),
        (250, 340, 4),
    ],
)
def test_duration_edit_racing_completion_keeps_reward_consistent(
    database, minutes, edited_total, edited_level
):
    before = storage.load_quests(database)
    updated = change_quest_duration(before, "q1", minutes)[0]

    def edit():
        storage.update_pending_quest(
            database,
            updated,
            expected_quest=before[0],
        )

    def complete():
        return storage.complete_quest(database, "q1")

    (_, edit_error), (result, completion_error) = run_together(edit, complete)

    assert completion_error is None

    if edit_error is None:
        expected_minutes = minutes
        expected_total = edited_total
        expected_level = edited_level
    else:
        assert isinstance(edit_error, ValueError)
        expected_minutes = 60
        expected_total = 150
        expected_level = 2

    timestamp = result["quest"]["completedAt"]
    assert timestamp
    expected_quest = {
        **before[0],
        "durationMinutes": expected_minutes,
        "xpReward": expected_minutes,
        "status": "completed",
        "completedAt": timestamp,
    }

    assert result == {
        "quest": expected_quest,
        "totalXP": expected_total,
        "level": expected_level,
        "awardedXP": expected_minutes,
    }
    assert storage.load_quests(database) == [expected_quest, before[1]]
    assert storage.load_progress(database) == {"totalXP": expected_total}

    retry = storage.complete_quest(database, "q1")

    assert retry == {**result, "awardedXP": 0}
    assert storage.load_quests(database) == [expected_quest, before[1]]
    assert storage.load_progress(database) == {"totalXP": expected_total}


def test_delete_racing_completion_cannot_leave_an_orphan_reward(database):
    before = storage.load_quests(database)

    def delete():
        storage.delete_pending_quest(database, "q1")

    def complete():
        return storage.complete_quest(database, "q1")

    (_, delete_error), (result, completion_error) = run_together(
        delete, complete
    )

    if delete_error is None:
        assert isinstance(completion_error, KeyError)
        assert result is None
        assert storage.load_quests(database) == [before[1]]
        assert storage.load_progress(database) == {"totalXP": 90}

        with pytest.raises(KeyError):
            storage.complete_quest(database, "q1")

        assert storage.load_quests(database) == [before[1]]
        assert storage.load_progress(database) == {"totalXP": 90}
    else:
        assert isinstance(delete_error, ValueError)
        assert completion_error is None

        timestamp = result["quest"]["completedAt"]
        assert timestamp
        expected_quest = {
            **before[0],
            "status": "completed",
            "completedAt": timestamp,
        }

        assert result == {
            "quest": expected_quest,
            "totalXP": 150,
            "level": 2,
            "awardedXP": 60,
        }
        assert storage.load_quests(database) == [expected_quest, before[1]]
        assert storage.load_progress(database) == {"totalXP": 150}

        retry = storage.complete_quest(database, "q1")

        assert retry == {**result, "awardedXP": 0}
        assert storage.load_quests(database) == [expected_quest, before[1]]
        assert storage.load_progress(database) == {"totalXP": 150}


def test_busy_writer_leaves_quest_pending_and_allows_retry(
    database, no_lock_wait
):
    before = storage.load_quests(database)

    with closing(sqlite3.connect(database)) as writer:
        writer.execute("BEGIN IMMEDIATE")

        with pytest.raises(sqlite3.OperationalError) as error:
            storage.complete_quest(database, "q1")

        assert error.value.sqlite_errorcode == sqlite3.SQLITE_BUSY
        assert storage.load_quests(database) == before
        assert storage.load_progress(database) == {"totalXP": 90}

    first = storage.complete_quest(database, "q1")

    assert first["awardedXP"] == 60
    assert first["totalXP"] == 150
    assert first["level"] == 2
    assert first["quest"]["status"] == "completed"
    assert first["quest"]["completedAt"]

    retry = storage.complete_quest(database, "q1")

    assert retry == {**first, "awardedXP": 0}
    assert storage.load_quests(database) == [first["quest"], before[1]]
    assert storage.load_progress(database) == {"totalXP": 150}


def test_blocked_commit_rolls_back_both_updates_and_allows_retry(
    database, no_lock_wait
):
    before = storage.load_quests(database)

    with closing(sqlite3.connect(database)) as reader:
        reader.execute("BEGIN")
        snapshot = reader.execute(
            "SELECT totalXP FROM progress WHERE id = 1"
        ).fetchone()
        assert snapshot == (90,)

        # The read transaction allows updates but prevents their final commit.
        with pytest.raises(sqlite3.OperationalError) as error:
            storage.complete_quest(database, "q1")

        assert error.value.sqlite_errorcode == sqlite3.SQLITE_BUSY
        assert storage.load_quests(database) == before
        assert storage.load_progress(database) == {"totalXP": 90}

    assert storage.load_quests(database) == before
    assert storage.load_progress(database) == {"totalXP": 90}

    first = storage.complete_quest(database, "q1")

    assert first["awardedXP"] == 60
    assert first["totalXP"] == 150
    assert first["level"] == 2
    assert first["quest"]["status"] == "completed"
    assert first["quest"]["completedAt"]

    retry = storage.complete_quest(database, "q1")

    assert retry == {**first, "awardedXP": 0}
    assert storage.load_quests(database) == [first["quest"], before[1]]
    assert storage.load_progress(database) == {"totalXP": 150}