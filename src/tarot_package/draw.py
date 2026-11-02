from datetime import date
from .models import Card


def draw_cards(
    name: str,
    date: date | None = None,
    count: int = 3,
    allow_reversed: bool = True,
) -> list[tuple[Card, str]]:
    """Draw unique tarot cards with deterministic results."""
    raise NotImplementedError
