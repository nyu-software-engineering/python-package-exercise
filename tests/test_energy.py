import pytest

from package.energy import drain_energy, restore_energy


@pytest.mark.parametrize(
    ("lines", "expected"),
    [
        (0, 50),
        (50, 50),
        (59, 50),
        (60, 49),
        (100, 45),
        (1000, 10),
    ],
)
def test_drain_energy_normal_and_boundaries(lines, expected):
    pet = {"energy": 50}

    assert drain_energy(pet, lines) == expected
    assert pet["energy"] == expected


def test_drain_energy_clamped():
    pet = {"energy": 5}

    assert drain_energy(pet, 1000) == 0


@pytest.mark.parametrize(
    ("count", "error"),
    [
        (-1, ValueError),
        (None, TypeError),
        (True, TypeError),
        (1.5, TypeError),
        ("100", TypeError),
    ],
)
def test_drain_energy_invalid_count(count, error):
    with pytest.raises(error):
        drain_energy({"energy": 50}, count)


@pytest.mark.parametrize(
    ("energy", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        ("50", TypeError),
    ],
)
def test_drain_energy_invalid_pet(energy, error):
    with pytest.raises(error):
        drain_energy({"energy": energy}, 60)


def test_drain_energy_missing_stat():
    with pytest.raises(TypeError):
        drain_energy({}, 60)


@pytest.mark.parametrize(
    ("passed", "failed", "expected"),
    [
        (0, 0, 50),
        (5, 0, 60),
        (3, 2, 54),
        (2, 4, 50),
        (1, 10, 50),
        (100, 0, 100),
    ],
)
def test_restore_energy_normal_and_boundaries(passed, failed, expected):
    pet = {"energy": 50}

    assert restore_energy(pet, passed, failed) == expected
    assert pet["energy"] == expected


@pytest.mark.parametrize(
    ("passed", "failed", "error"),
    [
        (-1, 0, ValueError),
        (0, -1, ValueError),
        (None, 0, TypeError),
        (0, True, TypeError),
        (1.5, 0, TypeError),
        (0, "5", TypeError),
    ],
)
def test_restore_energy_invalid_counts(passed, failed, error):
    with pytest.raises(error):
        restore_energy({"energy": 50}, passed, failed)


@pytest.mark.parametrize(
    ("energy", "error"),
    [
        (-1, ValueError),
        (101, ValueError),
        (None, TypeError),
        (True, TypeError),
    ],
)
def test_restore_energy_invalid_pet(energy, error):
    with pytest.raises(error):
        restore_energy({"energy": energy}, 5)


def test_restore_energy_missing_stat():
    with pytest.raises(TypeError):
        restore_energy({}, 5)
