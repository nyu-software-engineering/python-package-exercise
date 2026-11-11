import random

import pytest

from quest_descriptions import generate_fantasy_description
from quest_manager import create_quest, rename_quest


CATEGORY_TEMPLATES = {
    "study": ["Study adventure"],
    "exercise": ["Exercise adventure"],
    "chores": ["Chore adventure"],
    "fallback": ["General adventure"],
}


@pytest.mark.parametrize("title, category", [
    ("work out", "exercise"),
    ("Working out after lunch", "exercise"),
    ("Worked out before breakfast", "exercise"),
    ("WORK-OUT!", "exercise"),
    ("Go for a run", "exercise"),
    ("Morning run", "exercise"),
    ("Go running", "exercise"),
    ("Lift weights", "exercise"),
    ("Weight lifting", "exercise"),
    ("Strength training", "exercise"),
    ("Practice yoga", "exercise"),
    ("Stretch for ten minutes", "exercise"),
    ("Walk around the park", "exercise"),
    ("Go hiking", "exercise"),
    ("Take an exam", "study"),
    ("Prepare for final exams", "study"),
    ("Finish homework", "study"),
    ("Complete an assignment", "study"),
    ("Practice flashcards", "study"),
    ("Attend a lecture", "study"),
    ("Take a quiz", "study"),
    ("Take a test", "study"),
    ("Taking a test", "study"),
    ("Finish a practice test", "study"),
    ("Test prep", "study"),
    ("Make the bed", "chores"),
    ("Making my bed", "chores"),
    ("Wash clothes", "chores"),
    ("Wash up", "chores"),
    ("Take out the trash", "chores"),
    ("Take out garbage", "chores"),
    ("Do housework", "chores"),
    ("Clean the desk", "chores"),
    ("Tidy the apartment", "chores"),
    ("Clean the floor", "chores"),
])
def test_common_phrases_match_the_intended_category(title, category):
    result = generate_fantasy_description(title, custom_templates=CATEGORY_TEMPLATES)
    assert result == CATEGORY_TEMPLATES[category][0]


@pytest.mark.parametrize("title", [
    "Work outside", "Working outside", "Check the work output", "Fix a workflow",
    "Book a flight", "Run unit tests", "Train a model", "Clean code",
    "Clean a dataset", "Preview a movie", "Readiness report", "An example project",
])
def test_matching_respects_word_and_phrase_boundaries(title):
    assert generate_fantasy_description(title, custom_templates=CATEGORY_TEMPLATES) == "General adventure"


@pytest.mark.parametrize("title, category", [
    ("Read about working out", "study"),
    ("Go running then take a test", "study"),
    ("Take an exam then do housework", "study"),
    ("Make the bed after working out", "exercise"),
])
def test_phrase_matching_preserves_category_priority(title, category):
    assert generate_fantasy_description(title, custom_templates=CATEGORY_TEMPLATES) == CATEGORY_TEMPLATES[category][0]


@pytest.mark.parametrize("title", ["Read books", "Work out", "Make the bed", "Buy bread"])
def test_each_default_category_has_eight_seeded_choices(title):
    state = random.getstate()
    choices = {generate_fantasy_description(title, seed=seed) for seed in range(256)}
    assert len(choices) == 8
    assert all(isinstance(choice, str) and choice.strip() for choice in choices)
    assert generate_fantasy_description(title, seed=7) == generate_fantasy_description(title, seed=7)
    assert random.getstate() == state


def test_common_phrases_flow_through_creation_and_title_edits():
    quests = create_quest([], "Work out", 90)
    assert quests[0]["fantasyDescription"] == "Train for the Royal Tournament"
    renamed = rename_quest(quests, quests[0]["id"], "Take an exam")
    assert renamed[0]["fantasyDescription"] == "Decipher an Ancient Scroll"
    assert renamed[0]["durationMinutes"] == 90
    assert renamed[0]["xpReward"] == 90
    assert quests[0]["title"] == "Work out"
