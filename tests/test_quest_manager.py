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
            "title": "Clean my room",
            "durationMinutes": 20,
            "fantasyDescription": "Restore the Adventurer's Camp",
            "status": "completed",
            "xpReward": 20,
            "completedAt": "2026-11-09T15:00:00Z",
        },
        {
            "id": "q3",
            "title": "Read a book",
            "durationMinutes": 30,
            "fantasyDescription": "Explore the Ancient Library",
            "status": "pending",
            "xpReward": 30,
            "completedAt": None,
        },
    ]


def test_list_all_quests(quests):
    result = quest_manager.list_quests(quests)

    assert [quest["id"] for quest in result] == ["q1", "q2", "q3"]
    assert result[0] == {
        "id": "q1",
        "title": "Study math",
        "durationMinutes": 60,
        "fantasyDescription": "Decipher an Ancient Scroll",
        "status": "pending",
        "xpReward": 60,
        "completedAt": None,
    }
    assert result[1]["completedAt"] == "2026-11-09T15:00:00Z"


def test_list_pending_quests(quests):
    result = quest_manager.list_quests(quests, "pending")

    assert [quest["id"] for quest in result] == ["q1", "q3"]


def test_list_completed_quests(quests):
    result = quest_manager.list_quests(quests, "completed")

    assert [quest["id"] for quest in result] == ["q2"]


@pytest.mark.parametrize("status", [None, "pending", "completed"])
def test_empty_quest_list(status):
    assert quest_manager.list_quests([], status) == []


def test_no_matching_quests(quests):
    pending_quests = [quests[0], quests[2]]

    assert quest_manager.list_quests(pending_quests, "completed") == []


def test_filter_does_not_change_original_list(quests):
    quest_manager.list_quests(quests, "completed")

    assert [quest["id"] for quest in quests] == ["q1", "q2", "q3"]
    assert quests[0]["status"] == "pending"


@pytest.mark.parametrize("status", [None, "pending", "completed"])
def test_result_does_not_change_original_quests(quests, status):
    result = quest_manager.list_quests(quests, status)
    result[0]["title"] = "Changed title"
    result.clear()

    assert len(quests) == 3
    assert quests[0]["title"] == "Study math"
    assert quests[1]["title"] == "Clean my room"


@pytest.mark.parametrize("quests", [None, "quests", {}, ()])
def test_invalid_quest_collection(quests):
    with pytest.raises(TypeError):
        quest_manager.list_quests(quests)


@pytest.mark.parametrize("quest", [None, "Study math", 60, []])
def test_invalid_quest_entry(quests, quest):
    quests.append(quest)

    with pytest.raises(TypeError):
        quest_manager.list_quests(quests)


@pytest.mark.parametrize("status", ["done", "", "Pending", 1, []])
def test_invalid_status(quests, status):
    with pytest.raises(ValueError):
        quest_manager.list_quests(quests, status)
