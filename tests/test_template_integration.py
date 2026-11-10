"""Exercise custom description themes through the public quest-management API."""

from copy import deepcopy

import pytest

from quest_manager import change_quest_duration, create_quest, rename_quest


@pytest.mark.parametrize("category, title", [
    ("study", "Study math"), ("exercise", "Go swimming"),
    ("chores", "Do laundry"), ("fallback", "Buy bread"),
])
def test_create_and_rename_use_the_same_custom_theme(category, title):
    theme = {category: ["Adventure A", "Adventure B", "Adventure C"]}
    before = deepcopy(theme)
    quests = create_quest([], title, 30, seed=7, custom_templates=theme)
    original = deepcopy(quests)
    renamed = rename_quest(quests, quests[0]["id"], title, seed=7, custom_templates=theme)

    assert quests[0]["fantasyDescription"] in theme[category]
    assert renamed == quests
    assert quests == original
    assert theme == before
    assert set(quests[0]) == {
        "id", "title", "durationMinutes", "fantasyDescription",
        "status", "xpReward", "completedAt",
    }


def test_theme_survives_category_change_and_duration_edit():
    theme = {"study": ["Visit the wizard"], "chores": ["Tidy the castle"]}
    quests = create_quest([], "Study math", 30, custom_templates=theme)
    quests = create_quest(quests, "Go swimming", 10, custom_templates=theme)
    before = deepcopy(quests)
    quest_id = quests[0]["id"]
    renamed = rename_quest(quests, quest_id, "Do laundry", custom_templates=theme)
    updated = change_quest_duration(renamed, quest_id, 45)

    assert updated[0] == {**before[0], "title": "Do laundry",
                          "fantasyDescription": "Tidy the castle",
                          "durationMinutes": 45, "xpReward": 45}
    assert updated[1] == before[1]
    assert updated[1]["fantasyDescription"] == "Train for the Royal Tournament"
    assert quests == before
    assert renamed[0]["durationMinutes"] == 30


def test_omitting_theme_on_next_rename_restores_defaults():
    quests = create_quest([], "Study math", 30, custom_templates={"study": ["Custom"]})
    updated = rename_quest(quests, quests[0]["id"], "Study math")
    assert updated[0]["fantasyDescription"] == "Decipher an Ancient Scroll"
    assert quests[0]["fantasyDescription"] == "Custom"


@pytest.mark.parametrize("theme, error", [
    ("theme", TypeError), ({"unknown": ["Custom"]}, ValueError),
    ({"study": []}, ValueError), ({"study": [" "]}, ValueError),
    ({"study": [1]}, TypeError),
])
def test_invalid_templates_leave_existing_collection_unchanged(theme, error):
    quests = create_quest([], "Do laundry", 30)
    before = deepcopy(quests)
    with pytest.raises(error):
        create_quest(quests, "Buy bread", 10, custom_templates=theme)
    with pytest.raises(error):
        rename_quest(quests, quests[0]["id"], "Buy bread", custom_templates=theme)
    assert quests == before


def test_custom_theme_does_not_bypass_completed_quest_protection():
    quests = create_quest([], "Study math", 30)
    quests[0]["status"] = "completed"
    before = deepcopy(quests)
    with pytest.raises(ValueError, match="only pending quests"):
        rename_quest(quests, quests[0]["id"], "Read a book",
                     custom_templates={"study": ["Custom"]})
    assert quests == before
