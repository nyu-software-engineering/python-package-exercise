"""Tests for the compare_planets module."""

import importlib
from datetime import date, datetime, timedelta

import pytest

from cosmicly.compare_planets import compare_planets, earth_age

# The module itself, so its teammate functions can be swapped for fakes.
COMPARE_MODULE = importlib.import_module("cosmicly.compare_planets")


def days_ago(days: int) -> date:
    """Return the date that was the given number of days before today."""
    return date.today() - timedelta(days=days)


def fake_age_on_planet(age, planet):
    """Stand-in for age_on_planet that just reports what it was given."""
    return (age, planet)


def fake_weight_on_planet(_type_, value, planet):
    """Stand-in for weight_on_planet that just reports what it was given."""
    return (_type_, value, planet)


def use_fakes(monkeypatch):
    """Replace the teammates' functions inside compare_planets with fakes."""
    monkeypatch.setattr(COMPARE_MODULE, "age_on_planet", fake_age_on_planet)
    monkeypatch.setattr(COMPARE_MODULE, "weight_on_planet", fake_weight_on_planet)


class Tests:
    """Unit tests for earth_age and compare_planets."""

    def test_earth_age_from_string(self):
        """
        Verify a YYYY-MM-DD string exactly four years ago gives 4.0.
        """
        actual = earth_age(days_ago(1461).isoformat())
        assert isinstance(
            actual, float
        ), f"Expected earth_age() to return a float. Instead, it returned {actual}"
        assert actual == pytest.approx(
            4.0
        ), f"Expected an age of 4.0. Instead, it returned {actual}"

    def test_earth_age_from_date_object(self):
        """
        Verify a date object gives the same age as the matching string.
        """
        actual = earth_age(days_ago(1461))
        assert actual == pytest.approx(
            4.0
        ), f"Expected an age of 4.0. Instead, it returned {actual}"

    def test_earth_age_from_datetime_object(self):
        """
        Verify a datetime object is accepted and its time of day is ignored.
        """
        birthdate = days_ago(1461)
        actual = earth_age(
            datetime(birthdate.year, birthdate.month, birthdate.day, 23, 59)
        )
        assert actual == pytest.approx(
            4.0
        ), f"Expected an age of 4.0. Instead, it returned {actual}"

    def test_earth_age_fractional_years(self):
        """
        Verify the age keeps its fractional part (8210 days is 22.48 years).
        """
        actual = earth_age(days_ago(8210))
        assert actual == pytest.approx(
            22.48
        ), f"Expected an age of 22.48. Instead, it returned {actual}"
        assert actual != 22, f"Expected a fractional age. Instead, it returned {actual}"

    def test_earth_age_future_birthdate(self):
        """
        Verify a birthdate after today raises ValueError.
        """
        with pytest.raises(ValueError, match="future"):
            earth_age(date.today() + timedelta(days=1))
        with pytest.raises(ValueError, match="future"):
            earth_age("2999-01-01")

    def test_earth_age_impossible_dates(self):
        """
        Verify strings that are not real dates raise ValueError.
        """
        for impossible_date in ["2023-02-30", "2004-13-01", "2001-02-29", "hello", ""]:
            with pytest.raises(ValueError, match="not a real"):
                earth_age(impossible_date)

    def test_earth_age_wrong_type(self):
        """
        Verify a birthdate that is not a string or date raises TypeError.
        """
        for bad_birthdate_datatype in [20040517, 2004.5, None, True, ["2004-05-17"]]:
            with pytest.raises(TypeError):
                earth_age(bad_birthdate_datatype)

    def test_compare_planets_keys(self, monkeypatch):
        """
        Verify the result has one entry per planet, each with age and weight.
        """
        use_fakes(monkeypatch)
        actual = compare_planets("mars", "jupiter", days_ago(1461), 70)
        assert isinstance(
            actual, dict
        ), f"Expected compare_planets() to return a dict. Instead, it returned {actual}"
        assert list(actual) == [
            "mars",
            "jupiter",
        ], f"Expected keys ['mars', 'jupiter']. Instead, it returned {list(actual)}"
        for planet, stats in actual.items():
            assert set(stats) == {
                "age",
                "weight",
            }, f"Expected 'age' and 'weight' for {planet}. Instead, it returned {stats}"

    def test_compare_planets_passes_correct_values(self, monkeypatch):
        """
        Verify each planet gets the Earth age, the weight and weight mode "w".
        """
        use_fakes(monkeypatch)
        actual = compare_planets("venus", "saturn", days_ago(1461), 70)
        expected = {
            "venus": {"age": (4.0, "venus"), "weight": ("w", 70, "venus")},
            "saturn": {"age": (4.0, "saturn"), "weight": ("w", 70, "saturn")},
        }
        assert actual == expected, f"Expected {expected}. Instead, it returned {actual}"

    def test_compare_planets_mixed_case_names(self, monkeypatch):
        """
        Verify planet names are not case-sensitive and come back lowercased.
        """
        use_fakes(monkeypatch)
        actual = compare_planets("MARS", "Earth", days_ago(1461), 70)
        assert list(actual) == [
            "mars",
            "earth",
        ], f"Expected keys ['mars', 'earth']. Instead, it returned {list(actual)}"
        assert actual["mars"]["age"] == (
            4.0,
            "mars",
        ), f"Expected the lowercased name to be passed on. Instead, it returned {actual}"

    def test_compare_planets_zero_weight(self, monkeypatch):
        """
        Verify a weight of 0 is allowed and passed on unchanged.
        """
        use_fakes(monkeypatch)
        actual = compare_planets("moon", "neptune", days_ago(1461), 0)
        assert actual["moon"]["weight"] == (
            "w",
            0,
            "moon",
        ), f"Expected a weight of 0 to be passed on. Instead, it returned {actual}"

    def test_compare_planets_unknown_planet(self):
        """
        Verify an unknown planet in either position raises ValueError.
        """
        with pytest.raises(ValueError, match="pluto"):
            compare_planets("pluto", "mars", "2004-05-17", 70)
        with pytest.raises(ValueError, match="pluto"):
            compare_planets("mars", "Pluto", "2004-05-17", 70)
        with pytest.raises(ValueError, match="not a known planet"):
            compare_planets("", "mars", "2004-05-17", 70)

    def test_compare_planets_same_planet(self):
        """
        Verify the same planet twice raises ValueError, whatever the case.
        """
        with pytest.raises(ValueError, match="different"):
            compare_planets("mars", "mars", "2004-05-17", 70)
        with pytest.raises(ValueError, match="different"):
            compare_planets("mars", "MARS", "2004-05-17", 70)

    def test_compare_planets_negative_weight(self):
        """
        Verify a negative weight raises ValueError.
        """
        with pytest.raises(ValueError, match="negative"):
            compare_planets("mars", "venus", "2004-05-17", -1)
        with pytest.raises(ValueError, match="negative"):
            compare_planets("mars", "venus", "2004-05-17", -0.5)

    def test_compare_planets_wrong_planet_type(self):
        """
        Verify a planet that is not a string raises TypeError.
        """
        for bad_planet in [3, None, True, ["mars"]]:
            with pytest.raises(TypeError):
                compare_planets(bad_planet, "venus", "2004-05-17", 70)
            with pytest.raises(TypeError):
                compare_planets("venus", bad_planet, "2004-05-17", 70)

    def test_compare_planets_wrong_weight_type(self):
        """
        Verify a weight that is not a number, including a bool, raises TypeError.
        """
        for bad_weight in ["70", None, True, False, [70]]:
            with pytest.raises(TypeError):
                compare_planets("mars", "venus", "2004-05-17", bad_weight)

    def test_compare_planets_bad_birthdate(self):
        """
        Verify birthdate errors from earth_age reach the caller.
        """
        with pytest.raises(ValueError):
            compare_planets("mars", "venus", "2023-02-30", 70)
        with pytest.raises(ValueError):
            compare_planets("mars", "venus", "2999-01-01", 70)
        with pytest.raises(TypeError):
            compare_planets("mars", "venus", None, 70)

    def test_compare_planets_with_real_functions(self):
        """
        Integration check: use the real age and weight functions, not fakes.
        """
        actual = compare_planets("Mars", "jupiter", days_ago(8210), 70)
        expected = {
            "mars": {"age": 11.95, "weight": 26.43},
            "jupiter": {"age": 1.9, "weight": 165.0},
        }
        assert actual == expected, f"Expected {expected}. Instead, it returned {actual}"
