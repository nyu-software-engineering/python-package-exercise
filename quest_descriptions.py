"""Generate deterministic fantasy descriptions for everyday task titles."""

import random
import re


_STUDY_KEYWORDS = frozenset(
    {"study", "studying", "learn", "learning", "read", "reading", "review", "reviewing"}
)
_STUDY_TEMPLATES = (
    "Decipher an Ancient Scroll",
    "Explore the Ancient Library",
    "Unlock the Sage's Hidden Knowledge",
)
_EXERCISE_KEYWORDS = frozenset(
    {
        "exercise", "exercising", "workout", "workouts", "jog", "jogging",
        "swim", "swimming", "cycling", "gym",
    }
)
_EXERCISE_TEMPLATES = (
    "Train for the Royal Tournament",
    "Conquer the Knight's Endurance Trial",
    "Prepare for the Dragon's Challenge",
)
_CHORE_KEYWORDS = frozenset(
    {"laundry", "dishes", "vacuum", "vacuuming", "sweep", "sweeping", "mop", "mopping"}
)
_CHORE_TEMPLATES = (
    "Restore Order to the Kingdom",
    "Polish the Royal Castle",
    "Clear the Goblin Hideout",
)
_CLEANING_ACTIONS = frozenset({"clean", "cleaning", "tidy", "tidying"})
_HOUSEHOLD_PLACES = frozenset(
    {"room", "rooms", "bedroom", "bathroom", "kitchen", "house", "home", "garage"}
)


def generate_fantasy_description(title: str, *, seed: int | None = None) -> str:
    """Return a fantasy description without replacing the original task title.

    English keywords match whole words, ignoring case.
    Category priority is study, exercise, then chores, regardless of word order.
    Ambiguous exercise words such as "run" and "train" are not matched.
    Cleaning/tidying requires a household place (e.g. "clean the kitchen");
    a cleaning action alone does not match chores (e.g. "clean code").
    Other nonblank titles, including other languages, get a generic fallback.
    Without a seed, the original default descriptions are preserved.
    An integer seed selects a repeatable study, exercise, or chore template using a
    private random generator, without changing Python's global random state.
    The fallback keeps one template. Different seeds may select the same template.
    No AI service is used.

    Example: ``generate_fantasy_description("Study math", seed=7)``.

    Store the result as ``fantasyDescription`` alongside the original ``title``.
    Call this again when a pending quest's title changes.

    Raises:
        TypeError: If title is not a string or seed is not an integer or None.
            Boolean seeds are not accepted.
        ValueError: If title is empty or contains only whitespace.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not title.strip():
        raise ValueError("title must not be blank")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None")

    words = set(re.findall(r"\b[a-z]+\b", title.casefold()))
    if words & _STUDY_KEYWORDS:
        templates = _STUDY_TEMPLATES
    elif words & _EXERCISE_KEYWORDS:
        templates = _EXERCISE_TEMPLATES
    elif words & _CHORE_KEYWORDS or (
        words & _CLEANING_ACTIONS and words & _HOUSEHOLD_PLACES
    ):
        templates = _CHORE_TEMPLATES
    else:
        return "Embark on a New Quest"

    if seed is None:
        return templates[0]
    return random.Random(seed).choice(templates)


def rename_pending_quest(quest: dict, new_title: str, *, seed: int | None = None) -> dict:
    """Return a pending quest copy with its title and fantasy description updated.

    The caller supplies a quest dictionary and stores the returned copy after
    success. This function does not write to a database or mutate the input.
    It preserves the supplied title exactly, including case and whitespace.
    All other fields (ID, duration, XP, completion time, etc.) are preserved.
    This is a shallow copy, consistent with list_quests; nested metadata is
    shared and should not be mutated through the result.

    Only status="pending" is editable. Missing, completed, and unknown statuses
    are rejected. Title and seed validation follows generate_fantasy_description.
    Pass the same seed again to reproduce template selection; seeds are not
    stored in the quest and omitting one selects the default template.

    Raises:
        TypeError: If quest is not a dictionary, title is not a string, or seed
            is neither an integer (excluding booleans) nor None.
        ValueError: If the quest is not pending or new_title is blank.
    """
    if not isinstance(quest, dict):
        raise TypeError("quest must be a dictionary")
    if quest.get("status") != "pending":
        raise ValueError("only pending quests can be renamed")

    description = generate_fantasy_description(new_title, seed=seed)
    updated = quest.copy()
    updated["title"] = new_title
    updated["fantasyDescription"] = description
    return updated
