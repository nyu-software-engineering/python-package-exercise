"""Convert ages in Earth years to years on other planets."""

from .data import PLANETS


def age_on_planet(age, planet):
    """Return an age in Earth years converted to years on the given planet - two decimal places.

    Raises:
        TypeError: If age is not an int or float, or planet is not a string.
        ValueError: If age is negative or planet is unknown.
    """
    if not isinstance(age, (int, float)) or isinstance(age, bool):
        raise TypeError("age must be a number")

    if not isinstance(planet, str):
        raise TypeError("planet must be a string")

    planet = planet.lower()

    if age < 0:
        raise ValueError("age cannot be negative")

    if planet not in PLANETS:
        raise ValueError("No such planet in our solar system")

    planet_year = PLANETS[planet]["orbital_period_days"]
    earth_year = PLANETS["earth"]["orbital_period_days"]
    planetary_age = age * earth_year / planet_year
    return round(planetary_age, 2)
