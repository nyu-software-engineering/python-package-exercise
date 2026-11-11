"""Update the pet's hunger based on inputs since it was fed."""

from .history import record_event
from .pet import MIN_STAT, check_count, check_pet, clamp

HUNGER_PER_INPUT = 5


def feed(pet):
    """Set hunger to zero and record a feed event."""
    check_pet(pet, "hunger")
    before = pet["hunger"]
    pet["hunger"] = MIN_STAT
    record_event(pet, "feed", stat="hunger", before=before, after=pet["hunger"])
    return pet["hunger"]


def update_hunger(pet, inputs_since_fed):
    """Raise hunger as inputs occur after the pet was fed."""
    check_pet(pet, "hunger")
    check_count(inputs_since_fed, "inputs_since_fed")

    before = pet["hunger"]
    pet["hunger"] = clamp(inputs_since_fed * HUNGER_PER_INPUT)
    return pet["hunger"]
