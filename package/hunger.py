"""Update the pet's hunger based on inputs since it was fed."""

from .pet import check_count, check_pet, clamp

HUNGER_PER_INPUT = 5


def update_hunger(pet, inputs_since_fed):
    """Raise hunger as inputs occur after the pet was fed."""
    check_pet(pet, "hunger")
    check_count(inputs_since_fed, "inputs_since_fed")

    pet["hunger"] = clamp(inputs_since_fed * HUNGER_PER_INPUT)
    return pet["hunger"]