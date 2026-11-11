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
    actual = travel_at_speed("mars", 100)
    assert actual == "89 years", f"Expected '89 years'. Instead, it returned {actual}"
    actual = travel_at_speed("venus", 100)
    assert actual == "47 years", f"Expected '47 years'. Instead, it returned {actual}"
    actual = travel_at_speed("moon", 100)
    assert actual == "160 days", f"Expected '160 days'. Instead, it returned {actual}"
    actual = travel_at_speed("mars", 78_400_000)
    assert actual == "1 hour", f"Expected '1 hour'. Instead, it returned {actual}"


def test_travel_at_speed_units_and_plurals():
    """Verify time units, singular and plural forms, and subsecond wording."""
    actual = travel_at_speed("moon", 384_400)
    assert actual == "1 hour", f"Expected singular '1 hour'. Instead, it returned {actual}"
    actual = travel_at_speed("moon", 384_400 / 2)
    assert actual == "2 hours", f"Expected plural '2 hours'. Instead, it returned {actual}"
    actual = travel_at_speed("jupiter", LIGHT_SPEED_KMH)
    assert actual == "35 minutes", f"Expected '35 minutes'. Instead, it returned {actual}"
    actual = travel_at_speed("moon", LIGHT_SPEED_KMH)
    assert actual == "1 second", f"Expected '1 second'. Instead, it returned {actual}"
    actual = travel_at_speed("moon", 1e15)
    assert (
        actual == "less than a second"
    ), f"Expected 'less than a second'. Instead, it returned {actual}"


def test_travel_at_speed_planet_name_case_and_spaces():
    """Verify that destination names accept mixed case and surrounding spaces."""
    for name in ("MARS", "Mars", "  mArS "):
        actual = travel_at_speed(name, 100)
        assert (
            actual == "89 years"
        ), f"Expected '89 years' for {name!r}. Instead, it returned {actual}"


def test_travel_at_speed_int_and_float_speed():
    """Verify that integer and float speeds produce strings and equal speeds agree."""
    as_int = travel_at_speed("mars", 100)
    as_float = travel_at_speed("mars", 100.0)
    assert as_int == as_float, f"Expected int and float speeds to match. Got {as_int} and {as_float}"
    slow = travel_at_speed("mars", 0.5)
    assert slow != as_int, f"Expected a slower speed to give a different time. Both were {slow}"
    assert isinstance(as_float, str), f"Expected a string. Instead, it returned {as_float!r}"


def test_travel_at_speed_unknown_planet():
    """Verify that unknown destinations, empty names, and Earth raise ValueError."""
    with pytest.raises(ValueError, match="No such planet"):
        travel_at_speed("pluto", 100)
    with pytest.raises(ValueError, match="No such planet"):
        travel_at_speed("", 100)
    with pytest.raises(ValueError, match="already on Earth"):
        travel_at_speed("earth", 100)


def test_travel_at_speed_planet_wrong_type():
    """Verify that non-string destinations raise TypeError."""
    with pytest.raises(TypeError, match="planet must be a string"):
        travel_at_speed(42, 100)
    with pytest.raises(TypeError, match="planet must be a string"):
        travel_at_speed(None, 100)
    with pytest.raises(TypeError, match="planet must be a string"):
        travel_at_speed(["mars"], 100)


def test_travel_at_speed_bad_speed_value():
    """Verify that zero and negative speeds raise ValueError."""
    with pytest.raises(ValueError, match="greater than 0"):
        travel_at_speed("mars", 0)
    with pytest.raises(ValueError, match="greater than 0"):
        travel_at_speed("mars", -5)
    with pytest.raises(ValueError, match="greater than 0"):
        travel_at_speed("mars", -0.1)


def test_travel_at_speed_bad_speed_type():
    """Verify that strings, None, and booleans raise TypeError as speeds."""
    with pytest.raises(TypeError, match="must be a number"):
        travel_at_speed("mars", "100")
    with pytest.raises(TypeError, match="must be a number"):
        travel_at_speed("mars", None)
    with pytest.raises(TypeError, match="must be a number"):
        travel_at_speed("mars", True)


def test_drive_to():
    """Verify travel times at car speed and rejection of an unknown destination."""
    actual = drive_to("mars")
    assert actual == "89 years", f"Expected '89 years'. Instead, it returned {actual}"
    actual = drive_to("moon")
    expected = travel_at_speed("moon", CAR_SPEED_KMH)
    assert actual == expected, f"Expected drive_to to use car speed ({expected}). Instead, it returned {actual}"
    actual = drive_to("Venus")
    assert actual == "47 years", f"Expected '47 years'. Instead, it returned {actual}"
    with pytest.raises(ValueError, match="No such planet"):
        drive_to("pluto")


def test_fly_to():
    """Verify travel times at plane speed and rejection of a non-string destination."""
    actual = fly_to("mars")
    assert actual == "10 years", f"Expected '10 years'. Instead, it returned {actual}"
    actual = fly_to("moon")
    assert actual == "18 days", f"Expected '18 days'. Instead, it returned {actual}"
    actual = fly_to("saturn")
    expected = travel_at_speed("saturn", PLANE_SPEED_KMH)
    assert actual == expected, f"Expected fly_to to use plane speed ({expected}). Instead, it returned {actual}"
    with pytest.raises(TypeError, match="planet must be a string"):
        fly_to(3)


def test_light_speed_to():
    """Verify travel times at light speed and rejection of Earth as a destination."""
    actual = light_speed_to("mars")
    assert actual == "4 minutes", f"Expected '4 minutes'. Instead, it returned {actual}"
    actual = light_speed_to("neptune")
    assert actual == "4 hours", f"Expected '4 hours'. Instead, it returned {actual}"
    actual = light_speed_to("moon")
    assert actual == "1 second", f"Expected '1 second'. Instead, it returned {actual}"
    with pytest.raises(ValueError, match="already on Earth"):
        light_speed_to("earth")
