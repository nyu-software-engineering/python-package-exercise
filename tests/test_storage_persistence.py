"""Verify quest/progress reads and durable inserts against real SQLite files."""

from contextlib import closing
from copy import deepcopy
import json
import sqlite3
import subprocess
import sys

import pytest

from progression import calculate_level
from quest_manager import create_quest
from storage import initialize_database, insert_quest, load_progress, load_quests


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "quests.db"
    initialize_database(path)
    return path


def new_quest(title="Study math", minutes=60):
    return create_quest([], title, minutes, seed=7)[0]


def test_insert_survives_reopen_and_a_separate_process(database):
    quest = new_quest("  Study math's scroll; --  ")
    quest["id"] = "id'; DROP TABLE quests; --"
    original = deepcopy(quest)
    assert insert_quest(str(database), quest) is None
    assert quest == original
    assert load_quests(database) == [original]
    assert load_progress(database) == {"totalXP": 0}

    # A new Python process verifies committed data independently of our helpers.
    result = subprocess.run([
        sys.executable, "-I", "-c",
        "import json, sqlite3, sys; "
        "c = sqlite3.connect(sys.argv[1]); c.row_factory = sqlite3.Row; "
        "print(json.dumps([dict(r) for r in c.execute('SELECT * FROM quests')])); "
        "c.close()", str(database),
    ], check=True, capture_output=True, text=True)
    assert json.loads(result.stdout) == [original]


def test_loads_empty_lists_and_initial_progress(database):
    assert load_quests(database) == []
    assert load_quests(database, "pending") == []
    assert load_quests(database, "completed") == []
    assert load_progress(str(database)) == {"totalXP": 0}


def test_reads_order_status_and_independent_copies(database):
    first = new_quest("Read history", 10)
    second = new_quest("Clean kitchen", 20)
    insert_quest(database, first)
    insert_quest(database, second)
    # Model a record produced by the future completion transaction.
    with closing(sqlite3.connect(database)) as connection:
        connection.execute(
            "UPDATE quests SET status = 'completed', completedAt = ? WHERE id = ?",
            ("2026-11-10T12:00:00Z", first["id"]),
        )
        connection.commit()
    first.update(status="completed", completedAt="2026-11-10T12:00:00Z")

    assert load_quests(database) == [first, second]
    assert load_quests(database, "completed") == [first]
    assert load_quests(database, "pending") == [second]
    loaded = load_quests(database)
    loaded[0]["title"] = "Only a local edit"
    loaded.clear()
    assert load_quests(database) == [first, second]


def test_duplicate_id_does_not_overwrite_or_award_xp(database):
    quest = new_quest()
    insert_quest(database, quest)
    with pytest.raises(sqlite3.IntegrityError):
        insert_quest(database, quest | {"title": "Replacement"})
    assert load_quests(database) == [quest]
    assert load_progress(database) == {"totalXP": 0}
    # The failed write releases its connection/transaction for the next writer.
    another = new_quest("Do laundry", 30)
    insert_quest(database, another)
    assert load_quests(database) == [quest, another]


def test_failed_database_write_preserves_existing_data(database):
    quest = new_quest()
    insert_quest(database, quest)
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.execute(
            "CREATE TRIGGER fail_insert AFTER INSERT ON quests BEGIN "
            "UPDATE progress SET totalXP = 999 WHERE id = 1; "
            "SELECT RAISE(FAIL, 'simulated disk write failure'); END"
        )
        connection.commit()
    with pytest.raises(sqlite3.IntegrityError, match="simulated disk write failure"):
        insert_quest(database, new_quest("Go swimming"))
    assert load_quests(database) == [quest]
    assert load_progress(database) == {"totalXP": 90}


def test_load_progress_returns_saved_xp_without_mutation(database):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("UPDATE progress SET totalXP = 321 WHERE id = 1")
        connection.commit()
    result = load_progress(database)
    assert result == {"totalXP": 321}
    assert calculate_level(result["totalXP"]) == 4
    result["totalXP"] = 999
    assert load_progress(database) == {"totalXP": 321}
    initialize_database(database)
    assert load_progress(database) == {"totalXP": 321}


def test_missing_progress_row_is_not_silently_recreated(database):
    with closing(sqlite3.connect(database)) as connection:
        connection.execute("DELETE FROM progress")
        connection.commit()
    with pytest.raises(ValueError, match="not initialized"):
        load_progress(database)
    with closing(sqlite3.connect(database)) as connection:
        assert connection.execute("SELECT * FROM progress").fetchall() == []


@pytest.mark.parametrize("changes, error", [
    ({"id": 1}, TypeError),
    ({"id": " "}, ValueError),
    ({"title": None}, TypeError),
    ({"title": " \t\n"}, ValueError),
    ({"fantasyDescription": 1}, TypeError),
    ({"fantasyDescription": ""}, ValueError),
    ({"durationMinutes": True}, TypeError),
    ({"durationMinutes": 1.5}, TypeError),
    ({"durationMinutes": "60"}, TypeError),
    ({"durationMinutes": 0, "xpReward": 0}, ValueError),
    ({"durationMinutes": -1, "xpReward": -1}, ValueError),
    ({"durationMinutes": 2**63, "xpReward": 2**63}, ValueError),
    ({"xpReward": True}, TypeError),
    ({"xpReward": 1.5}, TypeError),
    ({"xpReward": 59}, ValueError),
    ({"status": "completed", "completedAt": "2026-11-10T12:00:00Z"}, ValueError),
    ({"status": "done"}, ValueError),
    ({"completedAt": "2026-11-10T12:00:00Z"}, ValueError),
    ({"customMetadata": "not silently lost"}, ValueError),
])
def test_invalid_insert_keeps_existing_quests_and_xp(database, changes, error):
    original = new_quest()
    insert_quest(database, original)
    invalid = new_quest() | changes
    before = deepcopy(invalid)
    with pytest.raises(error):
        insert_quest(database, invalid)
    assert invalid == before
    assert load_quests(database) == [original]
    assert load_progress(database) == {"totalXP": 0}


@pytest.mark.parametrize("quest, error", [(None, TypeError), ([], TypeError), ({}, ValueError)])
def test_missing_quest_fields_and_wrong_record_type(database, quest, error):
    with pytest.raises(error):
        insert_quest(database, quest)
    assert load_quests(database) == []


@pytest.mark.parametrize("status", ["done", "", 1, True, []])
def test_invalid_filter_is_rejected(database, status):
    with pytest.raises(ValueError, match="status"):
        load_quests(database, status)


@pytest.mark.parametrize("operation", [load_quests, load_progress, insert_quest])
def test_operations_do_not_create_missing_database_files(tmp_path, operation):
    path = tmp_path / "missing.db"
    args = (path, new_quest()) if operation is insert_quest else (path,)
    with pytest.raises(sqlite3.OperationalError):
        operation(*args)
    assert not path.exists()


@pytest.mark.parametrize("operation", [load_quests, load_progress, insert_quest])
@pytest.mark.parametrize("path, error", [(None, TypeError), (":memory:", ValueError)])
def test_operations_share_initializers_path_rules(operation, path, error):
    args = (path, new_quest()) if operation is insert_quest else (path,)
    with pytest.raises(error, match="database_path"):
        operation(*args)


def test_paths_with_unicode_spaces_and_uri_characters(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = "任务 ?#%.db"
    initialize_database(path)
    quest = new_quest("Read math", 2**63 - 1)
    insert_quest(path, quest)
    assert load_quests(path) == [quest]
    assert load_progress(path) == {"totalXP": 0}
