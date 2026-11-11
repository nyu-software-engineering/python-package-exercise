"""Tests for simulated planetary clock readings and input validation."""

from datetime import datetime

import pytest
from cosmicly.relative_time import relative_time

NOON = datetime(2026, 1, 1, 12, 0, 0)
MIDNIGHT = datetime(2026, 1, 1, 0, 0, 0)


def test_known_times_at_noon():
    """Verify the expected clock readings for Earth, Mars, and Jupiter at Earth noon."""
    actual = relative_time("earth", NOON)
    assert actual == "12:00:00", f"Expected '12:00:00'. Instead, it returned {actual}"
    actual = relative_time("mars", NOON)
    assert actual == "11:40:44", f"Expected '11:40:44'. Instead, it returned {actual}"
    actual = relative_time("jupiter", NOON)
    assert actual == "05:05:27", f"Expected '05:05:27'. Instead, it returned {actual}"


def test_midnight_is_zero_everywhere():
    """Verify that Earth, Mars, and Moon clocks read zero at Earth midnight."""
    actual = relative_time("earth", MIDNIGHT)
    assert actual == "00:00:00", f"Expected '00:00:00'. Instead, it returned {actual}"
    actual = relative_time("mars", MIDNIGHT)
    assert actual == "00:00:00", f"Expected '00:00:00'. Instead, it returned {actual}"
    actual = relative_time("moon", MIDNIGHT)
    assert actual == "00:00:00", f"Expected '00:00:00'. Instead, it returned {actual}"


def test_earth_matches_real_clock():
    """Verify that Earth's clock reading matches the current local time."""
    before = datetime.now().strftime("%H:%M:%S")
    actual = relative_time("earth")
    after = datetime.now().strftime("%H:%M:%S")
    assert actual in (before, after), (
        f"Expected {before} or {after}. Instead, it returned {actual}"
    )


def test_returns_hh_mm_ss_text():
    """Verify that the result is an 8-character HH:MM:SS string."""
    actual = relative_time("neptune", NOON)
    assert isinstance(actual, str), f"Expected a string. Instead, it returned {type(actual)}"
    assert len(actual) == 8, f"Expected 8 characters. Instead, it returned {actual}"
    assert actual[2] == ":" and actual[5] == ":", f"Expected HH:MM:SS. Instead, it returned {actual}"


def test_planet_name_is_not_case_sensitive():
    """Verify that different capitalizations of Mars return the same time."""
    actual = relative_time("MARS", NOON)
    assert actual == "11:40:44", f"Expected '11:40:44'. Instead, it returned {actual}"
    actual = relative_time("Mars", NOON)
    assert actual == "11:40:44", f"Expected '11:40:44'. Instead, it returned {actual}"
    actual = relative_time("mArS", NOON)
    assert actual == "11:40:44", f"Expected '11:40:44'. Instead, it returned {actual}"


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


def test_now_not_a_datetime():
    """Verify that a now value that is not a datetime raises TypeError."""
    with pytest.raises(TypeError):
        relative_time("mars", "12:00:00")
    with pytest.raises(TypeError):
        relative_time("mars", 12)
    with pytest.raises(TypeError):
        relative_time("mars", [NOON])
