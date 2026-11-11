"""Tests for weight calculations on Earth, Mars, and the Moon."""

import pytest
from cosmicly.planetary_weight import weight_on_planet


def test_value_weight_function():
    """Verify expected results in weight and mass modes for Earth, Mars, and the Moon."""
    actual = weight_on_planet("w", 70, "earth")
    assert actual == 70.0, f"Expected 70.0. Instead, it returned {actual}"
    actual = weight_on_planet("w", 70, "mars")
    assert actual == 26.43, f"Expected 26.43. Instead, it returned {actual}"
    actual = weight_on_planet("w", 70, "moon")
    assert actual == 11.43, f"Expected 11.43. Instead, it returned {actual}"

    actual = weight_on_planet("m", 70, "earth")
    assert actual == 686.0, f"Expected 686.0. Instead, it returned {actual}"
    actual = weight_on_planet("m", 70, "mars")
    assert actual == 259.0, f"Expected 259.0. Instead, it returned {actual}"
    actual = weight_on_planet("m", 70, "moon")
    assert actual == 112.0, f"Expected 112.0. Instead, it returned {actual}"


def test_type_weight_function():
    """Verify case-insensitive mode aliases and zero inputs in both modes."""
    for mode in ["w", "weight", "Weight", "WeIGhT", "W"]:
        actual = weight_on_planet(mode, 70, "earth")
        assert actual == 70.0, f"Expected 70.0 for mode {mode!r}. Instead, it returned {actual}"

    for mode in ["m", "M", "Mass", "mass", "MASS"]:
        actual = weight_on_planet(mode, 70, "earth")
        assert actual == 686.0, f"Expected 686.0 for mode {mode!r}. Instead, it returned {actual}"

    for mode in ["w", "m"]:
        for planet in ["mars", "earth"]:
            actual = weight_on_planet(mode, 0, planet)
            assert actual == 0.0, f"Expected 0.0 on {planet} in mode {mode!r}. Instead, it returned {actual}"


def test_unknown_planet():
    """Verify that unknown planet names raise ValueError and non-string names raise TypeError."""
    with pytest.raises(ValueError):
        weight_on_planet("w", 70, "pluto")
    with pytest.raises(ValueError):
        weight_on_planet("w", 70, "a2-18b")
    with pytest.raises(TypeError):
        weight_on_planet("w", 70, 111)


def test_unknown_type():
    """Verify that invalid mode names raise ValueError."""
    with pytest.raises(ValueError):
        weight_on_planet("a", 70, "mars")
    with pytest.raises(ValueError):
        weight_on_planet("mas", 70, "mars")
    with pytest.raises(ValueError):
        weight_on_planet("ww", 70, "mars")


def test_mode_not_a_string():
    """Verify that a mode that is not a string raises TypeError."""
    with pytest.raises(TypeError):
        weight_on_planet(5, 70, "mars")
    with pytest.raises(TypeError):
        weight_on_planet(None, 70, "mars")
    with pytest.raises(TypeError):
        weight_on_planet(["w"], 70, "mars")


def test_wrong_value():
    """Verify that negative values raise ValueError and non-numeric values raise TypeError."""
    with pytest.raises(ValueError):
        weight_on_planet("w", -5, "mars")
    with pytest.raises(TypeError):
        weight_on_planet("w", "70", "mars")
    with pytest.raises(TypeError):
        weight_on_planet("w", None, "mars")
    with pytest.raises(TypeError):
        weight_on_planet("w", True, "mars")


def test_planet_name():
    """Verify that different capitalizations of Mars return the same weight."""
    for planet in ["MARS", "Mars", "MArS"]:
        actual = weight_on_planet("w", 70, planet)
        assert actual == 26.43, f"Expected 26.43 for {planet!r}. Instead, it returned {actual}"
