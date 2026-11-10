"""Tests for weight calculations on Earth, Mars, and the Moon."""

import pytest
from cosmicly.planetary_weight import weight_on_planet


def test_value_weight_function():
    """Verify expected results in weight and mass modes for Earth, Mars, and the Moon."""
    assert weight_on_planet("w", 70, "earth") == 70.0
    assert weight_on_planet("w", 70, "mars") == 26.43
    assert weight_on_planet("w", 70, "moon") == 11.43

    assert weight_on_planet("m", 70, "earth") == 686.0
    assert weight_on_planet("m", 70, "mars") == 259.0
    assert weight_on_planet("m", 70, "moon") == 112.0


def test_type_weight_function():
    """Verify case-insensitive mode aliases and zero inputs in both modes."""
    assert weight_on_planet("w", 70, "earth") == 70.0
    assert weight_on_planet("weight", 70, "earth") == 70.0
    assert weight_on_planet("Weight", 70, "earth") == 70.0
    assert weight_on_planet("WeIGhT", 70, "earth") == 70.0
    assert weight_on_planet("W", 70, "earth") == 70.0

    assert weight_on_planet("m", 70, "earth") == 686.0
    assert weight_on_planet("M", 70, "earth") == 686.0
    assert weight_on_planet("Mass", 70, "earth") == 686.0
    assert weight_on_planet("mass", 70, "earth") == 686.0
    assert weight_on_planet("MASS", 70, "earth") == 686.0

    assert weight_on_planet("w", 0, "mars") == 0.0
    assert weight_on_planet("w", 0, "earth") == 0.0
    assert weight_on_planet("m", 0, "mars") == 0.0
    assert weight_on_planet("m", 0, "earth") == 0.0


def test_unknown_planet():
    """Verify that unknown planet names raise ValueError and non-string names raise TypeError."""
    with pytest.raises(ValueError):
        weight_on_planet("w", 70, "pluto")
    with pytest.raises(ValueError):
        weight_on_planet("w", 70, "a2-18b")
    with pytest.raises(TypeError):
        weight_on_planet("w", 70, 111)


def test_unknown_type():
    """Verify that calls with invalid mode names and an unknown planet raise ValueError."""
    with pytest.raises(ValueError):
        weight_on_planet("a", 70, "pluto")
    with pytest.raises(ValueError):
        weight_on_planet("mas", 70, "pluto")
    with pytest.raises(ValueError):
        weight_on_planet("ww", 70, "pluto")


def test_wrong_value():
    """Verify that negative values raise ValueError and non-numeric values raise TypeError."""
    with pytest.raises(ValueError):
        weight_on_planet("w", -5, "mars")
    with pytest.raises(TypeError):
        weight_on_planet("w", "70", "mars")
    with pytest.raises(TypeError):
        weight_on_planet("w", None, "mars")


def test_planet_name():
    """Verify that different capitalizations of Mars return the same weight."""
    assert weight_on_planet("w", 70, "MARS") == 26.43
    assert weight_on_planet("w", 70, "Mars") == 26.43
    assert weight_on_planet("w", 70, "MArS") == 26.43
