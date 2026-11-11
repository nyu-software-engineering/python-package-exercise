from datetime import datetime, timedelta, timezone

import pytest

from package.death import check_death
from package.pet import create_pet


def test_pet_alive():
    pet = create_pet("Buddy")

    assert check_death(pet) is False
    assert pet["alive"] is True
    assert pet["health"] == 100


def test_death_from_health():
    pet = create_pet("Buddy")
    pet["health"] = 10

    assert check_death(pet) is True
    assert pet["alive"] is False
    assert pet["health"] == 10


def test_death_below_threshold():
    pet = create_pet("Buddy")
    pet["health"] = 5

    assert check_death(pet) is True
    assert pet["alive"] is False


def test_death_from_inactivity():
    pet = create_pet("Mochi")
    now = datetime(2026, 11, 10, tzinfo=timezone.utc)
    last_opened = now - timedelta(days=8)

    result = check_death(pet, last_opened.isoformat(), now)

    assert result is True
    assert pet["alive"] is False
    assert pet["health"] == 100


def test_exactly_seven_days():
    pet = create_pet("Mochi")
    now = datetime(2026, 11, 10, tzinfo=timezone.utc)
    last_opened = now - timedelta(days=7)

    assert check_death(pet, last_opened.isoformat(), now) is True
    assert pet["alive"] is False


def test_less_than_seven_days():
    pet = create_pet("Mochi")
    now = datetime(2026, 11, 10, tzinfo=timezone.utc)
    last_opened = now - timedelta(days=6)

    assert check_death(pet, last_opened.isoformat(), now) is False
    assert pet["alive"] is True
    assert pet["health"] == 100


def test_dead_pet_stays_dead():
    pet = create_pet("Mochi")
    pet["alive"] = False

    assert check_death(pet) is True
    assert pet["alive"] is False


def test_invalid_health():
    pet = create_pet("Mochi")
    pet["health"] = -5

    with pytest.raises(ValueError):
        check_death(pet)


def test_missing_health():
    pet = create_pet("Mochi")
    del pet["health"]

    with pytest.raises(TypeError):
        check_death(pet)


def test_invalid_date():
    pet = create_pet("Mochi")

    with pytest.raises(ValueError):
        check_death(pet, "not-a-date")


def test_future_date():
    pet = create_pet("Mochi")
    now = datetime(2026, 11, 10, tzinfo=timezone.utc)
    future = now + timedelta(days=1)

    with pytest.raises(ValueError):
        check_death(pet, future.isoformat(), now)


def test_invalid_alive():
    pet = create_pet("Mochi")
    pet["alive"] = "yes"

    with pytest.raises(TypeError):
        check_death(pet)


def test_invalid_date_type():
    pet = create_pet("Mochi")

    with pytest.raises(TypeError):
        check_death(pet, 123)


def test_date_without_timezone():
    pet = create_pet("Mochi")

    with pytest.raises(ValueError):
        check_death(pet, "2026-11-01T12:00:00")


def test_invalid_now():
    pet = create_pet("Mochi")

    with pytest.raises(TypeError):
        check_death(pet, "2026-11-01T12:00:00+00:00", "today")
