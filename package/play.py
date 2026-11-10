from .happy import increase_happiness
from .history import record_event

def play(pet, name, play_type):
    """Uses user input to select which type of play, increases happiness accordingly"""
    # invalid arguments
    if play_type is None or not isinstance(play_type, str):
        return("\033[1mThat is not a valid play type.\033[0m")

    # case insensitive
    play_type = play_type.lower()

    # valid arguments
    if play_type == "pet":
        before = pet["happiness"]
        increase_happiness(pet, 15)
        record_event(pet, "play", detail=play_type, stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You pet {name}, they love it!*\033[0m")
    elif play_type == "catch":
        before = pet["happiness"]
        increase_happiness(pet, 10)
        record_event(pet, "play", detail=play_type, stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You throw a ball to {name}, they catch it and happily bring it back to you!*\033[0m")
    elif play_type == "walk":
        before = pet["happiness"]
        increase_happiness(pet, 5)
        record_event(pet, "play", detail=play_type, stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You take {name} on a walk, they smile the entire time!*\033[0m")
    else:
        return("\033[1mThat is not a valid play type.\033[0m")