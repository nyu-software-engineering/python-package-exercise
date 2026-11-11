import random
import re


_STUDY_KEYWORDS = frozenset(
    {
        "study", "studying", "learn", "learning", "read", "reading", "review", "reviewing",
        "exam", "exams", "homework", "assignment", "assignments", "quiz", "quizzes",
        "flashcards", "lecture", "lectures", "textbook", "textbooks",
    }
)
_STUDY_PHRASES = ("take a test", "taking a test", "practice test", "practice tests", "test prep")
_STUDY_TEMPLATES = (
    "Decipher an Ancient Scroll",
    "Explore the Ancient Library",
    "Unlock the Sage's Hidden Knowledge",
    "Solve the Riddle of the Moonlit Tower",
    "Translate the Wizard's Forgotten Notes",
    "Chart the Stars in the Scholar's Observatory",
    "Uncover the Secrets of the Crystal Archive",
    "Master a Lesson at the Academy of Mages",
)
_EXERCISE_KEYWORDS = frozenset(
    {
        "exercise", "exercising", "workout", "workouts", "jog", "jogging",
        "swim", "swimming", "cycling", "gym", "yoga", "pilates", "cardio",
        "stretch", "stretching", "walk", "walking", "hike", "hiking", "bike", "biking",
    }
)
_EXERCISE_PHRASES = (
    "work out", "working out", "worked out", "go for a run", "go running",
    "morning run", "evening run", "lift weights", "lifting weights",
    "weight lifting", "strength training",
)
_EXERCISE_TEMPLATES = (
    "Train for the Royal Tournament",
    "Conquer the Knight's Endurance Trial",
    "Prepare for the Dragon's Challenge",
    "Climb the Steps of the Sky Fortress",
    "Cross the Ranger's Mountain Pass",
    "Practice with the Guardians of the Grove",
    "Build Your Strength at the Adventurer's Camp",
    "Complete the Trial of the Swift Falcon",
)
_CHORE_KEYWORDS = frozenset(
    {"laundry", "dishes", "vacuum", "vacuuming", "sweep", "sweeping", "mop", "mopping", "housework"}
)
_CHORE_PHRASES = (
    "make the bed", "make my bed", "making the bed", "making my bed",
    "wash clothes", "washing clothes", "wash up", "washing up",
    "take out the trash", "take out trash", "take out the garbage", "take out garbage",
)
_CHORE_TEMPLATES = (
    "Restore Order to the Kingdom",
    "Polish the Royal Castle",
    "Clear the Goblin Hideout",
    "Prepare the Village for the Harvest Festival",
    "Restore the Ranger's Woodland Cabin",
    "Set the Guild Hall in Order",
    "Tend the Royal Courtyard",
    "Bring Balance to the Keeper's Cottage",
)
_CLEANING_ACTIONS = frozenset({"clean", "cleaning", "tidy", "tidying"})
_HOUSEHOLD_PLACES = frozenset(
    {
        "room", "rooms", "bedroom", "bathroom", "kitchen", "house", "home", "garage",
        "apartment", "desk", "floor", "floors", "office",
    }
)
_FALLBACK_TEMPLATES = (
    "Embark on a New Quest",
    "Follow the Trail Beyond the Village",
    "Answer a Call from the Adventurers' Guild",
    "Take the Next Step on Your Hero's Journey",
    "Explore a New Path Through the Enchanted Woods",
    "Discover What Awaits Beyond the Old Gate",
    "Begin a Chapter in the Chronicle of Adventures",
    "Carry Out a Favor for the Woodland Council",
)


_DEFAULT_TEMPLATES = {
    "study": _STUDY_TEMPLATES,
    "exercise": _EXERCISE_TEMPLATES,
    "chores": _CHORE_TEMPLATES,
    "fallback": _FALLBACK_TEMPLATES,
}


def _resolve_templates(custom_templates):
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


def _matches_phrase(normalized_title, phrases):
    return any(f" {phrase} " in normalized_title for phrase in phrases)


def generate_fantasy_description(
    title: str, *, seed: int | None = None, custom_templates: dict | None = None
) -> str:
    if not isinstance(title, str):
        raise TypeError("title must be a string")
    if not title.strip():
        raise ValueError("title must not be blank")
    if seed is not None and (isinstance(seed, bool) or not isinstance(seed, int)):
        raise TypeError("seed must be an integer or None")

    template_sets = _resolve_templates(custom_templates)
    tokens = re.findall(r"\b[a-z]+\b", title.casefold())
    words = set(tokens)
    normalized_title = " " + " ".join(tokens) + " "
    if words & _STUDY_KEYWORDS or _matches_phrase(normalized_title, _STUDY_PHRASES):
        templates = template_sets["study"]
    elif words & _EXERCISE_KEYWORDS or _matches_phrase(normalized_title, _EXERCISE_PHRASES):
        templates = template_sets["exercise"]
    elif words & _CHORE_KEYWORDS or _matches_phrase(normalized_title, _CHORE_PHRASES) or (
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
