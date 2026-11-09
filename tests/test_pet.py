import pytest 
from desktop_cat import Cat

# Test that head, back, and tail pets below threshold make mood happy
def test_head_below_threshold_makes_happy():
    cat = Cat()

    cat.mood = "sad"
    reaction = cat.pet("head", 2)
    assert cat.mood == "happy"
    assert reaction == f"{cat.name} purrs and enjoys the head pets."

    cat.mood = "sad"
    reaction = cat.pet("back", 2)
    assert cat.mood == "happy"
    assert reaction == f"{cat.name} purrs and enjoys the back pets."

    cat.mood = "sad"
    reaction = cat.pet("tail", 2)
    assert cat.mood == "happy"
    assert reaction == f"{cat.name} purrs and enjoys the tail pets."

# Test that belly, paws pets below threshold make mood happy
def test_belly_below_threshold_makes_happy():
    cat = Cat()

    cat.mood = "sad"
    reaction = cat.pet("belly", 2)
    assert cat.mood == "happy"
    assert reaction == f"{cat.name} lets you pet its belly."

    cat.mood = "sad"
    reaction = cat.pet("paws", 2)
    assert cat.mood == "happy"
    assert reaction == f"{cat.name} lets you pet its paws."


# Test that pets above threshold make mood annoyed, if not already annoyed
def test_pets_above_threshold_annoyed():
    cat = Cat()

    cat.mood = "happy"
    reaction = cat.pet("belly", 5)
    assert cat.mood == "annoyed"
    assert reaction == f"{cat.name} gets annoyed when you pet its belly."

    cat.mood = "happy"
    reaction = cat.pet("head", 10)
    assert cat.mood == "annoyed"
    assert reaction == f"{cat.name} gets tired of being pet on its head."


# Test that pets above threshold make mood angry, if annoyed
def test_annoyed_becomes_angry():
    cat = Cat()

    cat.mood = "annoyed"
    reaction = cat.pet("belly", 5)
    assert cat.mood == "angry"
    assert reaction == f"{cat.name} is angry after being bothered so much!"

    cat.mood = "annoyed"
    reaction = cat.pet("head", 10)
    assert cat.mood == "angry"
    assert reaction == f"{cat.name} is angry after being bothered so much!"

# Test that invalid areas raise error
def test_invalid_areas_raise_error():
    cat = Cat()
    start_times_petted = cat.times_petted
    start_mood = cat.mood

    with pytest.raises(ValueError) as error:
        cat.pet("ears", 1)
    assert str(error.value) == "Invalid petting area: ears"
    assert cat.times_petted == start_times_petted 
    assert cat.mood == start_mood


# Test that times_petted increases correctly
def test_times_petted_increase():
    cat = Cat()
    start_times_petted = cat.times_petted
    cat.pet("head", 3)
    assert cat.times_petted == start_times_petted + 3

# Test that text inputs are normalized
def test_area_normalized():
    cat = Cat()
    cat.mood = "sad"
    reaction = cat.pet(" Head", 2)

    assert cat.mood == "happy"
    assert reaction == f"{cat.name} purrs and enjoys the head pets."

# Test that times = 0 or negative number of times raises error
def test_negative_zero_times_error():
    cat = Cat()

    with pytest.raises(ValueError) as error:
        cat.pet("head", 0)
    assert str(error.value) == "Times must be greater than 0"

    with pytest.raises(ValueError) as error:
        cat.pet("head", -2)
    assert str(error.value) == "Times must be greater than 0"
    assert cat.times_petted == 0
