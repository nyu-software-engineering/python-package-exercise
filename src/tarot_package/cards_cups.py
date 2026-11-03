from .models import Card

CUPS: list[Card] = [
    Card(
        name="Two of Cups",
        arcana="minor",
        suit="cups",
        upright="A warm, balanced connection is forming between two people.",
        reversed="A bond feels uneven or strained, and honest talk is needed.",
        keywords=("partnership", "attraction", "harmony", "connection"),
    ),
]