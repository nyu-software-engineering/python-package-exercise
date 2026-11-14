
from .pet import clamp, check_count, check_pet
from .history import record_event
from .energy import drain_energy


def play(pet, name, play_type):
    """Uses user input to select which type of play, increases happiness accordingly"""

    # Invalid arguments
    if play_type is None or not isinstance(play_type, str):
        return "\033[1mThat is not a valid play type.\033[0m"

    # Valid arguments
    if play_type == "1":  # Pet
        before = pet["happiness"]
        increase_happiness(pet, 15)
        drain_energy(pet, 5)
        record_event(
            pet, "play", detail="pet",
            stat="happiness", before=before,
            after=pet["happiness"]
        )
        return f"\033[1m*You pet {name}, they love it!*\033[0m"

    elif play_type == "2":  # Catch
        before = pet["happiness"]
        increase_happiness(pet, 10)
        drain_energy(pet, 10)
        record_event(
            pet, "play", detail="catch",
            stat="happiness", before=before,
            after=pet["happiness"]
        )
        return f"\033[1m*You throw a ball to {name}, they catch it and happily bring it back to you!*\033[0m"

    elif play_type == "3":  # Walk
        before = pet["happiness"]
        increase_happiness(pet, 5)
        drain_energy(pet, 15)
        record_event(
            pet, "play", detail="walk",
            stat="happiness", before=before,
            after=pet["happiness"]
        )
        return f"\033[1m*You take {name} on a walk, they smile the entire time!*\033[0m"

    else:
        return "\033[1mThat is not a valid play type.\033[0m"


def increase_happiness(pet, happiness_change):
    """Increment pet happiness by specified amount."""
    check_pet(pet, "happiness")
    check_count(happiness_change, "happiness_change")
    pet["happiness"] = clamp(pet["happiness"] + happiness_change)
    return pet["happiness"]


def decrease_happiness(pet, happiness_change):
    """Decrement pet happiness by specified amount."""
    check_pet(pet, "happiness")
    check_count(happiness_change, "happiness_change")
    pet["happiness"] = clamp(pet["happiness"] - happiness_change)
    return pet["happiness"]
