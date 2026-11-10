from datetime import datetime

import pytest
from cosmicly.relative_time import relative_time

NOON = datetime(2026, 1, 1, 12, 0, 0)


def test_known_times_at_noon():
    assert relative_time("earth", NOON) == "12:00:00"
    assert relative_time("mars", NOON) == "11:40:44"
    assert relative_time("jupiter", NOON) == "05:05:27"


def test_midnight_is_zero_everywhere():
    midnight = datetime(2026, 1, 1, 0, 0, 0)
    assert relative_time("earth", midnight) == "00:00:00"
    assert relative_time("mars", midnight) == "00:00:00"
    assert relative_time("moon", midnight) == "00:00:00"


def test_earth_matches_real_clock():
    before = datetime.now().strftime("%H:%M:%S")
    result = relative_time("earth")
    after = datetime.now().strftime("%H:%M:%S")
    assert result == before or result == after


def test_planet_name_is_not_case_sensitive():
    assert relative_time("MARS", NOON) == "11:40:44"
    assert relative_time("Mars", NOON) == "11:40:44"
    assert relative_time("mArS", NOON) == "11:40:44"


def test_unknown_planet():
    with pytest.raises(ValueError):
        relative_time("pluto")
    with pytest.raises(ValueError):
        relative_time("")
    with pytest.raises(ValueError):
        relative_time("sun")


def test_planet_not_a_string():
    with pytest.raises(TypeError):
        relative_time(3)
    with pytest.raises(TypeError):
        relative_time(None)
    with pytest.raises(TypeError):
        relative_time(["mars"])
