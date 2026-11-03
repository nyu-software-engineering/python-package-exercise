from .models import Card

MAJOR: list[Card] = [
    Card(
        name="The Fool",
        arcana="major",
        suit=None,
        upright="A fresh start is calling, so take the leap with an open heart.",
        reversed="Slow down and look before you leap, because recklessness is near.",
        keywords=("beginnings", "innocence", "adventure", "spontaneity"),
    ),
    Card(
        name="The Magician",
        arcana="major",
        suit=None,
        upright="You already hold every tool you need, so turn your ideas into action.",
        reversed="Talent is being wasted or misused, so check your focus and honesty.",
        keywords=("willpower", "skill", "manifestation", "resourcefulness"),
    ),
]