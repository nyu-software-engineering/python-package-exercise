"""Contract tests for keeping an edited quest's title and description in sync."""

from copy import deepcopy
import random

import pytest

from quest_descriptions import generate_fantasy_description, rename_pending_quest


@pytest.fixture
def quest():
    return {
        "id": "q1",
        "title": "Study math",
        "fantasyDescription": "Decipher an Ancient Scroll",
        "status": "pending",
        "durationMinutes": 30,
        "xpReward": 30,
        "completedAt": None,
        "metadata": {"tags": ["personal"]},
    }


@pytest.mark.parametrize("new_title, expected", [
    ("Read a book", "Decipher an Ancient Scroll"),
    ("Go swimming", "Train for the Royal Tournament"),
    ("Do laundry", "Restore Order to the Kingdom"),
    ("Clean the kitchen", "Restore Order to the Kingdom"),
    ("Clean code", "Embark on a New Quest"),
    ("买菜", "Embark on a New Quest"),
])
def test_rename_updates_both_fields_and_preserves_other_data(quest, new_title, expected):
    before = deepcopy(quest)
    result = rename_pending_quest(quest, new_title)

    assert result == {**before, "title": new_title, "fantasyDescription": expected}
    assert quest == before
    assert result is not quest
    # The documented shallow-copy contract preserves custom metadata.
    assert result["metadata"] is quest["metadata"]
    result["title"] = "Another title"
    assert quest["title"] == before["title"]


@pytest.mark.parametrize("old_title", ["Read a book", "Go swimming", "Do laundry", "Buy bread"])
@pytest.mark.parametrize("new_title", ["Read a book", "Go swimming", "Do laundry", "Buy bread"])
def test_rename_replaces_stale_descriptions_across_categories(quest, old_title, new_title):
    quest["title"] = old_title
    quest["fantasyDescription"] = generate_fantasy_description(old_title, seed=1)
    result = rename_pending_quest(quest, new_title, seed=7)

    assert result["title"] == new_title
    assert result["fantasyDescription"] == generate_fantasy_description(new_title, seed=7)
    assert result["xpReward"] == quest["xpReward"]


@pytest.mark.parametrize("seed", [None, 0, 7, -10, 2**64])
@pytest.mark.parametrize("title", ["Study math", "Go swimming", "Do laundry", "Buy bread"])
def test_seeded_rename_is_repeatable_and_preserves_global_random_state(quest, title, seed):
    state = random.getstate()
    first = rename_pending_quest(quest, title, seed=seed)
    rename_pending_quest(quest, "Read something else", seed=999)

    assert rename_pending_quest(quest, title, seed=seed) == first
    assert random.getstate() == state


def test_rename_keeps_original_title_formatting(quest):
    result = rename_pending_quest(quest, "  SWIMMING!  ")
    assert result["title"] == "  SWIMMING!  "
    assert result["fantasyDescription"] == "Train for the Royal Tournament"


@pytest.mark.parametrize("status", ["completed", "done", "Pending", "", None, False, []])
def test_non_pending_quests_are_rejected_without_changes(quest, status):
    quest["status"] = status
    before = deepcopy(quest)
    with pytest.raises(ValueError, match="only pending quests"):
        rename_pending_quest(quest, "Do laundry")
    assert quest == before


def test_missing_status_is_rejected(quest):
    del quest["status"]
    before = deepcopy(quest)
    with pytest.raises(ValueError, match="only pending quests"):
        rename_pending_quest(quest, "Do laundry")
    assert quest == before


@pytest.mark.parametrize("value", [None, [], "quest", 1, True])
def test_non_dictionary_quests_are_rejected(value):
    with pytest.raises(TypeError, match="quest must be a dictionary"):
        rename_pending_quest(value, "Do laundry")


@pytest.mark.parametrize("title", [None, 30, True, [], {}, "", "  ", "\t\n"])
def test_invalid_titles_leave_original_quest_unchanged(quest, title):
    before = deepcopy(quest)
    error = ValueError if isinstance(title, str) else TypeError
    with pytest.raises(error, match="title"):
        rename_pending_quest(quest, title)
    assert quest == before


@pytest.mark.parametrize("seed", [True, False, "7", 7.5, [], {}])
def test_invalid_seeds_leave_both_fields_unchanged(quest, seed):
    before = deepcopy(quest)
    with pytest.raises(TypeError, match="seed"):
        rename_pending_quest(quest, "Go swimming", seed=seed)
    assert quest == before


def test_repeated_edits_use_the_latest_title_without_mutating_previous_result(quest):
    first = rename_pending_quest(quest, "Do laundry")
    second = rename_pending_quest(first, "Go swimming")

    assert first["fantasyDescription"] == "Restore Order to the Kingdom"
    assert second["fantasyDescription"] == "Train for the Royal Tournament"
    assert quest["title"] == "Study math"
