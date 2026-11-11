from .happy import increase_happiness
from .history import record_event
from .pet import clamp

def _spend_energy(pet, amount):
    """Lower energy by amount and record the change."""
    before = pet["energy"]
    pet["energy"] = clamp(before - amount)
    if pet["energy"] != before:
        record_event(pet, "stat", stat="energy", before=before, after=pet["energy"])
    return pet["energy"]

def play(pet, name, play_type):
    """Uses user input to select which type of play, increases happiness accordingly"""
    # invalid arguments
    if play_type is None or not isinstance(play_type, str):
        return("\033[1mThat is not a valid play type.\033[0m")

    # valid arguments
    if play_type == "1": # pet
        before = pet["happiness"]
        increase_happiness(pet, 15)
        _spend_energy(pet, 5)
        record_event(pet, "play", detail="pet", stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You pet {name}, they love it!*\033[0m")
    elif play_type == "2": # catch
        before = pet["happiness"]
        increase_happiness(pet, 10)
        _spend_energy(pet, 10)
        record_event(pet, "play", detail="catch", stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You throw a ball to {name}, they catch it and happily bring it back to you!*\033[0m")
    elif play_type == "3": # walk
        before = pet["happiness"]
        increase_happiness(pet, 5)
        _spend_energy(pet, 15)
        record_event(pet, "play", detail="walk", stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You take {name} on a walk, they smile the entire time!*\033[0m")
    else:
        return("\033[1mThat is not a valid play type.\033[0m")