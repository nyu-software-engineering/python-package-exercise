"""Raise hunger and lower energy for the minutes since the pet was last seen."""

import time

from .history import record_event
from .pet import check_pet, clamp

HUNGER_PER_MINUTE = 1
ENERGY_PER_MINUTE = 1


def _minutes_since(last_seen, now):
    """Return whole minutes from last_seen to now."""
    if isinstance(now, bool) or not isinstance(now, int):
        raise TypeError("now must be an int")
    if isinstance(last_seen, bool) or not isinstance(last_seen, int):
        return 0
    return max(now - last_seen, 0) // 60


def apply_time(pet, now=None):
    """Apply elapsed minutes and return how many whole minutes passed."""
    check_pet(pet, "hunger")
    check_pet(pet, "energy")
    if now is None:
        now = int(time.time())
    if isinstance(now, bool) or not isinstance(now, int):
        raise TypeError("now must be an int")

    last_seen = pet.get("last_seen")
    minutes = _minutes_since(last_seen, now)
    pet["last_seen"] = now
    if minutes == 0:
        return 0

    before_hunger = pet["hunger"]
    pet["hunger"] = clamp(before_hunger + minutes * HUNGER_PER_MINUTE)
    if pet["hunger"] != before_hunger:
        record_event(pet, "stat", stat="hunger", before=before_hunger, after=pet["hunger"])

    before_energy = pet["energy"]
    pet["energy"] = clamp(before_energy - minutes * ENERGY_PER_MINUTE)
    if pet["energy"] != before_energy:
        record_event(pet, "stat", stat="energy", before=before_energy, after=pet["energy"])
    return minutes