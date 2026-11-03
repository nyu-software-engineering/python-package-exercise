from difflib import get_close_matches

from .cards_cups import CUPS
from .cards_major import MAJOR
from .cards_pentacles import PENTACLES
from .cards_swords import SWORDS
from .cards_wands import WANDS
from .models import Card

DECK: list[Card] = [*MAJOR, *WANDS, *CUPS, *SWORDS, *PENTACLES]


def lookup_card(query: str) -> Card:
    """Find a tarot card by name or keyword.

    Matching is case-insensitive and tried in this order: exact name,
    partial name, exact keyword, then a fuzzy match on the name.

    Raises:
        TypeError: if query is not a string.
        ValueError: if query is empty or no card matches.
    """
    if not isinstance(query, str):
        raise TypeError("query must be a string")
    text = query.strip().casefold()
    if not text:
        raise ValueError("query must not be empty")

    for card in DECK:
        if card.name.casefold() == text:
            return card
    for card in DECK:
        if text in card.name.casefold():
            return card
    for card in DECK:
        if text in (word.casefold() for word in card.keywords):
            return card

    names = {card.name.casefold(): card for card in DECK}
    close = get_close_matches(text, names, n=1, cutoff=0.6)
    if close:
        return names[close[0]]
    raise ValueError(f"no card matches {query!r}")