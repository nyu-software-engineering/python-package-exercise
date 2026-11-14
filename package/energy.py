
from .history import record_event
from .pet import check_count, check_pet, clamp

REST_ENERGY = 20


def drain_energy(pet, amount):
    """Decrease energy by a given amount."""
    check_pet(pet, "energy")
    check_count(amount, "amount")

    before = pet["energy"]
    pet["energy"] = clamp(before - amount)

    if pet["energy"] != before:
        record_event(
            pet, "stat",
            stat="energy",
            before=before,
            after=pet["energy"]
        )

    return pet["energy"]


def restore_energy(pet, amount=REST_ENERGY):
    """Restore energy by a given amount."""
    check_pet(pet, "energy")
    check_count(amount, "amount")

    before = pet["energy"]
    pet["energy"] = clamp(before + amount)

    if pet["energy"] != before:
        record_event(
            pet, "stat",
            stat="energy",
            before=before,
            after=pet["energy"]
        )

    return pet["energy"]
