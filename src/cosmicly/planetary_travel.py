"""How long it would take to travel from Earth to another planet."""

from .data import PLANETS

CAR_SPEED_KMH = 100
PLANE_SPEED_KMH = 900
LIGHT_SPEED_KMH = 1_079_252_848.8

MOON_DISTANCE_KM = 384_400  # data.py stores the Moon at Earth's distance from the Sun

SECONDS_PER_UNIT = [
    ("year", 365.25 * 24 * 3600),
    ("day", 24 * 3600),
    ("hour", 3600),
    ("minute", 60),
    ("second", 1),
]


def distance_from_earth(planet: str) -> float:
    """Return the closest-approach distance in km from Earth to a planet.

    Raises:
        TypeError: If planet is not a string.
        ValueError: If planet is unknown, or is Earth itself.
    """
    if not isinstance(planet, str):
        raise TypeError("planet must be a string")
    planet = planet.strip().lower()
    if planet not in PLANETS:
        raise ValueError("No such planet in our solar system")
    if planet == "earth":
        raise ValueError("you are already on Earth")
    if planet == "moon":
        return MOON_DISTANCE_KM
    return abs(PLANETS[planet]["distance_from_sun_km"] - PLANETS["earth"]["distance_from_sun_km"])


def format_duration(seconds: float) -> str:
    """Turn a number of seconds into readable text, like '89 years'."""
    for unit, size in SECONDS_PER_UNIT:
        if seconds >= size:
            amount = round(seconds / size)
            return f"{amount} {unit}" + ("" if amount == 1 else "s")
    return "less than a second"


def travel_at_speed(planet: str, speed_kmh: float) -> str:
    """Return how long it takes to reach a planet from Earth at a given speed.

    Args:
        planet: Planet name, case-insensitive (e.g. "Mars").
        speed_kmh: Travel speed in kilometres per hour, greater than 0.

    Returns:
        Travel time as readable text, e.g. "89 years".

    Raises:
        TypeError: If planet is not a string or speed is not a number.
        ValueError: If planet is unknown or Earth, or speed is not positive.
    """
    if isinstance(speed_kmh, bool) or not isinstance(speed_kmh, (int, float)):
        raise TypeError("speed_kmh must be a number")
    if speed_kmh <= 0:
        raise ValueError("speed_kmh must be greater than 0")
    hours = distance_from_earth(planet) / speed_kmh
    return format_duration(hours * 3600)


def drive_to(planet: str) -> str:
    """Travel time to a planet by car (100 km/h)."""
    return travel_at_speed(planet, CAR_SPEED_KMH)


def fly_to(planet: str) -> str:
    """Travel time to a planet by plane (900 km/h)."""
    return travel_at_speed(planet, PLANE_SPEED_KMH)


def light_speed_to(planet: str) -> str:
    """Travel time to a planet at the speed of light."""
    return travel_at_speed(planet, LIGHT_SPEED_KMH)
