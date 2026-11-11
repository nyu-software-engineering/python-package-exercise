"""How long it would take to travel from Earth to another planet."""

from datetime import date

import ephem

from .data import PLANETS

CAR_SPEED_KMH = 100
PLANE_SPEED_KMH = 900
LIGHT_SPEED_KMH = 1_079_252_848.8

MOON_DISTANCE_KM = 384_400  # data.py stores the Moon at Earth's distance from the Sun
KM_PER_AU = 149_597_870.7  # ephem gives distances in astronomical units

SECONDS_PER_UNIT = [
    ("year", 365.25 * 24 * 3600),
    ("day", 24 * 3600),
    ("hour", 3600),
    ("minute", 60),
    ("second", 1),
]


def _to_date(on_date):
    """Turn a 'YYYY-MM-DD' string or a date into a date.

    Raises:
        TypeError: If on_date is not a string or a date.
        ValueError: If the string is not a real YYYY-MM-DD date.
    """
    if isinstance(on_date, date):
        return on_date
    if isinstance(on_date, str):
        try:
            return date.fromisoformat(on_date)
        except ValueError as error:
            raise ValueError(f"'{on_date}' is not a real YYYY-MM-DD date") from error
    raise TypeError("on_date must be a 'YYYY-MM-DD' string or a date")


def distance_from_earth(planet: str, on_date=None) -> float:
    """Return the distance in km from Earth to a planet.

    Args:
        planet: Planet name, case-insensitive (e.g. "Mars").
        on_date: Optional "YYYY-MM-DD" string or date. Without it, the
            closest-approach distance from data.py is used. With it, the
            real distance on that day is calculated, since planets move.

    Raises:
        TypeError: If planet is not a string, or on_date is the wrong type.
        ValueError: If planet is unknown or Earth, or on_date is not a real date.
    """
    if not isinstance(planet, str):
        raise TypeError("planet must be a string")
    planet = planet.strip().lower()
    if planet not in PLANETS:
        raise ValueError("No such planet in our solar system")
    if planet == "earth":
        raise ValueError("you are already on Earth")

    if on_date is None:
        if planet == "moon":
            return MOON_DISTANCE_KM
        return abs(
            PLANETS[planet]["distance_from_sun_km"]
            - PLANETS["earth"]["distance_from_sun_km"]
        )

    day = _to_date(on_date)
    body = getattr(ephem, planet.capitalize())()
    body.compute(day.strftime("%Y/%m/%d"))
    return body.earth_distance * KM_PER_AU


def format_duration(seconds: float) -> str:
    """Turn a number of seconds into readable text, like '89 years'."""
    for unit, size in SECONDS_PER_UNIT:
        if seconds >= size:
            amount = round(seconds / size)
            return f"{amount} {unit}" + ("" if amount == 1 else "s")
    return "less than a second"


def travel_at_speed(planet: str, speed_kmh: float, on_date=None) -> str:
    """Return how long it takes to reach a planet from Earth at a given speed.

    Args:
        planet: Planet name, case-insensitive (e.g. "Mars").
        speed_kmh: Travel speed in kilometres per hour, greater than 0.
        on_date: Optional departure date ("YYYY-MM-DD" or a date) to use the
            real distance on that day instead of the closest approach.

    Returns:
        Travel time as readable text, e.g. "89 years".

    Raises:
        TypeError: If planet is not a string, speed is not a number,
            or on_date is the wrong type.
        ValueError: If planet is unknown or Earth, speed is not positive,
            or on_date is not a real date.
    """
    if isinstance(speed_kmh, bool) or not isinstance(speed_kmh, (int, float)):
        raise TypeError("speed_kmh must be a number")
    if speed_kmh <= 0:
        raise ValueError("speed_kmh must be greater than 0")
    hours = distance_from_earth(planet, on_date) / speed_kmh
    return format_duration(hours * 3600)


def drive_to(planet: str, on_date=None) -> str:
    """Travel time to a planet by car (100 km/h)."""
    return travel_at_speed(planet, CAR_SPEED_KMH, on_date)


def fly_to(planet: str, on_date=None) -> str:
    """Travel time to a planet by plane (900 km/h)."""
    return travel_at_speed(planet, PLANE_SPEED_KMH, on_date)


def light_speed_to(planet: str, on_date=None) -> str:
    """Travel time to a planet at the speed of light."""
    return travel_at_speed(planet, LIGHT_SPEED_KMH, on_date)


def arrival_age(planet: str, speed_kmh: float, current_age: float, on_date=None) -> float:
    """Return how old you will be when you arrive at a planet.

    Args:
        planet: Planet name, case-insensitive (e.g. "Mars").
        speed_kmh: Travel speed in kilometres per hour, greater than 0.
        current_age: Your age in Earth years today, 0 or more.
        on_date: Optional departure date ("YYYY-MM-DD" or a date) to use the
            real distance on that day instead of the closest approach.

    Returns:
        Your age in Earth years on arrival, rounded to 2 decimals.

    Raises:
        TypeError: If planet is not a string, speed or age is not a number,
            or on_date is the wrong type.
        ValueError: If planet is unknown or Earth, speed is not positive,
            age is negative, or on_date is not a real date.
    """
    if isinstance(speed_kmh, bool) or not isinstance(speed_kmh, (int, float)):
        raise TypeError("speed_kmh must be a number")
    if speed_kmh <= 0:
        raise ValueError("speed_kmh must be greater than 0")
    if isinstance(current_age, bool) or not isinstance(current_age, (int, float)):
        raise TypeError("current_age must be a number")
    if current_age < 0:
        raise ValueError("current_age cannot be negative")

    hours = distance_from_earth(planet, on_date) / speed_kmh
    years = hours / (365.25 * 24)
    return round(current_age + years, 2)

