import pytest
from desktop_cat import Cat, MOODS

# Makes sure custom attributes are allowed
def test_new_cat_valid_custom_attributes():
    cat = Cat(name="Mochi", mood="sad")
    assert cat.name == "Mochi"
    assert cat.mood == "sad"

# Tests that names are properly stripped before being saved
def test_new_cat_normalizes_attributes():
    cat = Cat(name="  Mochi  ", mood=" HAPPY ")
    assert cat.name == "Mochi"
    assert cat.mood == "happy"

# Tests that invalid name types don't work (integer instead of string)
def test_new_cat_invalid_name_type():
    with pytest.raises(TypeError):
        Cat(name=123)

# Tests that an empty name will result in a ValueError
def test_new_cat_empty_name():
    with pytest.raises(ValueError):
        Cat(name="   ")

# Tests that an overly long name will result in a ValueError
def test_new_cat_name_too_long():
    with pytest.raises(ValueError):
        Cat(name="a" * 21)

# Tests that invalid mood types don't work (integer instead of string)
def test_new_cat_invalid_mood_type():
    with pytest.raises(TypeError):
        Cat(mood=123)

# Tests that moods not in the MOODS list result in a ValueError
def test_new_cat_invalid_mood():
    with pytest.raises(ValueError):
        Cat(mood="excited")

# Tests default Cat instance attributes
def test_new_cat_defaults():
    cat = Cat()
    assert cat.name == "Whiskers"
    assert cat.mood == "happy"
    assert cat.mood in MOODS
    assert cat.hunger == 5
    assert cat.sleepiness == 5
    assert cat.times_petted == 0
    assert cat.foods_eaten == {}
    assert cat.last_action == "idle"