from .models import Card


def interpret_card(
    card: Card,
    orientation: str,
    topic: str,
    tone: str,
) -> str:
    """Interpret one tarot card based on orientation, topic, and tone."""
    raise NotImplementedError
