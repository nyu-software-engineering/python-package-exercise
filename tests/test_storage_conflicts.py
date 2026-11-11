from contextlib import closing
import sqlite3

import pytest

from quest_manager import create_quest
from storage import (
    initialize_database, insert_quest, load_progress, load_quests, update_pending_quest,
)


@pytest.fixture
def database(tmp_path):
    path = tmp_path / "quests.db"
    initialize_database(path)
    quest = create_quest([], "Study math", 60)[0]
    quest["id"] = "q1"
    insert_quest(path, quest)
    with closing(sqlite3.connect(path)) as connection:
        connection.execute("UPDATE progress SET totalXP = 90 WHERE id = 1")
        connection.commit()
    return path


def test_matching_snapshot_can_be_saved(database):
    before = load_quests(database)[0]
    updated = {**before, "durationMinutes": 45, "xpReward": 45}

    update_pending_quest(database, updated, expected_quest=before)

    assert load_quests(database) == [updated]
    assert load_progress(database) == {"totalXP": 90}


def test_stale_snapshot_does_not_overwrite_a_newer_edit(database):
    before = load_quests(database)[0]
    newer = {**before, "title": "Read history"}
    update_pending_quest(database, newer)
    stale_update = {**before, "durationMinutes": 45, "xpReward": 45}

    with pytest.raises(ValueError):
        update_pending_quest(database, stale_update, expected_quest=before)

    assert load_quests(database) == [newer]
    assert load_progress(database) == {"totalXP": 90}


def test_snapshot_must_match_the_edited_id(database):
    before = load_quests(database)[0]
    other_id = {**before, "id": "q2"}

    with pytest.raises(ValueError):
        update_pending_quest(database, before, expected_quest=other_id)

    assert load_quests(database) == [before]


@pytest.mark.parametrize("snapshot, error", [("quest", TypeError), ([], TypeError), ({}, ValueError)])
def test_invalid_snapshot_is_rejected(database, snapshot, error):
    before = load_quests(database)[0]

    with pytest.raises(error):
        update_pending_quest(database, before, expected_quest=snapshot)

    assert load_quests(database) == [before]
