from datetime import date
from .models import Card


DECK: list[Card] = []

def lookup_card(query: str) -> Card:
    """Find a tarot card by name or keyword."""
    raise NotImplementedError



def draw_cards(
    name: str,
    date: date | None = None,
    count: int = 3,
    allow_reversed: bool = True,
) -> list[tuple[Card, str]]:
    """Draw unique tarot cards with deterministic results."""
    raise NotImplementedError

