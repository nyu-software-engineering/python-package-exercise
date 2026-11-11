import pytest

from package.health import wellness, update_health
from package.pet import STATS


def make_pet():
    return {
        "hunger": 20,
        "energy": 80,
        "hygiene": 80,
        "happiness": 80,
        "health": 50,
        "alive": True,
    }


@pytest.mark.parametrize(
    ("hunger", "energy", "hygiene", "happiness", "expected"),
    [
        (0, 100, 100, 100, 100),
        (100, 0, 0, 0, 0),
        (20, 80, 80, 80, 80),
        (60, 40, 60, 80, 55),
        (50, 50, 50, 50, 50),
    ],
)
def test_wellness_values(hunger, energy, hygiene, happiness, expected):
    pet = make_pet()
    pet.update({
        "hunger": hunger,
        "energy": energy,
        "hygiene": hygiene,
        "happiness": happiness,
    })
    original = pet.copy()

    assert wellness(pet) == expected
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

    assert update_health(pet) == 52
    assert update_health(pet, 3) == 58


def test_update_health_clamped():
    pet = make_pet()
    pet["health"] = 99

    assert update_health(pet, 5) == 100


def test_update_health_unhealthy():
    pet = make_pet()
    pet.update({
        "hunger": 100,
        "energy": 20,
        "hygiene": 20,
        "happiness": 20,
    })

    assert wellness(pet) == 15
    assert update_health(pet) == 43
    assert update_health(pet, 3) == 22


def test_update_health_wellness_boundary():
    pet = make_pet()
    pet.update({
        "hunger": 50,
        "energy": 50,
        "hygiene": 50,
        "happiness": 50,
    })

    assert wellness(pet) == 50
    assert update_health(pet, 3) == 50


def test_update_health_below_healthy_threshold():
    pet = make_pet()
    pet["hunger"] = 41
    pet["energy"] = 60
    pet["hygiene"] = 60
    pet["happiness"] = 60

    assert update_health(pet) == 50


def test_update_health_death_and_stops():
    pet = make_pet()
    pet.update({
        "hunger": 100,
        "energy": 0,
        "hygiene": 0,
        "happiness": 0,
        "health": 18,
    })

    assert update_health(pet, 10) == 8
    assert pet["alive"] is False
    assert update_health(pet, 5) == 8


def test_update_health_exact_death_threshold():
    pet = make_pet()
    pet.update({
        "hunger": 100,
        "energy": 30,
        "hygiene": 30,
        "happiness": 40,
        "health": 15,
    })

    assert update_health(pet) == 10
    assert pet["alive"] is False


def test_update_health_zero_ticks_and_dead_pet():
    pet = make_pet()

    assert update_health(pet, 0) == 50

    pet["alive"] = False
    assert update_health(pet, 5) == 50


def test_update_health_missing_alive():
    pet = make_pet()
    del pet["alive"]

    assert update_health(pet) == 52


@pytest.mark.parametrize(
    ("ticks", "error"),
    [
        (-1, ValueError),
        (None, TypeError),
        (True, TypeError),
        (1.5, TypeError),
        ("3", TypeError),
    ],
)
def test_update_health_invalid_ticks(ticks, error):
    with pytest.raises(error):
        update_health(make_pet(), ticks)


@pytest.mark.parametrize(
    ("stat", "value", "error"),
    [
        ("hunger", -1, ValueError),
        ("energy", 101, ValueError),
        ("hygiene", None, TypeError),
        ("happiness", "80", TypeError),
        ("health", True, TypeError),
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
