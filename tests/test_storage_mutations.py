from contextlib import closing
from copy import deepcopy
import json
import sqlite3
import subprocess
import sys

import pytest

from quest_manager import change_quest_duration, create_quest, rename_quest
from storage import (
    delete_pending_quest, initialize_database, insert_quest, load_progress,
    load_quests, update_pending_quest,
)


@pytest.fixture
def saved_quests(tmp_path):
    path = tmp_path / "quests.db"
    initialize_database(path)
    quests = create_quest([], "Study math", 60, seed=7)
    quests = create_quest(quests, "Read history", 20, seed=7)
    quests[0]["id"] = "q'1; --"
    for quest in quests:
        insert_quest(path, quest)
    with closing(sqlite3.connect(path)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()
    return path, quests


@pytest.mark.parametrize("title, minutes", [
    ("Do laundry", None), (None, 25), ("Go swimming", 45),
])
def test_edits_persist_with_description_and_reward(saved_quests, title, minutes):
    path, original = saved_quests
    updated = original
    if title is not None:
        updated = rename_quest(updated, original[0]["id"], title, seed=7)
    if minutes is not None:
        updated = change_quest_duration(updated, original[0]["id"], minutes)
    before = deepcopy(updated)

    assert update_pending_quest(str(path), updated[0]) is None
    assert updated == before
    assert load_quests(path) == updated
    assert load_progress(path) == {"totalXP": 90}
    assert original[0]["title"] == "Study math"
    assert original[0]["durationMinutes"] == 60


def test_custom_description_is_saved_without_regeneration(saved_quests):
    path, quests = saved_quests
    updated = rename_quest(
        quests, quests[0]["id"], "Study physics",
        custom_templates={"study": ["Read the royal archive"]},
    )
    update_pending_quest(path, updated[0])
    assert load_quests(path)[0]["fantasyDescription"] == "Read the royal archive"
    assert load_quests(path)[1] == quests[1]
    assert load_progress(path) == {"totalXP": 90}


def test_delete_removes_only_the_requested_quest(saved_quests):
    path, quests = saved_quests
    assert delete_pending_quest(str(path), quests[0]["id"]) is None
    assert load_quests(path) == [quests[1]]
    assert load_progress(path) == {"totalXP": 90}
    initialize_database(path)
    assert load_quests(path) == [quests[1]]
    with pytest.raises(KeyError, match="not found"):
        delete_pending_quest(path, quests[0]["id"])
    assert load_quests(path) == [quests[1]]


def test_changes_survive_a_new_python_process(saved_quests):
    path, quests = saved_quests
    updated = change_quest_duration(quests, quests[0]["id"], 45)
    update_pending_quest(path, updated[0])
    delete_pending_quest(path, quests[1]["id"])
    result = subprocess.run([
        sys.executable, "-I", "-c",
        "import json, sqlite3, sys; "
        "c=sqlite3.connect(sys.argv[1]); c.row_factory=sqlite3.Row; "
        "print(json.dumps({'quests': [dict(r) for r in c.execute('SELECT * FROM quests')], "
        "'totalXP': c.execute('SELECT totalXP FROM progress WHERE id=1').fetchone()[0]})); "
        "c.close()", str(path),
    ], check=True, capture_output=True, text=True)
    assert json.loads(result.stdout) == {"quests": [updated[0]], "totalXP": 90}


@pytest.mark.parametrize("operation", [update_pending_quest, delete_pending_quest])
def test_saved_completed_status_blocks_stale_pending_requests(saved_quests, operation):
    path, stale = saved_quests
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(
            "UPDATE quests SET status='completed', completedAt=? WHERE id=?",
            ("2026-11-10T12:00:00Z", stale[0]["id"]),
        )
        connection.commit()
    saved = load_quests(path)
    argument = stale[0] if operation is update_pending_quest else stale[0]["id"]
    with pytest.raises(ValueError, match="only pending"):
        operation(path, argument)
    assert load_quests(path) == saved
    assert load_progress(path) == {"totalXP": 90}


@pytest.mark.parametrize("operation", [update_pending_quest, delete_pending_quest])
def test_unknown_ids_do_not_insert_or_change_other_quests(saved_quests, operation):
    path, quests = saved_quests
    argument = quests[0] | {"id": "missing"} if operation is update_pending_quest else "missing"
    with pytest.raises(KeyError, match="not found"):
        operation(path, argument)
    assert load_quests(path) == quests
    assert load_progress(path) == {"totalXP": 90}


@pytest.mark.parametrize("changes, error", [
    ({"title": " "}, ValueError),
    ({"fantasyDescription": None}, TypeError),
    ({"durationMinutes": True}, TypeError),
    ({"durationMinutes": 0, "xpReward": 0}, ValueError),
    ({"durationMinutes": 2**63, "xpReward": 2**63}, ValueError),
    ({"xpReward": 59}, ValueError),
    ({"status": "completed", "completedAt": "2026-11-10T12:00:00Z"}, ValueError),
    ({"completedAt": "2026-11-10T12:00:00Z"}, ValueError),
    ({"extra": "not silently lost"}, ValueError),
])
def test_invalid_updates_preserve_saved_data(saved_quests, changes, error):
    path, quests = saved_quests
    invalid = quests[0] | changes
    before = deepcopy(invalid)
    with pytest.raises(error):
        update_pending_quest(path, invalid)
    assert invalid == before
    assert load_quests(path) == quests
    assert load_progress(path) == {"totalXP": 90}


@pytest.mark.parametrize("quest, error", [(None, TypeError), ({}, ValueError)])
def test_invalid_update_record_shape(saved_quests, quest, error):
    path, quests = saved_quests
    with pytest.raises(error):
        update_pending_quest(path, quest)
    assert load_quests(path) == quests


@pytest.mark.parametrize("quest_id, error", [
    (None, TypeError), (True, TypeError), (1, TypeError), ("", ValueError), (" \t", ValueError),
])
def test_invalid_delete_ids_preserve_saved_data(saved_quests, quest_id, error):
    path, quests = saved_quests
    with pytest.raises(error):
        delete_pending_quest(path, quest_id)
    assert load_quests(path) == quests
    assert load_progress(path) == {"totalXP": 90}


@pytest.mark.parametrize("operation, event", [
    (update_pending_quest, "UPDATE"), (delete_pending_quest, "DELETE"),
])
def test_write_failure_rolls_back_task_and_progress(saved_quests, operation, event):
    path, quests = saved_quests
    with closing(sqlite3.connect(path)) as connection:
        connection.execute(
            f"CREATE TRIGGER fail_write AFTER {event} ON quests BEGIN "
            "UPDATE progress SET totalXP=999 WHERE id=1; "
            "SELECT RAISE(FAIL, 'simulated write failure'); END"
        )
        connection.commit()
    argument = quests[0] | {"title": "Changed"} if operation is update_pending_quest else quests[0]["id"]
    with pytest.raises(sqlite3.IntegrityError, match="simulated write failure"):
        operation(path, argument)
    assert load_quests(path) == quests
    assert load_progress(path) == {"totalXP": 90}
    with closing(sqlite3.connect(path)) as connection:
        connection.execute("DROP TRIGGER fail_write")
    operation(path, argument)


@pytest.mark.parametrize("operation", [update_pending_quest, delete_pending_quest])
def test_missing_database_is_not_created(tmp_path, operation):
    path = tmp_path / "missing.db"
    quest = create_quest([], "Study math", 60)[0]
    argument = quest if operation is update_pending_quest else quest["id"]
    with pytest.raises(sqlite3.OperationalError):
        operation(path, argument)
    assert not path.exists()
