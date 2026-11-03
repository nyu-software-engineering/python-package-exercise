from .models import Card

PENTACLES: list[Card] = [
    Card(
        name="Ace of Pentacles",
        arcana="minor",
        suit="pentacles",
        upright="A promising opportunity for money or a new project is on offer.",
        reversed="A chance is slipping away through poor planning, so tighten up.",
        keywords=("opportunity", "prosperity", "new venture", "stability"),
    ),
]