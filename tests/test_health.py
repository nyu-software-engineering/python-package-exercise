import pytest

from package.health import (
    wellness,
    update_health,
    HEALTHY_STAT,
    HEALTHY_HUNGER,
    SICK_WELLNESS,
    DEATH_HEALTH,
)
from package.pet import MAX_STAT, STATS


def make_pet():
    """Create a valid pet for health tests."""
    return {
        "hunger": 20,
        "energy": 80,
        "hygiene": 80,
        "happiness": 80,
        "health": 50,
        "alive": True,
    }


def test_wellness_healthy_pet():
    pet = make_pet()

    assert wellness(pet) == 80


def test_wellness_perfect_and_unhealthy():
    pet = make_pet()
    pet["hunger"] = 0
    pet["energy"] = MAX_STAT
    pet["hygiene"] = MAX_STAT
    pet["happiness"] = MAX_STAT

    assert wellness(pet) == MAX_STAT

    pet["hunger"] = MAX_STAT
    pet["energy"] = 0
    pet["hygiene"] = 0
    pet["happiness"] = 0

    assert wellness(pet) == 0


def test_wellness_mixed_stats():
    pet = make_pet()
    pet["hunger"] = 60
    pet["energy"] = 40
    pet["hygiene"] = 60
    pet["happiness"] = 80

    assert wellness(pet) == 55


def test_wellness_does_not_modify_pet():
    pet = make_pet()
    original = pet.copy()

    wellness(pet)

    assert pet == original


@pytest.mark.parametrize(
    ("stat", "value", "error"),
    [
        ("hunger", -1, ValueError),
        ("energy", 101, ValueError),
        ("hygiene", None, TypeError),
        ("happiness", "80", TypeError),
        ("health", True, TypeError),
        ("energy", 50.5, TypeError),
    ],
)
def test_wellness_invalid_stats(stat, value, error):
    pet = make_pet()
    pet[stat] = value

    with pytest.raises(error):
        wellness(pet)


@pytest.mark.parametrize("stat", STATS)
def test_wellness_missing_stats(stat):
    pet = make_pet()
    del pet[stat]

    with pytest.raises(TypeError):
        wellness(pet)


def test_update_health_regeneration():
    pet = make_pet()
    pet["hunger"] = HEALTHY_HUNGER
    pet["energy"] = HEALTHY_STAT
    pet["hygiene"] = HEALTHY_STAT
    pet["happiness"] = HEALTHY_STAT

    assert update_health(pet) == 52
    assert update_health(pet, 3) == 58


def test_update_health_max_and_clamped():
    pet = make_pet()
    pet["hunger"] = 0
    pet["energy"] = MAX_STAT
    pet["hygiene"] = MAX_STAT
    pet["happiness"] = MAX_STAT
    pet["health"] = 99

    assert update_health(pet, 5) == MAX_STAT


def test_update_health_unhealthy():
    pet = make_pet()
    pet["hunger"] = 100
    pet["energy"] = 20
    pet["hygiene"] = 20
    pet["happiness"] = 20

    assert wellness(pet) == 15
    assert update_health(pet) == 43
    assert update_health(pet, 3) == 22


def test_update_health_wellness_boundary():
    pet = make_pet()
    pet["hunger"] = 50
    pet["energy"] = 50
    pet["hygiene"] = 50
    pet["happiness"] = 50

    assert wellness(pet) == SICK_WELLNESS
    assert update_health(pet) == 50
    assert update_health(pet, 3) == 50


def test_update_health_below_healthy_threshold():
    pet = make_pet()
    pet["hunger"] = HEALTHY_HUNGER + 1
    pet["energy"] = HEALTHY_STAT
    pet["hygiene"] = HEALTHY_STAT
    pet["happiness"] = HEALTHY_STAT

    assert update_health(pet) == 50

    pet["hunger"] = HEALTHY_HUNGER
    pet["energy"] = HEALTHY_STAT - 1

    assert update_health(pet) == 50


def test_update_health_death():
    pet = make_pet()
    pet["hunger"] = 100
    pet["energy"] = 0
    pet["hygiene"] = 0
    pet["happiness"] = 0
    pet["health"] = 15

    assert update_health(pet) == 5
    assert pet["alive"] is False


def test_update_health_exact_death_threshold():
    pet = make_pet()
    pet["hunger"] = 100
    pet["energy"] = 30
    pet["hygiene"] = 30
    pet["happiness"] = 40
    pet["health"] = 15

    assert wellness(pet) == 25
    assert update_health(pet) == DEATH_HEALTH
    assert pet["alive"] is False


def test_update_health_stops_after_death():
    pet = make_pet()
    pet["hunger"] = 100
    pet["energy"] = 0
    pet["hygiene"] = 0
    pet["happiness"] = 0
    pet["health"] = 18

    assert update_health(pet, 10) == 8
    assert pet["alive"] is False


def test_update_health_dead_pet():
    pet = make_pet()
    pet["health"] = DEATH_HEALTH
    pet["alive"] = False

    assert update_health(pet, 5) == DEATH_HEALTH
    assert pet["alive"] is False


def test_update_health_zero_ticks():
    pet = make_pet()

    assert update_health(pet, 0) == 50


def test_update_health_missing_alive():
    pet = make_pet()
    del pet["alive"]

    assert update_health(pet) == 52
    assert pet["health"] == 52


@pytest.mark.parametrize(
    ("count", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (None, TypeError),
        (-1, ValueError),
        ("3", TypeError),
    ],
)
def test_update_health_invalid_ticks(count, error):
    pet = make_pet()

    with pytest.raises(error):
        update_health(pet, count)


@pytest.mark.parametrize(
    ("stat", "value", "error"),
    [
        ("hunger", -1, ValueError),
        ("energy", 101, ValueError),
        ("hygiene", None, TypeError),
        ("happiness", "80", TypeError),
        ("health", True, TypeError),
        ("health", 50.5, TypeError),
    ],
)
def test_update_health_invalid_stats(stat, value, error):
    pet = make_pet()
    pet[stat] = value

    with pytest.raises(error):
        update_health(pet)


@pytest.mark.parametrize("stat", STATS)
def test_update_health_missing_stats(stat):
    pet = make_pet()
    del pet[stat]

    with pytest.raises(TypeError):
        update_health(pet)


def test_update_health_updates_pet():
    pet = make_pet()

    result = update_health(pet, 2)

    assert pet["health"] == result
    assert pet["health"] == 54
