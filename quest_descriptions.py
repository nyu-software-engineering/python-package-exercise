"""Generate deterministic fantasy descriptions for everyday task titles."""

import re


_STUDY_KEYWORDS = frozenset(
    {"study", "studying", "learn", "learning", "read", "reading", "review", "reviewing"}
)


def generate_fantasy_description(title: str) -> str:
    """Return a fantasy description without replacing the original task title.

    English study keywords are matched as whole words, ignoring case.
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

    return "Embark on a New Quest"
