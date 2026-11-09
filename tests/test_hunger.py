"""Tests for the pet's hunger stat."""

import pytest

from package.hunger import HUNGER_PER_INPUT, update_hunger
from package.pet import MAX_STAT


def test_update_hunger_zero_typical_and_clamped():
    pet = {"hunger": 0}

    assert update_hunger(pet, 0) == 0
    assert update_hunger(pet, 3) == 3 * HUNGER_PER_INPUT
    assert update_hunger(pet, MAX_STAT) == MAX_STAT


@pytest.mark.parametrize(
    ("count", "error"),
    [
        (True, TypeError),
        (1.5, TypeError),
        (None, TypeError),
        (-1, ValueError),
    ],
)
def test_update_hunger_rejects_invalid_counts(count, error):
    pet = {"hunger": 0}

    with pytest.raises(error):
        update_hunger(pet, count)