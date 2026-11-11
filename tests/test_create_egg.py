import pytest

#from create_egg import create_egg

#from get_stage import get_stage
from terminal_pet_respin import create_egg, get_stage



def test_default_egg():

    pet = create_egg("Bob")

    assert pet["name"] == "Bob"

    assert pet["hatch_at"] == 50

    assert pet["commands_run"] == 0

    assert pet["stage"] == "egg"


@pytest.mark.parametrize("threshold", [1, 20, 100])

def test_custom_threshold(threshold):

    pet = create_egg("Lucy", threshold)


    assert pet["hatch_at"] == threshold
    
    assert pet["stage"] == get_stage(pet["commands_run"], pet["hatch_at"])


def test_name_whitespace():

    pet = create_egg("  Bob  ")

    assert pet["name"] == "Bob"


@pytest.mark.parametrize("name", ["", "   ", "\t\n"])

def test_empty_name(name):

    with pytest.raises(ValueError):

        create_egg(name)


@pytest.mark.parametrize("name", [None, 123, True, []])

def test_invalid_name_type(name):

    with pytest.raises(TypeError):

        create_egg(name)


@pytest.mark.parametrize("threshold", [0, -1, -50])

def test_nonpositive_threshold(threshold):

    with pytest.raises(ValueError):

        create_egg("Bob", threshold)


@pytest.mark.parametrize("threshold", [True, False, 1.5, "50", None])

def test_invalid_threshold_type(threshold):

    with pytest.raises(TypeError):

        create_egg("Bob", threshold)


def test_eggs_are_independent():

    first = create_egg("Bob")

    second = create_egg("Lucy")

    first["commands_run"] = 10

    assert second["commands_run"] == 0

    assert second["name"] == "Lucy"