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
    ]


def test_get_pending_quest(quests):
    result = quest_manager.get_quest(quests, "q1")

    assert result == {
        "id": "q1",
        "title": "Study math",
        "durationMinutes": 60,
        "fantasyDescription": "Decipher an Ancient Scroll",
        "status": "pending",
        "xpReward": 60,
        "completedAt": None,
    }


def test_get_completed_quest(quests):
    result = quest_manager.get_quest(quests, "q2")

    assert result["id"] == "q2"
    assert result["status"] == "completed"
    assert result["xpReward"] == 20
    assert result["completedAt"] == "2026-11-09T15:00:00Z"


def test_only_matches_exact_id(quests):
    quests.insert(0, dict(quests[0], id="q10"))

    assert quest_manager.get_quest(quests, "q1")["id"] == "q1"


def test_integer_and_string_ids_are_different(quests):
    quests[0]["id"] = 1
    quests[1]["id"] = "1"

    assert quest_manager.get_quest(quests, 1)["title"] == "Study math"
    assert quest_manager.get_quest(quests, "1")["title"] == "Do the laundry"


@pytest.mark.parametrize("quest_id", ["q1", "q2"])
def test_result_changes_do_not_change_original_quest(quests, quest_id):
    result = quest_manager.get_quest(quests, quest_id)
    result["title"] = "Changed title"
    result["status"] = "changed"

    assert quests[0]["title"] == "Study math"
    assert quests[0]["status"] == "pending"
    assert quests[1]["title"] == "Do the laundry"
    assert quests[1]["status"] == "completed"


def test_lookup_keeps_original_order(quests):
    quest_manager.get_quest(quests, "q2")

    assert [quest["id"] for quest in quests] == ["q1", "q2"]


@pytest.mark.parametrize("quest_id", ["q3", " q1 ", 1])
def test_unknown_id(quests, quest_id):
    with pytest.raises(KeyError):
        quest_manager.get_quest(quests, quest_id)


def test_empty_list():
    with pytest.raises(KeyError):
        quest_manager.get_quest([], "q1")


@pytest.mark.parametrize("quests", [None, "quests", {}, ()])
def test_invalid_quest_collection(quests):
    with pytest.raises(TypeError):
        quest_manager.get_quest(quests, "q1")


@pytest.mark.parametrize("quest", [None, "Study math", 60, []])
def test_invalid_quest_entry(quests, quest):
    with pytest.raises(TypeError):
        quest_manager.get_quest([quest] + quests, "q1")


@pytest.mark.parametrize("quest_id", [None, True, False, 1.5, [], {}])
def test_invalid_id_type(quests, quest_id):
    with pytest.raises(TypeError):
        quest_manager.get_quest(quests, quest_id)


@pytest.mark.parametrize("quest_id", ["", " ", "\t\n"])
def test_blank_id(quests, quest_id):
    with pytest.raises(ValueError):
        quest_manager.get_quest(quests, quest_id)
