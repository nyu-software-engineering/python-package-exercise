from .models import Card


def lucky_extras(
    drawn: list[tuple[Card, str]],
    category: str,
) -> str:
    """Generate a lucky extra based on the drawn cards."""
    raise NotImplementedError
