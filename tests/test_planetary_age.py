import pytest
from cosmicly.planetary_age import age_on_planet


def test_value_age_function():
    assert age_on_planet(20, "earth") == 20.0
    assert age_on_planet(20, "mercury") == 83.0
    assert age_on_planet(20, "mars") == 10.63
    assert age_on_planet(20, "jupiter") == 1.69
    assert age_on_planet(20, "moon") == 20.0
    assert age_on_planet(0, "mars") == 0.0


def test_age_type():
    assert age_on_planet(20, "earth") == 20.0
    assert age_on_planet(20.5, "earth") == 20.5
    assert age_on_planet(10, "earth") == 10.0
    assert age_on_planet(0, "earth") == 0.0


def test_unknown_planet():
    with pytest.raises(ValueError):
        age_on_planet(20, "pluto")
    with pytest.raises(ValueError):
        age_on_planet(20, "a2-18b")
    with pytest.raises(ValueError):
        age_on_planet(20, "")
    with pytest.raises(TypeError):
        age_on_planet(20, 111)
    with pytest.raises(TypeError):
        age_on_planet(20, None)


def test_wrong_age():
    with pytest.raises(ValueError):
        age_on_planet(-5, "mars")
    with pytest.raises(TypeError):
        age_on_planet("20", "mars")
    with pytest.raises(TypeError):
        age_on_planet(None, "mars")
    with pytest.raises(TypeError):
        age_on_planet(True, "mars")
    with pytest.raises(TypeError):
        age_on_planet([20], "mars")


def test_planet_name():
    assert age_on_planet(20, "MARS") == 10.63
    assert age_on_planet(20, "Mars") == 10.63
    assert age_on_planet(20, "MArS") == 10.63
    assert age_on_planet(20, "EARTH") == 20.0
    assert age_on_planet(20, "Moon") == 20.0


def test_zero_age():
    assert age_on_planet(0, "earth") == 0.0
    assert age_on_planet(0, "mars") == 0.0
    assert age_on_planet(0, "mercury") == 0.0
    assert age_on_planet(0, "moon") == 0.0
