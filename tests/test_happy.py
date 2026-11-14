"""Tests for the pet's happiness stat."""

import pytest

from package.happy import decrease_happiness, increase_happiness, play
from package.pet import MAX_STAT


def make_pet():
    return {
        "hunger": 20,
        "energy": 80,
        "hygiene": 80,
        "happiness": 80,
        "health": 50,
        "alive": True,
    }


# increase_happiness
@pytest.mark.parametrize(
    ("start", "change", "expected"),
    [
        (0, 0, 0),
        (0, 10, 10),
        (80, 15, 95),
        (90, MAX_STAT, MAX_STAT),
    ],
)
def test_increase_happiness_zero_typical_and_clamped(start, change, expected):
    pet = make_pet()
    pet["happiness"] = start

    assert increase_happiness(pet, change) == expected
    assert pet["happiness"] == expected


@pytest.mark.parametrize(
    ("change", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (None, TypeError),
        (-1, ValueError),
        ("3", TypeError),
    ],
)
def test_increase_happiness_invalid_change(change, error):
    pet = make_pet()

    with pytest.raises(error):
        increase_happiness(pet, change)


@pytest.mark.parametrize(
    ("value", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        ("80", TypeError),
        (True, TypeError),
        (50.5, TypeError),
    ],
)
def test_increase_happiness_invalid_stat(value, error):
    pet = make_pet()
    pet["happiness"] = value

    with pytest.raises(error):
        increase_happiness(pet, 5)


def test_increase_happiness_missing_stat():
    pet = make_pet()
    del pet["happiness"]

    with pytest.raises(TypeError):
        increase_happiness(pet, 5)


# decrease_happiness
@pytest.mark.parametrize(
    ("start", "expected"),
    [
        (MAX_STAT, MAX_STAT - 10),
        (80, 65),
        (5, 0),
        (0, 0),
    ],
)
def test_decrease_happiness_zero_typical_and_clamped(start, expected):
    pet = make_pet()
    pet["happiness"] = start

    assert decrease_happiness(pet) == expected
    assert pet["happiness"] == expected


@pytest.mark.parametrize(
    ("value", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        ("80", TypeError),
        (True, TypeError),
        (50.5, TypeError),
    ],
)
def test_decrease_happiness_invalid_stat(value, error):
    pet = make_pet()
    pet["happiness"] = value

    with pytest.raises(error):
        decrease_happiness(pet)


def test_decrease_happiness_missing_stat():
    pet = make_pet()
    del pet["happiness"]

    with pytest.raises(TypeError):
        decrease_happiness(pet)


# play
@pytest.mark.parametrize(
    ("play_type", "gain", "message"),
    [
        ("1", 15, "You pet Mochi, they love it!"),
        (
            "2",
            10,
            "You throw a ball to Mochi, they catch it and happily bring it back to you!",
        ),
        ("3", 5, "You take Mochi on a walk, they smile the entire time!"),
    ],
)
def test_play_increases_happiness(play_type, gain, message):
    pet = make_pet()
    pet["happiness"] = 0

    result = play(pet, "Mochi", play_type)

    assert message in result
    assert pet["happiness"] == gain


def test_play_clamped():
    pet = make_pet()
    pet["happiness"] = MAX_STAT - 1

    play(pet, "Mochi", "1")

    assert pet["happiness"] == MAX_STAT


@pytest.mark.parametrize("play_type", ["0", "4", "pet", "", None, 1])
def test_play_invalid_play_type(play_type):
    pet = make_pet()
    original = pet.copy()

    result = play(pet, "Mochi", play_type)

    assert "not a valid play type" in result
    assert pet == original
