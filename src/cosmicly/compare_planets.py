"""Compare your stats on two planets side by side."""

from datetime import date, datetime

from .data import PLANETS
from .planetary_age import age_on_planet
from .planetary_weight import weight_on_planet

def earth_age(birthdate: str | date) -> float:
    """Return how many Earth years have passed since a birthdate.

    Args:
        birthdate: A "YYYY-MM-DD" string, or a date or datetime object.

    Returns:
        The age in fractional Earth years up to today, rounded to 2 decimals.

    Raises:
        TypeError: If birthdate is not a string, date or datetime.
        ValueError: If birthdate is not a real date or is in the future.
    """
    today = date.today()

    if isinstance(birthdate, datetime):
        birthdate = birthdate.date()
    elif isinstance(birthdate, str):
        try:
            birthdate = date.fromisoformat(birthdate)
        except ValueError as error:
            raise ValueError(f"'{birthdate}' is not a real YYYY-MM-DD date") from error
    elif not isinstance(birthdate, date):
        raise TypeError("birthdate must be a 'YYYY-MM-DD' string or a date")

    if birthdate > today:
        raise ValueError("birthdate cannot be in the future")

    days_alive = (today - birthdate).days
    return round(days_alive / 365.25, 2) #365.25 includes leap years


def compare_planets(
    planet_a: str,
    planet_b: str,
    birthdate: str | date,
    weight: float,
) -> dict[str, dict[str, float]]:
    """Return your age and weight on two different planets.

    Args:
        planet_a: The first planet, for example "Mars". Not case-sensitive.
        planet_b: The second planet. Must be different from planet_a.
        birthdate: A "YYYY-MM-DD" string, or a date or datetime object.
        weight: Your weight on Earth, in any unit (kg or lb).

    Returns:
        A dict with one entry per planet, each holding "age" and "weight",
        for example {"mars": {"age": 11.95, "weight": 26.43}, ...}.

    Raises:
        TypeError: If a planet is not a string or weight is not a number.
        ValueError: If a planet is unknown, both planets are the same,
            weight is negative, or the birthdate is invalid.
    """
    if not isinstance(planet_a, str) or not isinstance(planet_b, str):
        raise TypeError("planet names must be strings")
    if isinstance(weight, bool) or not isinstance(weight, (int, float)):
        raise TypeError("weight must be a number")

    planet_a = planet_a.lower()
    planet_b = planet_b.lower()
    for planet in (planet_a, planet_b):
        if planet not in PLANETS:
            raise ValueError(f"'{planet}' is not a known planet")
    if planet_a == planet_b:
        raise ValueError("planet_a and planet_b must be different planets")
    if weight < 0:
        raise ValueError("weight cannot be negative")

    age = earth_age(birthdate)

    comparison = {}
    for planet in (planet_a, planet_b):
        comparison[planet] = {
            "age": age_on_planet(age, planet),
            "weight": weight_on_planet("w", weight, planet),
        }
    return comparison
