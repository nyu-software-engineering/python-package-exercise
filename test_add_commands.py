import pytest

from add_commands import add_commands
from create_egg import create_egg


def test_default_count():
    pet = create_egg("Bob")
    result = add_commands(pet)
    assert result["commands_run"] == 1
    assert result["stage"] == "egg"
    assert result is pet


@pytest.mark.parametrize(
    "count, expected_stage",
    [
        (4, "egg"),
        (5, "cracking"),
        (10, "hatchling"),
        (20, "young python"),
        (40, "full python"),
    ],
)
def test_stage_updates(count, expected_stage):
    pet = create_egg("Lucy", 10)
    add_commands(pet, count)
    assert pet["commands_run"] == count
    assert pet["stage"] == expected_stage


def test_counts_add_up():
    pet = create_egg("Bob", 10)
    add_commands(pet, 3)
    add_commands(pet, 2)
    assert pet["commands_run"] == 5
    assert pet["stage"] == "cracking"


def test_other_keys_unchanged():
    pet = create_egg("Bob", 10)
    add_commands(pet, 7)
    assert pet["name"] == "Bob"
    assert pet["hatch_at"] == 10