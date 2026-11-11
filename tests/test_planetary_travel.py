"""Tests for the planetary_travel module."""

from datetime import date, datetime

import pytest

from cosmicly.planetary_travel import (
    CAR_SPEED_KMH,
    LIGHT_SPEED_KMH,
    PLANE_SPEED_KMH,
    arrival_age,
    distance_from_earth,
    drive_to,
    fly_to,
    format_duration,
    light_speed_to,
    travel_at_speed,
)

YEAR_SECONDS = 365.25 * 24 * 3600



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
    assert as_int == as_float, (
        f"Expected int and float speeds to match."
        f"Got {as_int} and {as_float}"
    )
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
    assert actual == expected, (
        f"Expected drive_to to use car speed ({expected}). "
        f"Instead, it returned {actual}"
    )
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
    assert actual == expected, (
        f"Expected fly_to to use plane speed ({expected})."
        f"Instead, it returned {actual}"
    )
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



def test_format_duration_units():
    """Verify each time unit and its singular and plural forms."""
    assert format_duration(1) == "1 second", "Expected '1 second'"
    assert format_duration(59) == "59 seconds", "Expected '59 seconds'"
    assert format_duration(60) == "1 minute", "Expected '1 minute'"
    assert format_duration(7200) == "2 hours", "Expected '2 hours'"
    assert format_duration(86400) == "1 day", "Expected '1 day'"
    assert format_duration(2 * YEAR_SECONDS) == "2 years", "Expected '2 years'"


def test_format_duration_rounding_and_tiny_values():
    """Verify rounding to the nearest unit and wording for under a second."""
    actual = format_duration(0)
    assert actual == "less than a second", f"Expected 'less than a second'. Got {actual}"
    actual = format_duration(0.5)
    assert actual == "less than a second", f"Expected 'less than a second'. Got {actual}"
    actual = format_duration(89)
    assert actual == "1 minute", f"Expected 89 seconds to round to '1 minute'. Got {actual}"


def test_distance_from_earth_without_date():
    """Verify closest-approach distances from data.py and the fixed Moon distance."""
    actual = distance_from_earth("mars")
    assert actual == 78_400_000, f"Expected 78,400,000 km. Got {actual}"
    actual = distance_from_earth("venus")
    assert actual == 41_400_000, f"Expected 41,400,000 km. Got {actual}"
    actual = distance_from_earth("Mercury")
    assert actual == 91_700_000, f"Expected 91,700,000 km. Got {actual}"
    actual = distance_from_earth("moon")
    assert actual == 384_400, f"Expected 384,400 km. Got {actual}"


def test_distance_from_earth_bad_planet():
    """Verify unknown planets, Earth, and non-strings are rejected."""
    with pytest.raises(ValueError, match="No such planet"):
        distance_from_earth("pluto")
    with pytest.raises(ValueError, match="already on Earth"):
        distance_from_earth("earth", "2026-11-10")
    with pytest.raises(TypeError, match="planet must be a string"):
        distance_from_earth(42)


def test_distance_from_earth_with_date():
    """Verify a date gives the real distance, whether string, date, or datetime."""
    from_string = distance_from_earth("mars", "2026-11-10")
    assert from_string == pytest.approx(
        203_187_602, rel=1e-4
    ), f"Expected about 203,187,602 km on 2026-11-10. Got {from_string}"
    from_date = distance_from_earth("mars", date(2026, 11, 10))
    assert from_date == from_string, f"Expected date and string to match. Got {from_date}"
    from_datetime = distance_from_earth("mars", datetime(2026, 11, 10, 15, 0))
    assert (
        from_datetime == from_string
    ), f"Expected the time of day to be ignored. Got {from_datetime}"


def test_distance_from_earth_changes_over_the_year():
    """Verify distances move during a year and stay within real limits."""
    distances = [distance_from_earth("mars", date(2026, month, 1)) for month in range(1, 13)]
    assert len(set(distances)) == 12, "Expected Mars's distance to change every month"
    assert all(
        54_000_000 < d < 402_000_000 for d in distances
    ), f"Expected Mars to stay 54M to 402M km away. Got {distances}"
    moon = distance_from_earth("moon", "2026-11-10")
    assert 356_000 < moon < 407_000, f"Expected the Moon 356k to 407k km away. Got {moon}"


def test_distance_from_earth_bad_dates():
    """Verify impossible dates raise ValueError and wrong types raise TypeError."""
    with pytest.raises(ValueError, match="not a real"):
        distance_from_earth("mars", "2026-13-01")
    with pytest.raises(ValueError, match="not a real"):
        distance_from_earth("mars", "tomorrow")
    with pytest.raises(TypeError, match="on_date must be"):
        distance_from_earth("mars", 20261110)
    with pytest.raises(TypeError, match="on_date must be"):
        distance_from_earth("mars", [2026])


def test_travel_functions_with_date():
    """Verify every travel function passes the date through."""
    actual = drive_to("mars", "2026-11-10")
    assert actual == "232 years", f"Expected '232 years'. Got {actual}"
    actual = fly_to("mars", "2026-11-10")
    assert actual == "26 years", f"Expected '26 years'. Got {actual}"
    actual = light_speed_to("mars", date(2026, 11, 10))
    assert actual == "11 minutes", f"Expected '11 minutes'. Got {actual}"
    actual = travel_at_speed("mars", 100, date(2026, 11, 10))
    assert actual == "232 years", f"Expected '232 years'. Got {actual}"
    actual = drive_to("mars")
    assert actual == "89 years", f"Expected no date to keep '89 years'. Got {actual}"


def test_arrival_age_values():
    """Verify arrival ages for whole, zero, and fractional starting ages."""
    actual = arrival_age("mars", 100, 20)
    assert actual == 109.44, f"Expected 109.44. Got {actual}"
    actual = arrival_age("moon", 900, 30)
    assert actual == 30.05, f"Expected 30.05. Got {actual}"
    actual = arrival_age("mars", 100, 0)
    assert actual == 89.44, f"Expected 89.44. Got {actual}"
    actual = arrival_age("mars", 100, 20.5)
    assert actual == 109.94, f"Expected 109.94. Got {actual}"
    assert isinstance(actual, float), f"Expected a float. Got {actual!r}"


def test_arrival_age_with_date_and_light_speed():
    """Verify a date changes the answer and light speed barely ages you."""
    actual = arrival_age("mars", 100, 20, "2026-11-10")
    assert actual == 251.79, f"Expected 251.79. Got {actual}"
    same = arrival_age("mars", 100, 20, date(2026, 11, 10))
    assert same == actual, f"Expected date and string to match. Got {same}"
    assert actual > arrival_age("mars", 100, 20), "Expected a later, farther trip to take longer"
    actual = arrival_age("moon", LIGHT_SPEED_KMH, 40)
    assert actual == 40.0, f"Expected 40.0 at light speed. Got {actual}"


def test_arrival_age_bad_age():
    """Verify negative and non-number ages are rejected."""
    with pytest.raises(ValueError, match="cannot be negative"):
        arrival_age("mars", 100, -1)
    with pytest.raises(TypeError, match="current_age must be a number"):
        arrival_age("mars", 100, "20")
    with pytest.raises(TypeError, match="current_age must be a number"):
        arrival_age("mars", 100, True)
    with pytest.raises(TypeError, match="current_age must be a number"):
        arrival_age("mars", 100, None)

def test_arrival_age_bad_planet_speed_and_date():
    """Verify bad planets, speeds, and dates are rejected."""
    with pytest.raises(ValueError, match="No such planet"):
        arrival_age("pluto", 100, 20)
    with pytest.raises(ValueError, match="already on Earth"):
        arrival_age("earth", 100, 20)
    with pytest.raises(ValueError, match="greater than 0"):
        arrival_age("mars", 0, 20)
    with pytest.raises(TypeError, match="must be a number"):
        arrival_age("mars", "fast", 20)
    with pytest.raises(ValueError, match="not a real"):
        arrival_age("mars", 100, 20, "2026-02-30")
