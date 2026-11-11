import pytest

from package.history import get_history
from package.pet import create_pet
from package.time_passed import apply_time


def test_two_minutes_changes_hunger_and_energy():
    pet = create_pet("Mochi")
    pet["hunger"] = 10
    pet["energy"] = 50
    pet["last_seen"] = 1000

    assert apply_time(pet, now=1120) == 2
    assert pet["hunger"] == 12
    assert pet["energy"] == 48
    assert pet["last_seen"] == 1120
    assert [event["stat"] for event in get_history(pet, 5)] == ["hunger", "energy"]


def test_less_than_a_minute_changes_nothing():
    pet = create_pet("Mochi")
    pet["last_seen"] = 1000

    assert apply_time(pet, now=1050) == 0
    assert pet["hunger"] == 0
    assert pet["energy"] == 100
    assert get_history(pet, 5) == []
    assert pet["last_seen"] == 1050


def test_missing_last_seen_starts_the_clock():
    pet = create_pet("Mochi")

    assert apply_time(pet, now=5000) == 0
    assert pet["last_seen"] == 5000
    assert pet["hunger"] == 0
    assert pet["energy"] == 100


def test_stats_stop_at_the_limits():
    pet = create_pet("Mochi")
    pet["hunger"] = 99
    pet["energy"] = 1
    pet["last_seen"] = 0

    assert apply_time(pet, now=180) == 3
    assert pet["hunger"] == 100
    assert pet["energy"] == 0


def test_apply_time_rejects_a_bad_clock():
    pet = create_pet("Mochi")
    pet["last_seen"] = 1000

    with pytest.raises(TypeError):
        apply_time(pet, now=True)
    with pytest.raises(TypeError):
        apply_time(pet, now=1.5)