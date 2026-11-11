import random

import pytest

from quest_descriptions import generate_fantasy_description


FALLBACK_CHOICES = {
    "Embark on a New Quest",
    "Follow the Trail Beyond the Village",
    "Answer a Call from the Adventurers' Guild",
    "Take the Next Step on Your Hero's Journey",
    "Explore a New Path Through the Enchanted Woods",
    "Discover What Awaits Beyond the Old Gate",
    "Begin a Chapter in the Chronicle of Adventures",
    "Carry Out a Favor for the Woodland Council",
}


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
        "\u5b66\u4e60\u6570\u5b66",
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


@pytest.mark.parametrize("seed", [0, 7, -10, 2**64])
def test_seeded_study_descriptions_are_repeatable(seed):
    first = generate_fantasy_description("Study math", seed=seed)
    generate_fantasy_description("Read a book", seed=seed + 1)

    assert generate_fantasy_description("Study math", seed=seed) == first
    assert generate_fantasy_description("  STUDY math!  ", seed=seed) == first


def test_seeds_offer_multiple_study_templates():
    descriptions = {
        generate_fantasy_description("Study math", seed=seed)
        for seed in range(20)
    }

    assert len(descriptions) > 1
    assert descriptions <= {
        "Decipher an Ancient Scroll",
        "Explore the Ancient Library",
        "Unlock the Sage's Hidden Knowledge",
        "Solve the Riddle of the Moonlit Tower",
        "Translate the Wizard's Forgotten Notes",
        "Chart the Stars in the Scholar's Observatory",
        "Uncover the Secrets of the Crystal Archive",
        "Master a Lesson at the Academy of Mages",
    }


def test_no_seed_preserves_the_original_study_description():
    assert generate_fantasy_description("Study math") == "Decipher an Ancient Scroll"
    assert (
        generate_fantasy_description("Study math", seed=None)
        == "Decipher an Ancient Scroll"
    )


@pytest.mark.parametrize("title", ["Study math", "Go swimming", "Do laundry"])
def test_seed_does_not_change_global_random_state(title):
    state = random.getstate()
    generate_fantasy_description(title, seed=7)

    assert random.getstate() == state


def test_seeded_fallback_stays_in_generic_templates():
    assert (
        generate_fantasy_description("Water the plants", seed=7)
        in FALLBACK_CHOICES
    )


def test_seed_preserves_study_priority():
    expected = generate_fantasy_description("Read a book", seed=7)
    assert generate_fantasy_description("Read about swimming", seed=7) == expected
    assert generate_fantasy_description("Do laundry then study", seed=7) == expected


@pytest.mark.parametrize("seed", [True, False, "7", 7.5, [], {}])
@pytest.mark.parametrize("title", ["Study math", "Go swimming", "Do laundry", "Water the plants"])
def test_invalid_seeds_are_rejected(title, seed):
    with pytest.raises(TypeError, match="seed must be an integer or None"):
        generate_fantasy_description(title, seed=seed)


@pytest.mark.parametrize("seed", [0, 7, -10, 2**64])
def test_seeded_exercise_descriptions_are_repeatable(seed):
    first = generate_fantasy_description("Go swimming", seed=seed)
    generate_fantasy_description("Study math", seed=seed + 1)
    generate_fantasy_description("Go swimming", seed=seed + 1)

    assert generate_fantasy_description("Go swimming", seed=seed) == first
    assert generate_fantasy_description("  GO SWIMMING!  ", seed=seed) == first


def test_seeds_offer_multiple_exercise_templates():
    descriptions = {
        generate_fantasy_description("Go swimming", seed=seed)
        for seed in range(20)
    }

    assert len(descriptions) > 1
    assert descriptions <= {
        "Train for the Royal Tournament",
        "Conquer the Knight's Endurance Trial",
        "Prepare for the Dragon's Challenge",
        "Climb the Steps of the Sky Fortress",
        "Cross the Ranger's Mountain Pass",
        "Practice with the Guardians of the Grove",
        "Build Your Strength at the Adventurer's Camp",
        "Complete the Trial of the Swift Falcon",
    }


def test_no_seed_preserves_the_original_exercise_description():
    assert generate_fantasy_description("Go swimming") == "Train for the Royal Tournament"
    assert (
        generate_fantasy_description("Go swimming", seed=None)
        == "Train for the Royal Tournament"
    )


def test_seed_preserves_exercise_priority_over_chores():
    expected = generate_fantasy_description("Workout", seed=7)

    assert generate_fantasy_description("Workout then do laundry", seed=7) == expected
    assert generate_fantasy_description("Do laundry then workout", seed=7) == expected


@pytest.mark.parametrize("seed", [0, 7, -10, 2**64])
@pytest.mark.parametrize("title", ["Do laundry", "Clean the kitchen"])
def test_seeded_chore_descriptions_are_repeatable(title, seed):
    first = generate_fantasy_description(title, seed=seed)
    generate_fantasy_description("Study math", seed=seed + 1)
    generate_fantasy_description(title, seed=seed + 1)

    assert generate_fantasy_description(title, seed=seed) == first
    assert generate_fantasy_description(f"  {title.upper()}!  ", seed=seed) == first


def test_seeds_offer_multiple_chore_templates():
    descriptions = {
        generate_fantasy_description("Do laundry", seed=seed)
        for seed in range(20)
    }

    assert len(descriptions) > 1
    assert descriptions <= {
        "Restore Order to the Kingdom",
        "Polish the Royal Castle",
        "Clear the Goblin Hideout",
        "Prepare the Village for the Harvest Festival",
        "Restore the Ranger's Woodland Cabin",
        "Set the Guild Hall in Order",
        "Tend the Royal Courtyard",
        "Bring Balance to the Keeper's Cottage",
    }


def test_no_seed_preserves_the_original_chore_description():
    assert generate_fantasy_description("Do laundry") == "Restore Order to the Kingdom"
    assert (
        generate_fantasy_description("Do laundry", seed=None)
        == "Restore Order to the Kingdom"
    )


@pytest.mark.parametrize("title", ["Clean code", "Visit the kitchen", "Buy a dishwasher"])
def test_seed_does_not_broaden_chore_matching(title):
    for seed in range(20):
        assert generate_fantasy_description(title, seed=seed) in FALLBACK_CHOICES
