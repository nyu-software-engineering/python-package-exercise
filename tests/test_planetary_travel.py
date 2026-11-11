"""Tests for the planetary_travel module."""

import pytest

from cosmicly.planetary_travel import (
    CAR_SPEED_KMH,
    LIGHT_SPEED_KMH,
    PLANE_SPEED_KMH,
    drive_to,
    fly_to,
    light_speed_to,
    travel_at_speed,
)


def test_travel_at_speed_known_values():
    """Verify expected travel times for Mars, Venus, and the Moon."""
    assert travel_at_speed("mars", 100) == "89 years"
    assert travel_at_speed("venus", 100) == "47 years"
    assert travel_at_speed("moon", 100) == "160 days"
    assert travel_at_speed("mars", 78_400_000) == "1 hour"


def test_travel_at_speed_units_and_plurals():
    """Verify time units, singular and plural forms, and subsecond wording."""
    assert travel_at_speed("moon", 384_400) == "1 hour"
    assert travel_at_speed("moon", 384_400 / 2) == "2 hours"
    assert travel_at_speed("jupiter", LIGHT_SPEED_KMH) == "35 minutes"
    assert travel_at_speed("moon", LIGHT_SPEED_KMH) == "1 second"
    assert travel_at_speed("moon", 1e15) == "less than a second"


def test_travel_at_speed_planet_name_case_and_spaces():
    """Verify that destination names accept mixed case and surrounding spaces."""
    assert travel_at_speed("MARS", 100) == "89 years"
    assert travel_at_speed("Mars", 100) == "89 years"
    assert travel_at_speed("  mArS ", 100) == "89 years"


def test_travel_at_speed_int_and_float_speed():
    """Verify that integer and float speeds produce strings and equal speeds agree."""
    assert travel_at_speed("mars", 100) == travel_at_speed("mars", 100.0)
    assert travel_at_speed("mars", 0.5) != travel_at_speed("mars", 100)
    assert isinstance(travel_at_speed("mars", 100.0), str)


def test_travel_at_speed_unknown_planet():
    """Verify that unknown destinations, empty names, and Earth raise ValueError."""
    with pytest.raises(ValueError):
        travel_at_speed("pluto", 100)
    with pytest.raises(ValueError):
        travel_at_speed("", 100)
    with pytest.raises(ValueError):
        travel_at_speed("earth", 100)


def test_travel_at_speed_planet_wrong_type():
    """Verify that non-string destinations raise TypeError."""
    with pytest.raises(TypeError):
        travel_at_speed(42, 100)
    with pytest.raises(TypeError):
        travel_at_speed(None, 100)
    with pytest.raises(TypeError):
        travel_at_speed(["mars"], 100)


def test_travel_at_speed_bad_speed_value():
    """Verify that zero and negative speeds raise ValueError."""
    with pytest.raises(ValueError):
        travel_at_speed("mars", 0)
    with pytest.raises(ValueError):
        travel_at_speed("mars", -5)
    with pytest.raises(ValueError):
        travel_at_speed("mars", -0.1)


def test_travel_at_speed_bad_speed_type():
    """Verify that strings, None, and booleans raise TypeError as speeds."""
    with pytest.raises(TypeError):
        travel_at_speed("mars", "100")
    with pytest.raises(TypeError):
        travel_at_speed("mars", None)
    with pytest.raises(TypeError):
        travel_at_speed("mars", True)


def test_drive_to():
    """Verify travel times at car speed and rejection of an unknown destination."""
    assert drive_to("mars") == "89 years"
    assert drive_to("moon") == travel_at_speed("moon", CAR_SPEED_KMH)
    assert drive_to("Venus") == "47 years"
    with pytest.raises(ValueError):
        drive_to("pluto")


def test_fly_to():
    """Verify travel times at plane speed and rejection of a non-string destination."""
    assert fly_to("mars") == "10 years"
    assert fly_to("moon") == "18 days"
    assert fly_to("saturn") == travel_at_speed("saturn", PLANE_SPEED_KMH)
    with pytest.raises(TypeError):
        fly_to(3)


def test_light_speed_to():
    """Verify travel times at light speed and rejection of Earth as a destination."""
    assert light_speed_to("mars") == "4 minutes"
    assert light_speed_to("neptune") == "4 hours"
    assert light_speed_to("moon") == "1 second"
    with pytest.raises(ValueError):
        light_speed_to("earth")
