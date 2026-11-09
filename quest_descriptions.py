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
_CHORE_KEYWORDS = frozenset(
    {"laundry", "dishes", "vacuum", "vacuuming", "sweep", "sweeping", "mop", "mopping"}
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
    An integer seed selects a repeatable study template using a private random
    generator, without changing Python's global random state. Other categories
    keep their single template. Different seeds may select the same template.
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
        if seed is None:
            return _STUDY_TEMPLATES[0]
        return random.Random(seed).choice(_STUDY_TEMPLATES)
    if words & _EXERCISE_KEYWORDS:
        return "Train for the Royal Tournament"
    if words & _CHORE_KEYWORDS or (
        words & _CLEANING_ACTIONS and words & _HOUSEHOLD_PLACES
    ):
        return "Restore Order to the Kingdom"

    return "Embark on a New Quest"
