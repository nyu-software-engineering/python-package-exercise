"""Generate fictional historical events."""

import random


# Inclusive (earliest, latest) year range and label format for each era.
_ERA_YEARS = {
    "ancient": (3000, 100, "{year} BC"),
    "medieval": (500, 1400, "{year} AD"),
    "modern": (1600, 2000, "{year}"),
}

_HISTORY_TEMPLATES = {
    "ancient": (
        "In {year}, {subject} were declared the official rulers of the kingdom for one afternoon.",
        "In {year}, historians recorded that {subject} built the first pyramid by accident.",
        "In {year}, an ancient treaty was signed to settle the Great {subject} Dispute.",
    ),
    "medieval": (
        "In {year}, a royal decree banned {subject} from every castle in the realm.",
        "In {year}, knights set out on a quest to find the legendary {subject} of destiny.",
        "In {year}, {subject} were crowned champions of the first medieval feast competition.",
    ),
    "modern": (
        "In {year}, {subject} briefly took over the national news cycle for no apparent reason.",
        "In {year}, a landmark court case ruled that {subject} are legally people.",
        "In {year}, scientists confirmed that {subject} were behind the great office printer outage.",
    ),
}


def generate_history(subject: str, era: str) -> str:
    """Generate a fictional historical event about a subject in an era.

    Args:
        subject: Nonempty text describing who or what the event is about.
        era: One of "ancient", "medieval" or "modern". Case-insensitive,
            surrounding whitespace is ignored.

    Returns:
        A fictional historical event with surrounding input whitespace
        removed from the subject. Internal whitespace and capitalization
        of the subject are preserved.

    Raises:
        TypeError: If either argument is not a string.
        ValueError: If subject is empty after trimming, or era is not supported.
    """
    if not isinstance(subject, str):
        raise TypeError("subject must be a string")

    if not isinstance(era, str):
        raise TypeError("era must be a string")

    subject = subject.strip()
    era = era.strip().lower()

    if not subject:
        raise ValueError("subject must not be empty or whitespace-only")

    if era not in _HISTORY_TEMPLATES:
        supported = ", ".join(sorted(_HISTORY_TEMPLATES))
        raise ValueError(f"era must be one of: {supported}")

    first, last, label = _ERA_YEARS[era]
    year = label.format(year=random.randint(min(first, last), max(first, last)))
    template = random.choice(_HISTORY_TEMPLATES[era])

    return template.format(subject=subject, year=year)
