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


_DEFAULT_TEMPLATES = {
    "study": _STUDY_TEMPLATES,
    "exercise": _EXERCISE_TEMPLATES,
    "chores": _CHORE_TEMPLATES,
    "fallback": ("Embark on a New Quest",),
}


def _resolve_templates(custom_templates):
    """Validate all overrides eagerly and snapshot their lists as tuples."""
    templates = _DEFAULT_TEMPLATES.copy()
    if custom_templates is None:
        return templates
    if not isinstance(custom_templates, dict):
        raise TypeError("custom_templates must be a dictionary or None")
    for category, choices in custom_templates.items():
        if category not in templates:
            raise ValueError(f"unknown template category: {category!r}")
        if not isinstance(choices, (list, tuple)):
            raise TypeError("template choices must be a list or tuple")
        if not choices:
            raise ValueError("template choices must not be empty")
        for choice in choices:
            if not isinstance(choice, str):
                raise TypeError("each template must be a string")
            if not choice.strip():
                raise ValueError("templates must not be blank")
        templates[category] = tuple(choices)
    return templates


def generate_fantasy_description(
    title: str, *, seed: int | None = None, custom_templates: dict | None = None
) -> str:
    """Return a fantasy description without replacing the original task title.

    English keywords match whole words, ignoring case.
    Category priority is study, exercise, then chores, regardless of word order.
    Ambiguous exercise words such as "run" and "train" are not matched.
    Cleaning/tidying requires a household place (e.g. "clean the kitchen");
    a cleaning action alone does not match chores (e.g. "clean code").
    Other nonblank titles, including other languages, get a generic fallback.
    Without custom templates or a seed, original defaults are preserved.
    An integer seed selects a repeatable study, exercise, or chore template using a
    private random generator, without changing Python's global random state.
    The default fallback keeps one template. Different seeds may select the same template.
    custom_templates optionally overrides study, exercise, chores, or fallback.
    Values must be nonempty lists/tuples of nonblank strings; omitted categories
    keep their defaults. All entries are validated, even for unmatched categories.
    Templates are literal text, not format strings; their whitespace is preserved.
    Without a seed, the first template is used. Input configuration is not mutated.
    No AI service is used.

    Example: ``generate_fantasy_description("Study math", seed=7)``.

    Store the result as ``fantasyDescription`` alongside the original ``title``.
    Call this again when a pending quest's title changes.

    Raises:
        TypeError: If title is not a string or seed is not an integer or None.
            Boolean seeds and invalid custom template types are not accepted.
        ValueError: If title is blank, a template category is unknown, or a
            template list/string is empty or blank.
    """
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not title.strip():
        raise ValueError("title must not be blank")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None")

    template_sets = _resolve_templates(custom_templates)
    words = set(re.findall(r"\b[a-z]+\b", title.casefold()))
    if words & _STUDY_KEYWORDS:
        templates = template_sets["study"]
    elif words & _EXERCISE_KEYWORDS:
        templates = template_sets["exercise"]
    elif words & _CHORE_KEYWORDS or (
        words & _CLEANING_ACTIONS and words & _HOUSEHOLD_PLACES
    ):
        templates = template_sets["chores"]
    else:
        templates = template_sets["fallback"]

    if seed is None:
        return templates[0]
    return random.Random(seed).choice(templates)


def rename_pending_quest(
    quest: dict, new_title: str, *, seed: int | None = None,
    custom_templates: dict | None = None,
) -> dict:
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
    stored in the quest and omitting one selects the first template.
    custom_templates follows the generator contract and must be passed on each
    edit; configuration is not stored in the quest. Invalid overrides leave the
    original quest unchanged.

    Raises:
        TypeError: If quest is not a dictionary, title is not a string, or seed
            is neither an integer (excluding booleans) nor None.
        ValueError: If the quest is not pending or new_title is blank.
    """
    if not isinstance(quest, dict):
        raise TypeError("quest must be a dictionary")
    if quest.get("status") != "pending":
        raise ValueError("only pending quests can be renamed")

    description = generate_fantasy_description(
        new_title, seed=seed, custom_templates=custom_templates
    )
    updated = quest.copy()
    updated["title"] = new_title
    updated["fantasyDescription"] = description
    return updated
