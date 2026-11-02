from dataclasses import dataclass


@dataclass(frozen=True)
class Card:
    name: str
    arcana: str
    suit: str | None
    upright: str
    reversed: str
    keywords: tuple[str, ...]
