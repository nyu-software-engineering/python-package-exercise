from datetime import date
from .models import Card



def interpret_spread(
    drawn: list[tuple[Card, str]],
    topic: str,
    tone: str,
) -> str:
    """Interpret a three-card Past, Present, Future spread."""
    raise NotImplementedError


def daily_reading(
    name: str,
    date: date | None = None,
    topic: str = "general",
    tone: str = "mystic",
) -> str:
    """Generate a complete daily tarot reading."""
    raise NotImplementedError
