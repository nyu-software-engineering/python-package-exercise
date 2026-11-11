from .happy import increase_happiness

def play(pet, name, play_type):
    """Uses user input to select which type of play, increases happiness accordingly"""
    # invalid arguments
    if play_type is None or not isinstance(play_type, str):
        return("\033[1mThat is not a valid play type.\033[0m")

    # valid arguments
    if play_type == "1": # pet
        increase_happiness(pet, 15)
        record_event(pet, "play", detail=play_type, stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You pet {name}, they love it!*\033[0m")
    elif play_type == "2": # catch
        increase_happiness(pet, 10)
        record_event(pet, "play", detail=play_type, stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You throw a ball to {name}, they catch it and happily bring it back to you!*\033[0m")
    elif play_type == "3": # walk
        increase_happiness(pet, 5)
        record_event(pet, "play", detail=play_type, stat="happiness", before=before, after=pet["happiness"])
        return(f"\033[1m*You take {name} on a walk, they smile the entire time!*\033[0m")
    else:
        return("\033[1mThat is not a valid play type.\033[0m")