"""Generate deterministic fantasy descriptions for everyday task titles."""

import re


_STUDY_KEYWORDS = frozenset(
    {"study", "studying", "learn", "learning", "read", "reading", "review", "reviewing"}
)
_EXERCISE_KEYWORDS = frozenset(
    {
        "exercise", "exercising", "workout", "workouts", "jog", "jogging",
        "swim", "swimming", "cycling", "gym",
    }
)
_CHORE_KEYWORDS = frozenset(
    {"laundry", "dishes", "vacuum", "vacuuming", "sweep", "sweeping", "mop", "mopping"}
)
_CLEANING_ACTIONS = frozenset({"clean", "cleaning", "tidy", "tidying"})
_HOUSEHOLD_PLACES = frozenset(
    {"room", "rooms", "bedroom", "bathroom", "kitchen", "house", "home", "garage"}
)


def generate_fantasy_description(title: str) -> str:
    """Return a fantasy description without replacing the original task title.

    English keywords match whole words, ignoring case.
    Category priority is study, exercise, then chores, regardless of word order.
    Ambiguous exercise words such as "run" and "train" are not matched.
    Cleaning/tidying requires a household place (e.g. "clean the kitchen");
    a cleaning action alone does not match chores (e.g. "clean code").
    Other nonblank titles, including other languages, get a generic fallback.
    The same title always produces the same description; no AI service is used.

    Store the result as ``fantasyDescription`` alongside the original ``title``.
    Call this again when a pending quest's title changes.

    Raises:
        TypeError: If title is not a string.
        ValueError: If title is empty or contains only whitespace.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not title.strip():
        raise ValueError("title must not be blank")

    words = set(re.findall(r"\b[a-z]+\b", title.casefold()))
    if words & _STUDY_KEYWORDS:
        return "Decipher an Ancient Scroll"
    if words & _EXERCISE_KEYWORDS:
        return "Train for the Royal Tournament"
    if words & _CHORE_KEYWORDS or (
        words & _CLEANING_ACTIONS and words & _HOUSEHOLD_PLACES
    ):
        return "Restore Order to the Kingdom"

    return "Embark on a New Quest"
