from pet import clamp

def play(pet, name, play_type):
    # invalid arguments
    if play_type is None or not isinstance(play_type, str):
        print("\033[1mThat is not a valid play type.\033[0m")
        return

    # case insensitive
    play_type = play_type.lower()

    # valid arguments
    if play_type == "pet":
        print(f"\033[1m*You pet {name}, they love it!*\033[0m")
        _increase_happiness(pet, 15)
    elif play_type == "catch":
        print(f"\033[1m*You throw a ball to {name}, they catch it and happily bring it back to you!*\033[0m")
        _increase_happiness(pet, 10)
    elif play_type == "walk":
        print(f"\033[1m*You take {name} on a walk, they smile the entire time!*\033[0m")
        _increase_happiness(pet, 5)
    else:
        print("\033[1mThat is not a valid play type.\033[0m")
    return

def _increase_happiness(pet, happiness_boost):
    pet["happiness"] = clamp(pet["happiness"] + happiness_boost)
    return pet["happiness"]
