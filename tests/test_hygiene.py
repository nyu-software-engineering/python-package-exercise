"""Tests for the pet's hygiene stat."""

import pytest

from package.hygiene import (
    HYGIENE_LOSS_PER_COMMIT_BEHIND,
    update_hygiene,
)
from package.pet import MAX_STAT


def test_update_hygiene_zero_typical_and_clamped():
    pet = {"hygiene": 0}

    assert update_hygiene(pet, 0) == MAX_STAT
    assert update_hygiene(pet, 3) == max(
        0, MAX_STAT - 3 * HYGIENE_LOSS_PER_COMMIT_BEHIND
    )
    assert update_hygiene(pet, MAX_STAT) == 0


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
def test_update_hygiene_rejects_invalid_counts(count, error):
    pet = {"hygiene": 0}

    with pytest.raises(error):
        update_hygiene(pet, count)