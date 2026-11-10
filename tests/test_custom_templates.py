"""Custom templates preserve matching rules and support safe quest edits."""

from copy import deepcopy
import random

import pytest

from quest_descriptions import generate_fantasy_description, rename_pending_quest


@pytest.mark.parametrize("category, title", [
    ("study", "Read a book"), ("exercise", "Go swimming"),
    ("chores", "Clean the kitchen"), ("fallback", "Buy bread"),
])
def test_category_override_preserves_text_and_config(category, title):
    config = {category: ["  Brave {hero}!  ", "Another adventure"]}
    before = deepcopy(config)
    assert generate_fantasy_description(title, custom_templates=config) == "  Brave {hero}!  "
    assert config == before
    assert generate_fantasy_description(title) != "  Brave {hero}!  "


@pytest.mark.parametrize("config", [None, {}])
@pytest.mark.parametrize("title", ["Study math", "Workout", "Do laundry", "Buy bread"])
def test_empty_configuration_keeps_defaults(config, title):
    for seed in [None, 0, 7, -10]:
        assert generate_fantasy_description(title, seed=seed, custom_templates=config) == (
            generate_fantasy_description(title, seed=seed)
        )


def test_partial_overrides_keep_other_defaults_and_priority():
    config = {"exercise": ("Train with a wizard",), "chores": ["Tidy the castle"]}
    assert generate_fantasy_description("Read then workout", custom_templates=config) == "Decipher an Ancient Scroll"
    assert generate_fantasy_description("Do laundry then workout", custom_templates=config) == "Train with a wizard"
    assert generate_fantasy_description("Do laundry", custom_templates=config) == "Tidy the castle"
    assert generate_fantasy_description("Clean code", custom_templates=config) == "Embark on a New Quest"


@pytest.mark.parametrize("category, title", [
    ("study", "Study math"), ("exercise", "Workout"),
    ("chores", "Do laundry"), ("fallback", "买菜"),
])
def test_custom_seed_selection_is_repeatable_and_private(category, title):
    config = {category: ["Adventure A", "Adventure B", "Adventure C"]}
    before = deepcopy(config)
    state = random.getstate()
    results = set()
    for seed in [-10, 2**64, *range(20)]:
        first = generate_fantasy_description(title, seed=seed, custom_templates=config)
        assert generate_fantasy_description(title, seed=seed, custom_templates=config) == first
        results.add(first)
    assert 1 < len(results) <= 3
    assert results <= set(config[category])
    assert random.getstate() == state
    assert config == before


@pytest.mark.parametrize("config, error", [
    ([], TypeError), ("study", TypeError), (True, TypeError),
    ({"unknown": ["Adventure"]}, ValueError),
    ({"Study": ["Adventure"]}, ValueError),
    ({"study": "Adventure"}, TypeError),
    ({"study": {"Adventure"}}, TypeError),
    ({"study": None}, TypeError),
    ({"study": []}, ValueError), ({"study": ()}, ValueError),
    ({"study": ["valid", "  \t"]}, ValueError),
    ({"study": ["valid", 1]}, TypeError),
])
def test_invalid_config_is_rejected_before_renaming(config, error):
    quest = {"id": "q1", "title": "Study math", "status": "pending",
             "fantasyDescription": "Old description", "xpReward": 30}
    before = deepcopy(quest)
    # Validate the study override even though this title matches fallback.
    with pytest.raises(error):
        generate_fantasy_description("Buy bread", custom_templates=config)
    with pytest.raises(error):
        rename_pending_quest(quest, "Buy bread", custom_templates=config)
    assert quest == before


def test_rename_uses_custom_templates_without_storing_configuration():
    quest = {"id": "q1", "title": "Study math", "status": "pending", "xpReward": 30}
    before = deepcopy(quest)
    config = {"exercise": ["Train with a wizard", "Race a dragon"]}
    updated = rename_pending_quest(quest, "Workout", seed=7, custom_templates=config)
    assert updated == {**quest, "title": "Workout", "fantasyDescription":
                       generate_fantasy_description("Workout", seed=7, custom_templates=config)}
    assert quest == before
    assert updated is not quest


def test_overrides_do_not_leak_between_calls():
    config = {"study": ["Visit the wizard"]}
    first = generate_fantasy_description("Study math", custom_templates=config)
    config["study"][0] = "Visit the library"
    assert first == "Visit the wizard"
    assert generate_fantasy_description("Study math", custom_templates=config) == "Visit the library"
    assert generate_fantasy_description("Study math") == "Decipher an Ancient Scroll"
