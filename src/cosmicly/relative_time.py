"""Simulate the current time on another planet using its solar day length."""

from datetime import datetime
from .data import PLANETS


def relative_time(planet, now=None):
    """Return the simulated time on a planet as an HH:MM:SS string.

    Convert the time elapsed since local Earth midnight using the planet's
    solar day length. Both clocks start at midnight together.

    Raises:
        TypeError: If planet is not a string.
        ValueError: If planet is unknown.
    """

    
    
    if not isinstance(planet, str):
        raise TypeError("planet must be a string")

    planet = planet.lower()
    if planet not in PLANETS:
        raise ValueError("No such planet in our solar system")

    if now is None:
        now = datetime.now()

    earth_seconds = now.hour * 3600 + now.minute * 60 + now.second
    day_seconds = PLANETS[planet]["solar_day_hours"] * 3600

    fraction_of_day = (earth_seconds % day_seconds) / day_seconds
    clock_seconds = int(fraction_of_day * 86400)
    hours, remainder = divmod(clock_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


if __name__ == "__main__":
    print(relative_time("mars"))
