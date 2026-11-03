from .models import Card

SWORDS: list[Card] = [
    Card(
        name="Three of Swords",
        arcana="minor",
        suit="swords",
        upright="A painful truth stings now, but facing it starts the healing.",
        reversed="The hurt is slowly easing, so let go of an old grudge.",
        keywords=("heartbreak", "grief", "sorrow", "truth"),
    ),
]