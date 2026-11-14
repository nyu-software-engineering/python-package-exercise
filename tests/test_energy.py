
import pytest

from package.energy import drain_energy, restore_energy
from package.pet import create_pet


@pytest.mark.parametrize(
    ("start", "amount", "expected"),
    [
        (50, 0, 50),
        (50, 10, 40),
        (50, 25, 25),
        (50, 50, 0),
        (50, 100, 0),
        (5, 10, 0),
        (100, 10, 90),
    ],
)
def test_drain_energy_normal_and_boundaries(start, amount, expected):
    pet = create_pet("Mochi")
    pet["energy"] = start

    assert drain_energy(pet, amount) == expected
    assert pet["energy"] == expected


def test_restore_energy_default():
    pet = create_pet("Mochi")
    pet["energy"] = 50

    assert restore_energy(pet) == 70
    assert pet["energy"] == 70


@pytest.mark.parametrize(
    ("start", "amount", "expected"),
    [
        (50, 0, 50),
        (50, 10, 60),
        (50, 20, 70),
        (50, 50, 100),
        (90, 20, 100),
        (100, 20, 100),
        (0, 100, 100),
    ],
)
def test_restore_energy_normal_and_boundaries(start, amount, expected):
    pet = create_pet("Mochi")
    pet["energy"] = start

    assert restore_energy(pet, amount) == expected
    assert pet["energy"] == expected


@pytest.mark.parametrize(
    ("amount", "error"),
    [
        (-1, ValueError),
        (None, TypeError),
        (True, TypeError),
        (1.5, TypeError),
        ("10", TypeError),
    ],
)
def test_drain_energy_invalid_amount(amount, error):
    pet = create_pet("Mochi")

    with pytest.raises(error):
        drain_energy(pet, amount)


@pytest.mark.parametrize(
    ("amount", "error"),
    [
        (-1, ValueError),
        (None, TypeError),
        (True, TypeError),
        (1.5, TypeError),
        ("10", TypeError),
    ],
)
def test_restore_energy_invalid_amount(amount, error):
    pet = create_pet("Mochi")

    with pytest.raises(error):
        restore_energy(pet, amount)


@pytest.mark.parametrize(
    ("energy", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        (True, TypeError),
        ("50", TypeError),
        (50.5, TypeError),
    ],
)
def test_drain_energy_invalid_pet(energy, error):
    pet = {"energy": energy}

    with pytest.raises(error):
        drain_energy(pet, 10)


@pytest.mark.parametrize(
    ("energy", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        (True, TypeError),
        ("50", TypeError),
        (50.5, TypeError),
    ],
)
def test_restore_energy_invalid_pet(energy, error):
    pet = {"energy": energy}

    with pytest.raises(error):
        restore_energy(pet, 10)


def test_drain_energy_missing_stat():
    with pytest.raises(TypeError):
        drain_energy({}, 10)


def test_restore_energy_missing_stat():
    with pytest.raises(TypeError):
        restore_energy({}, 10)


def test_drain_energy_records_history():
    pet = create_pet("Mochi")
    pet["energy"] = 50

    drain_energy(pet, 10)

    assert len(pet["history"]) == 1
    event = pet["history"][0]

    assert event["action"] == "stat"
    assert event["stat"] == "energy"
    assert event["before"] == 50
    assert event["after"] == 40


def test_restore_energy_records_history():
    pet = create_pet("Mochi")
    pet["energy"] = 50

    restore_energy(pet, 20)

    assert len(pet["history"]) == 1
    event = pet["history"][0]

    assert event["action"] == "stat"
    assert event["stat"] == "energy"
    assert event["before"] == 50
    assert event["after"] == 70


def test_no_history_when_energy_unchanged():
    pet = create_pet("Mochi")

    drain_energy(pet, 0)
    restore_energy(pet, 20)

    assert pet["energy"] == 100
    assert pet["history"] == []


def test_drain_and_restore_together():
    pet = create_pet("Mochi")
    pet["energy"] = 80

    drain_energy(pet, 30)
    assert pet["energy"] == 50

    restore_energy(pet, 20)
    assert pet["energy"] == 70

    assert len(pet["history"]) == 2
