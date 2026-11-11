from copy import deepcopy
from uuid import UUID

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
            "metadata": {"tags": ["school"]},
        },
        {
            "id": "q2",
            "title": "Do laundry",
            "durationMinutes": 20,
            "fantasyDescription": "Restore Order to the Kingdom",
            "status": "completed",
            "xpReward": 20,
            "completedAt": "2026-11-09T15:00:00Z",
        },
    ]


def test_create_first_quest():
    original = []
    result = quest_manager.create_quest(original, "Study math", 60)
    quest = result[0]

    assert original == []
    assert len(result) == 1
    assert isinstance(quest["id"], str)
    assert quest["id"]
    assert {key: value for key, value in quest.items() if key != "id"} == {
        "title": "Study math",
        "durationMinutes": 60,
        "fantasyDescription": "Decipher an Ancient Scroll",
        "status": "pending",
        "xpReward": 60,
        "completedAt": None,
    }


@pytest.mark.parametrize(
    "title, description",
    [
        ("Read a book", "Decipher an Ancient Scroll"),
        ("Go swimming", "Train for the Royal Tournament"),
        ("Do laundry", "Restore Order to the Kingdom"),
        ("Buy bread", "Embark on a New Quest"),
        ("\u5b66\u4e60\u6570\u5b66", "Embark on a New Quest"),
        ("  STUDY math!  ", "Decipher an Ancient Scroll"),
    ],
)
def test_create_uses_teammate_descriptions(quests, title, description):
    result = quest_manager.create_quest(quests, title, 30)

    assert result[-1]["title"] == title
    assert result[-1]["fantasyDescription"] == description


@pytest.mark.parametrize("duration", [1, 30, 250])
def test_create_calculates_reward(duration):
    quest = quest_manager.create_quest([], "Study math", duration)[0]

    assert quest["durationMinutes"] == duration
    assert quest["xpReward"] == duration
    assert quest["status"] == "pending"


def test_create_keeps_existing_data_and_generates_different_ids(quests):
    before = deepcopy(quests)
    first = quest_manager.create_quest(quests, "Read a book", 30)
    second = quest_manager.create_quest(first, "Read a book", 30)

    assert quests == before
    assert second[:2] == before
    assert len(second) == 4
    assert len({quest["id"] for quest in second}) == 4
    first[0]["title"] = "Changed"
    assert quests[0]["title"] == "Study math"


def test_create_retries_an_existing_id(quests, monkeypatch):
    quests[0]["id"] = "00000000000000000000000000000001"
    ids = iter([UUID(int=1), UUID(int=2)])
    monkeypatch.setattr(quest_manager, "uuid4", lambda: next(ids))

    result = quest_manager.create_quest(quests, "Buy bread", 10)

    assert result[-1]["id"] == "00000000000000000000000000000002"
    assert len(result) == 3


def test_create_and_rename_forward_seed(quests):
    created = quest_manager.create_quest([], "Study math", 30, seed=7)[0]
    renamed = quest_manager.rename_quest(quests, "q1", "Read a book", seed=7)

    assert created["fantasyDescription"] == "Chart the Stars in the Scholar's Observatory"
    assert renamed[0]["fantasyDescription"] == "Chart the Stars in the Scholar's Observatory"


@pytest.mark.parametrize(
    "new_title, description",
    [
        ("Read a book", "Decipher an Ancient Scroll"),
        ("Go swimming", "Train for the Royal Tournament"),
        ("Do laundry", "Restore Order to the Kingdom"),
        ("Buy bread", "Embark on a New Quest"),
        ("  SWIMMING!  ", "Train for the Royal Tournament"),
    ],
)
def test_rename_replaces_the_right_quest(quests, new_title, description):
    before = deepcopy(quests)
    result = quest_manager.rename_quest(quests, "q1", new_title)

    assert result[0] == {
        **before[0], "title": new_title, "fantasyDescription": description
    }
    assert result[1] == before[1]
    assert quests == before
    assert result[0]["metadata"] is quests[0]["metadata"]


@pytest.mark.parametrize("duration", [1, 45, 250])
def test_duration_and_reward_change_together(quests, duration):
    before = deepcopy(quests)
    result = quest_manager.change_quest_duration(quests, "q1", duration)

    assert result[0] == {
        **before[0], "durationMinutes": duration, "xpReward": duration
    }
    assert result[1] == before[1]
    assert quests == before


def test_edit_returns_copies_of_other_quests(quests):
    before = deepcopy(quests)
    renamed = quest_manager.rename_quest(quests, "q1", "Buy bread")
    changed = quest_manager.change_quest_duration(quests, "q1", 45)
    renamed[0]["title"] = "Changed again"
    renamed[1]["title"] = "Changed completed title"
    changed[0]["xpReward"] = 999
    changed[1]["status"] = "pending"

    assert quests == before


def test_create_lookup_edit_delete_flow(quests):
    before = deepcopy(quests)
    created = quest_manager.create_quest(quests, "Study history", 30)
    quest_id = created[-1]["id"]
    assert quest_manager.get_quest(created, quest_id)["xpReward"] == 30

    renamed = quest_manager.rename_quest(created, quest_id, "Do laundry")
    changed = quest_manager.change_quest_duration(renamed, quest_id, 45)
    edited = quest_manager.get_quest(changed, quest_id)
    assert edited["title"] == "Do laundry"
    assert edited["fantasyDescription"] == "Restore Order to the Kingdom"
    assert edited["durationMinutes"] == 45
    assert edited["xpReward"] == 45
    assert edited["status"] == "pending"
    assert quest_manager.delete_quest(changed, quest_id) == before
    assert quests == before


@pytest.mark.parametrize(
    "title, error",
    [("", ValueError), (" \t\n", ValueError), (None, TypeError),
     (30, TypeError), (True, TypeError), ([], TypeError), ({}, TypeError)],
)
def test_invalid_titles_leave_data_unchanged(quests, title, error):
    before = deepcopy(quests)

    with pytest.raises(error):
        quest_manager.create_quest(quests, title, 30)
    with pytest.raises(error):
        quest_manager.rename_quest(quests, "q1", title)

    assert quests == before


@pytest.mark.parametrize(
    "duration, error",
    [(0, ValueError), (-1, ValueError), (None, TypeError),
     ("30", TypeError), (30.0, TypeError), (1.5, TypeError),
     (True, TypeError), (False, TypeError), ([], TypeError), ({}, TypeError)],
)
def test_invalid_durations_leave_data_unchanged(quests, duration, error):
    before = deepcopy(quests)

    with pytest.raises(error):
        quest_manager.create_quest(quests, "Study math", duration)
    with pytest.raises(error):
        quest_manager.change_quest_duration(quests, "q1", duration)

    assert quests == before


@pytest.mark.parametrize("seed", [True, False, "7", 7.5, [], {}])
def test_invalid_seed_leaves_data_unchanged(quests, seed):
    before = deepcopy(quests)

    with pytest.raises(TypeError):
        quest_manager.create_quest(quests, "Study math", 30, seed=seed)
    with pytest.raises(TypeError):
        quest_manager.rename_quest(quests, "q1", "Buy bread", seed=seed)

    assert quests == before


@pytest.mark.parametrize("status", ["completed", "done", "Pending", "", None, []])
def test_non_pending_quests_cannot_be_edited(quests, status):
    quests[0]["status"] = status
    before = deepcopy(quests)

    with pytest.raises(ValueError):
        quest_manager.rename_quest(quests, "q1", "Buy bread")
    with pytest.raises(ValueError):
        quest_manager.change_quest_duration(quests, "q1", 45)

    assert quests == before


def test_missing_status_cannot_be_edited(quests):
    del quests[0]["status"]

    with pytest.raises(ValueError):
        quest_manager.rename_quest(quests, "q1", "Buy bread")
    with pytest.raises(ValueError):
        quest_manager.change_quest_duration(quests, "q1", 45)


def test_duplicate_ids_cannot_be_edited(quests):
    quests.append(quests[0].copy())
    before = deepcopy(quests)

    with pytest.raises(ValueError):
        quest_manager.rename_quest(quests, "q1", "Buy bread")
    with pytest.raises(ValueError):
        quest_manager.change_quest_duration(quests, "q1", 45)

    assert quests == before


@pytest.mark.parametrize("quest_id", ["missing", " q1 "])
def test_unknown_id(quests, quest_id):
    before = deepcopy(quests)

    with pytest.raises(KeyError):
        quest_manager.rename_quest(quests, quest_id, "Buy bread")
    with pytest.raises(KeyError):
        quest_manager.change_quest_duration(quests, quest_id, 45)

    assert quests == before


@pytest.mark.parametrize("quest_id", [None, True, False, 1.5, [], {}])
def test_invalid_id_type(quests, quest_id):
    with pytest.raises(TypeError):
        quest_manager.rename_quest(quests, quest_id, "Buy bread")
    with pytest.raises(TypeError):
        quest_manager.change_quest_duration(quests, quest_id, 45)


@pytest.mark.parametrize("quest_id", ["", " ", "\t\n"])
def test_blank_id(quests, quest_id):
    with pytest.raises(ValueError):
        quest_manager.rename_quest(quests, quest_id, "Buy bread")
    with pytest.raises(ValueError):
        quest_manager.change_quest_duration(quests, quest_id, 45)


@pytest.mark.parametrize("quests", [None, "quests", {}, ()])
def test_invalid_collection(quests):
    with pytest.raises(TypeError):
        quest_manager.create_quest(quests, "Buy bread", 30)
    with pytest.raises(TypeError):
        quest_manager.rename_quest(quests, "q1", "Buy bread")
    with pytest.raises(TypeError):
        quest_manager.change_quest_duration(quests, "q1", 45)


@pytest.mark.parametrize("quest", [None, "Study math", 60, []])
def test_invalid_collection_entry(quests, quest):
    quests.append(quest)

    with pytest.raises(TypeError):
        quest_manager.create_quest(quests, "Buy bread", 30)
    with pytest.raises(TypeError):
        quest_manager.rename_quest(quests, "q1", "Buy bread")
    with pytest.raises(TypeError):
        quest_manager.change_quest_duration(quests, "q1", 45)
