"""Tests for fantasy templates, category priority, and the generic fallback."""

import pytest

from quest_descriptions import generate_fantasy_description


@pytest.mark.parametrize(
    "title",
    [
        "Study math for 60 minutes",
        "Studying history",
        "Learn Python",
        "Learning Spanish",
        "Read a chapter",
        "Reading class notes",
        "Review lecture slides",
        "Reviewing vocabulary",
        "  STUDY math!  ",
        "Read, summarize, and discuss",
    ],
)
def test_study_tasks_use_the_scroll_template(title):
    assert generate_fantasy_description(title) == "Decipher an Ancient Scroll"


@pytest.mark.parametrize(
    "title",
    [
        "Exercise for 30 minutes",
        "Exercising after work",
        "Finish a workout",
        "Two workouts this week",
        "Jog around the park",
        "Go jogging",
        "Swim ten laps",
        "Go swimming",
        "Go cycling",
        "  GYM!  ",
    ],
)
def test_exercise_tasks_use_the_tournament_template(title):
    assert generate_fantasy_description(title) == "Train for the Royal Tournament"


@pytest.mark.parametrize(
    "title",
    ["Read about swimming", "Swimming then study math", "Study math then swimming"],
)
def test_study_takes_priority_over_exercise(title):
    assert generate_fantasy_description(title) == "Decipher an Ancient Scroll"


@pytest.mark.parametrize(
    "title",
    [
        "Do the laundry",
        "Wash the dishes",
        "Vacuum the carpet",
        "Vacuuming the hallway",
        "Sweep the floor",
        "Sweeping the porch",
        "Mop the floor",
        "Mopping the kitchen",
        "Clean the room",
        "Cleaning the bathroom",
        "Tidy the house",
        "Tidying the bedroom",
        "  CLEAN the KITCHEN!  ",
    ],
)
def test_chores_use_the_kingdom_template(title):
    assert generate_fantasy_description(title) == "Restore Order to the Kingdom"


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Read then do laundry", "Decipher an Ancient Scroll"),
        ("Do laundry then read", "Decipher an Ancient Scroll"),
        ("Workout then wash dishes", "Train for the Royal Tournament"),
        ("Wash dishes then workout", "Train for the Royal Tournament"),
        ("Study, workout, and do laundry", "Decipher an Ancient Scroll"),
    ],
)
def test_chores_do_not_override_existing_categories(title, expected):
    assert generate_fantasy_description(title) == expected


@pytest.mark.parametrize(
    "title",
    [
        "Water the plants",
        "Buy bread",
        "Preview a movie",
        "Sort unread emails",
        "学习数学",
        "Buy a swimsuit",
        "Run unit tests",
        "Train a model",
        "Clean code",
        "Cleaning a dataset",
        "Clean",
        "Visit the kitchen",
        "Buy a dishwasher",
        "Tidy the imports",
    ],
)
def test_unmatched_titles_use_the_generic_fallback(title):
    assert generate_fantasy_description(title) == "Embark on a New Quest"


def test_results_are_consistent_across_calls():
    study_description = generate_fantasy_description("Study math")
    other_description = generate_fantasy_description("Water the plants")
    exercise_description = generate_fantasy_description("Go swimming")
    chore_description = generate_fantasy_description("Do laundry")

    assert generate_fantasy_description("Study math") == study_description
    assert generate_fantasy_description("Water the plants") == other_description
    assert generate_fantasy_description("STUDY MATH") == study_description
    assert generate_fantasy_description("Go swimming") == exercise_description
    assert generate_fantasy_description("Do laundry") == chore_description


@pytest.mark.parametrize("title", ["", " ", "\t\n"])
def test_blank_titles_are_rejected(title):
    with pytest.raises(ValueError, match="title must not be blank"):
        generate_fantasy_description(title)


@pytest.mark.parametrize("title", [None, 60, 1.5, True, [], {}])
def test_non_string_titles_are_rejected(title):
    with pytest.raises(TypeError, match="title must be a string"):
        generate_fantasy_description(title)
