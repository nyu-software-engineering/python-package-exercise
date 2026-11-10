import pytest
from desktop_cat import Cat

# Test that sleeping reduces sleepiness
def test_sleep_reduces_sleepiness():
    cat = Cat()
    cat.sleepiness = 8

    text = cat.sleep(2)

    assert cat.sleepiness == 4
    assert isinstance(text, str)

# Test that sleepiness cannot go below 0
def test_sleep_cannot_go_below_0():
    cat = Cat()
    cat.sleepiness = 3

    text = cat.sleep(10)

    assert cat.sleepiness == 0
    assert cat.mood == "happy"
    assert "hours and is fully rested!" in text

# Test that sleeping doesn't work when already at 0 sleepiness
def test_sleep_when_already_rested():
    cat = Cat()
    cat.sleepiness = 0

    text = cat.sleep(8)

    assert cat.sleepiness == 0
    assert "is already fully rested." in text

# Test that invalid types don't work
def test_sleep_invalid_types():
    cat = Cat()

    for hours in (True, False, 1.5, "2", None):
        with pytest.raises(TypeError):
            cat.sleep(hours)

# Test that invalid values don't work
def test_sleep_invalid_values():
    cat = Cat()

    for hours in (0, -1):
        with pytest.raises(ValueError):
            cat.sleep(hours)

    assert cat.sleepiness == 5