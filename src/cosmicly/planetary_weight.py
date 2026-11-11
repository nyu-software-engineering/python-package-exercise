"""Convert a mass or an Earth weight into a weight on another planet."""

from .data import PLANETS


def weight_on_planet(mode, value, planet):
    """Return the weight on the given planet, rounded to two decimal places.

    mode "m"/"mass": value is a mass in kg, the result is in newtons.
    mode "w"/"weight": value is a weight on Earth, the result is in the same unit.

    Raises:
        TypeError: If mode or planet is not a string, or value is not a number.
        ValueError: If mode or planet is unknown, or value is negative.
    """
    if not isinstance(mode, str):
        raise TypeError("_type_ must be a string")

    if not isinstance(planet, str):
        raise TypeError("planet must be a string")

    mode = mode.lower()
    planet = planet.lower()

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError("value must be a number")

    if mode not in {"m", "mass", "w", "weight"}:
        raise ValueError("mode must be either mass or weight (m or w)")

    if planet not in PLANETS:
        raise ValueError("No such planet in our solar system")

    if value < 0:
        raise ValueError("Neither weight nor mass can be negative")

    planet_gravity = PLANETS[planet]["gravity_m_s2"]

    if mode in {"m", "mass"}:
        return round(value * planet_gravity, 2)

    earth_gravity = PLANETS["earth"]["gravity_m_s2"]
    return round(value / earth_gravity * planet_gravity, 2)
