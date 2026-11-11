"""Tests for simulated planetary clock readings and input validation."""

from datetime import datetime

import pytest
from cosmicly.relative_time import relative_time

NOON = datetime(2026, 1, 1, 12, 0, 0)


def test_known_times_at_noon():
    """Verify the expected clock readings for Earth, Mars, and Jupiter at Earth noon."""
    assert relative_time("earth", NOON) == "12:00:00"
    assert relative_time("mars", NOON) == "11:40:44"
    assert relative_time("jupiter", NOON) == "05:05:27"


def test_midnight_is_zero_everywhere():
    """Verify that Earth, Mars, and Moon clocks read zero at Earth midnight."""
    midnight = datetime(2026, 1, 1, 0, 0, 0)
    assert relative_time("earth", midnight) == "00:00:00"
    assert relative_time("mars", midnight) == "00:00:00"
    assert relative_time("moon", midnight) == "00:00:00"


def test_earth_matches_real_clock():
    """Verify that Earth's clock reading matches the current local time."""
    before = datetime.now().strftime("%H:%M:%S")
    result = relative_time("earth")
    after = datetime.now().strftime("%H:%M:%S")
    assert result in {before, after}


def test_planet_name_is_not_case_sensitive():
    """Verify that different capitalizations of Mars return the same time."""
    assert relative_time("MARS", NOON) == "11:40:44"
    assert relative_time("Mars", NOON) == "11:40:44"
    assert relative_time("mArS", NOON) == "11:40:44"


def test_unknown_planet():
    """Verify that unknown and empty planet names raise ValueError."""
    with pytest.raises(ValueError):
        relative_time("pluto")
    with pytest.raises(ValueError):
        relative_time("")
    with pytest.raises(ValueError):
        relative_time("sun")


def test_planet_not_a_string():
    """Verify that non-string planet names raise TypeError."""
    with pytest.raises(TypeError):
        relative_time(3)
    with pytest.raises(TypeError):
        relative_time(None)
    with pytest.raises(TypeError):
        relative_time(["mars"])
