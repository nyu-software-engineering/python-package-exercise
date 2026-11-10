import pytest

from package.energy import (
    drain_energy,
    restore_energy,
    FREE_LINES,
    LINES_PER_POINT,
    MAX_DRAIN,
)
from package.pet import MAX_STAT


def test_drain_energy_zero_and_small_commit():
    pet = {"energy": 50}

    assert drain_energy(pet, 0) == 50
    assert drain_energy(pet, 20) == 50
    assert drain_energy(pet, FREE_LINES) == 50


def test_drain_energy_typical():
    pet = {"energy": 50}

    assert drain_energy(pet, 60) == 49
    assert drain_energy(pet, 100) == 44
    assert drain_energy(pet, 150) == 34


def test_drain_energy_max_and_clamped():
    pet = {"energy": 100}

    assert drain_energy(pet, 1000) == 100 - MAX_DRAIN

    pet["energy"] = 5
    assert drain_energy(pet, 1000) == 0


def test_drain_energy_boundary():
    pet = {"energy": 50}

    assert drain_energy(
        pet, FREE_LINES + LINES_PER_POINT - 1
    ) == 50
    assert drain_energy(
        pet, FREE_LINES + LINES_PER_POINT
    ) == 49


@pytest.mark.parametrize(
    ("count", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (None, TypeError),
        (-1, ValueError),
        ("100", TypeError),
    ],
)
def test_drain_energy_invalid_counts(count, error):
    pet = {"energy": 50}

    with pytest.raises(error):
        drain_energy(pet, count)


@pytest.mark.parametrize(
    ("value", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        ("50", TypeError),
        (True, TypeError),
        (50.5, TypeError),
    ],
)
def test_drain_energy_invalid_pet(value, error):
    pet = {"energy": value}

    with pytest.raises(error):
        drain_energy(pet, 60)


def test_drain_energy_missing_stat():
    pet = {}

    with pytest.raises(TypeError):
        drain_energy(pet, 60)


def test_restore_energy_typical():
    pet = {"energy": 50}

    assert restore_energy(pet, 5) == 60
    assert restore_energy(pet, 3, 2) == 64
    assert restore_energy(pet, 0) == 64


def test_restore_energy_failures():
    pet = {"energy": 50}

    assert restore_energy(pet, 2, 3) == 51
    assert restore_energy(pet, 1, 10) == 51
    assert restore_energy(pet, 0, 5) == 51


def test_restore_energy_zero_gain():
    pet = {"energy": 50}

    assert restore_energy(pet, 2, 4) == 50
    assert restore_energy(pet, 0, 0) == 50


def test_restore_energy_max_and_clamped():
    pet = {"energy": 95}

    assert restore_energy(pet, 10) == MAX_STAT
    assert restore_energy(pet, 5) == MAX_STAT


def test_restore_energy_large_count():
    pet = {"energy": 10}

    assert restore_energy(pet, 10000) == MAX_STAT


@pytest.mark.parametrize(
    ("count", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (None, TypeError),
        (-1, ValueError),
        ("5", TypeError),
    ],
)
def test_restore_energy_invalid_passed(count, error):
    pet = {"energy": 50}

    with pytest.raises(error):
        restore_energy(pet, count)


@pytest.mark.parametrize(
    ("count", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (None, TypeError),
        (-1, ValueError),
        ("5", TypeError),
    ],
)
def test_restore_energy_invalid_failed(count, error):
    pet = {"energy": 50}

    with pytest.raises(error):
        restore_energy(pet, 5, count)


@pytest.mark.parametrize(
    ("value", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        ("50", TypeError),
        (True, TypeError),
        (50.5, TypeError),
    ],
)
def test_restore_energy_invalid_pet(value, error):
    pet = {"energy": value}

    with pytest.raises(error):
        restore_energy(pet, 5)


def test_restore_energy_missing_stat():
    pet = {}

    with pytest.raises(TypeError):
        restore_energy(pet, 5)


def test_energy_updates_pet():
    pet = {"energy": 50}

    assert drain_energy(pet, 100) == pet["energy"]
    assert restore_energy(pet, 5) == pet["energy"]
