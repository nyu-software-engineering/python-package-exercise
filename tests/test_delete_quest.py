from copy import deepcopy

import pytest

import quest_manager


@pytest.fixture
def quests():
    return [
        {
            "id": "q1",
            "title": "Study math",
            "durationMinutes": 60,
            "fantasyDescription": "Decipher an Ancient Scroll",
            "status": "pending",
            "xpReward": 60,
            "completedAt": None,
        },
        {
            "id": "q2",
            "title": "Do the laundry",
            "durationMinutes": 20,
            "fantasyDescription": "Restore Order to the Kingdom",
            "status": "completed",
            "xpReward": 20,
            "completedAt": "2026-11-09T15:00:00Z",
        },
        {
            "id": "q3",
            "title": "Go swimming",
            "durationMinutes": 30,
            "fantasyDescription": "Train for the Royal Tournament",
            "status": "pending",
            "xpReward": 30,
            "completedAt": None,
        },
    ]


@pytest.mark.parametrize(
    "quest_id, remaining_ids",
    [("q1", ["q2", "q3"]), ("q3", ["q1", "q2"])],
)
def test_delete_pending_quest(quests, quest_id, remaining_ids):
    before = deepcopy(quests)
    result = quest_manager.delete_quest(quests, quest_id)

    assert [quest["id"] for quest in result] == remaining_ids
    assert result == [quest for quest in before if quest["id"] != quest_id]
    assert quests == before


def test_delete_last_quest(quests):
    original = [quests[0]]

    assert quest_manager.delete_quest(original, "q1") == []
    assert len(original) == 1


def test_completed_quest_cannot_be_deleted(quests):
    before = deepcopy(quests)

    with pytest.raises(ValueError):
        quest_manager.delete_quest(quests, "q2")

    assert quests == before


@pytest.mark.parametrize("status", [None, "done", "Pending", "", False, []])
def test_unknown_status_cannot_be_deleted(quests, status):
    quests[0]["status"] = status
    before = deepcopy(quests)

    with pytest.raises(ValueError):
        quest_manager.delete_quest(quests, "q1")

    assert quests == before


def test_missing_status_cannot_be_deleted(quests):
    del quests[0]["status"]
    before = deepcopy(quests)

    with pytest.raises(ValueError):
        quest_manager.delete_quest(quests, "q1")

    assert quests == before


@pytest.mark.parametrize("status", ["pending", "completed"])
def test_duplicate_id_is_rejected(quests, status):
    quests.append(dict(quests[0], status=status))
    before = deepcopy(quests)

    with pytest.raises(ValueError):
        quest_manager.delete_quest(quests, "q1")

    assert quests == before


def test_only_deletes_exact_id(quests):
    quests.insert(0, dict(quests[0], id="q10"))

    result = quest_manager.delete_quest(quests, "q1")

    assert [quest["id"] for quest in result] == ["q10", "q2", "q3"]


def test_integer_and_string_ids_are_different(quests):
    quests[0]["id"] = 1
    quests[2]["id"] = "1"

    assert [quest["id"] for quest in quest_manager.delete_quest(quests, 1)] == [
        "q2", "1"
    ]
    assert [quest["id"] for quest in quest_manager.delete_quest(quests, "1")] == [
        1, "q2"
    ]


def test_result_changes_do_not_change_remaining_quests(quests):
    before = deepcopy(quests)
    result = quest_manager.delete_quest(quests, "q1")
    result[0]["title"] = "Changed title"
    result[1]["durationMinutes"] = 999
    result.clear()

    assert quests == before


@pytest.mark.parametrize("quest_id", ["missing", " q1 "])
def test_unknown_id(quests, quest_id):
    before = deepcopy(quests)

    with pytest.raises(KeyError):
        quest_manager.delete_quest(quests, quest_id)

    assert quests == before


def test_repeated_deletion(quests):
    result = quest_manager.delete_quest(quests, "q1")
    before = deepcopy(result)

    with pytest.raises(KeyError):
        quest_manager.delete_quest(result, "q1")

    assert result == before


def test_empty_list():
    with pytest.raises(KeyError):
        quest_manager.delete_quest([], "q1")


@pytest.mark.parametrize("quests", [None, "quests", {}, ()])
def test_invalid_quest_collection(quests):
    with pytest.raises(TypeError):
        quest_manager.delete_quest(quests, "q1")


@pytest.mark.parametrize("quest", [None, "Study math", 60, []])
def test_invalid_quest_entry(quests, quest):
    quests.append(quest)

    with pytest.raises(TypeError):
        quest_manager.delete_quest(quests, "q1")


@pytest.mark.parametrize("quest_id", [None, True, False, 1.5, [], {}])
def test_invalid_id_type(quests, quest_id):
    with pytest.raises(TypeError):
        quest_manager.delete_quest(quests, quest_id)


@pytest.mark.parametrize("quest_id", ["", " ", "\t\n"])
def test_blank_id(quests, quest_id):
    with pytest.raises(ValueError):
        quest_manager.delete_quest(quests, quest_id)
