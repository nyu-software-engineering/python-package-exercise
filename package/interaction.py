# all user interaction goes here
from pathlib import Path

from .history import get_history
from .hunger import feed
from .hygiene import clean
from .pet import MIN_STAT, MAX_STAT
from .happy import play
from .save_load import load_pet, save_pet

COLOR = "\033[34m"
BOLD = "\033[1m"
UNBOLD = "\033[0m"
SAVE_FILE = Path.home() / ".virtual_pet.json"
INTRO = """
    *************************
    *                       *
    *   ~+ VIRTUAL PET +~   *
    *                       *
    *************************
"""
MENU = """
    *************************
    *                       *
    *   (1) CHECK WELLNESS  *
    *   (2) PLAY            *
    *   (3) FEED            *
    *   (4) CLEAN           *
    *   (5) HISTORY         *
    *   (6) QUIT            *
    *                       *
    *************************
"""

def create_pet():
    """Initializes pet and gives it a name chosen by the user"""
    print(f"{BOLD}What would you like to name your pet?{UNBOLD}")
    name = input().strip()
    while not name:
        name = input("Please enter a name").strip()
    return {
        "name": name,
        "alive": True,
        "history": [],
        "hunger": MIN_STAT,
        "happiness": MAX_STAT,
        "energy": MAX_STAT,
        "health": MAX_STAT,
        "hygiene": MAX_STAT,
    }

def get_pet():
    """Loads the saved pet if there is one, otherwise creates a new pet"""
    if SAVE_FILE.exists():
        try:
            pet = load_pet(SAVE_FILE)
            print(f"{BOLD}Welcome back, {pet['name']}!{UNBOLD}")
            return pet
        except (ValueError, TypeError):
            print(f"{BOLD}Your save file couldn't be read, so let's start a new pet.{UNBOLD}")
    return create_pet()

def show_stats(pet):
    print(f"{BOLD}{pet['name']}'s stats:{UNBOLD}")
    for stat in ("health", "hunger", "happiness", "hygiene", "energy"):
        print(f"{BOLD}{stat.capitalize()}: {pet[stat]}%{UNBOLD}")

def show_history(pet):
    events = get_history(pet, 10)
    if not events:
        print(f"{BOLD}No history yet.{UNBOLD}")
        return
    print(f"{BOLD}Recent history:{UNBOLD}")
    for event in events:
        detail = f" ({event['detail']})" if event["detail"] else ""
        change = ""
        if event["stat"] is not None:
            change = f": {event['stat']} {event['before']} -> {event['after']}"
        print(f"{BOLD}{event['action']}{detail}{change}{UNBOLD}")

# Primary function
def main():
    print(f"{BOLD}{COLOR}{INTRO}{UNBOLD}")
    pet = get_pet()

    while True:
        print(f"{BOLD}{MENU}{UNBOLD}")
        choice = input("> ").strip()
        if choice == "1":
            show_stats(pet)
        elif choice == "2":
            print(f"{BOLD}Chose a type of play: (1) pet, (2) catch, or (3) walk{UNBOLD}")
            play_type = input("> ").strip()
            print(play(pet, pet["name"], play_type))
            save_pet(pet, SAVE_FILE)
        elif choice == "3":
            feed(pet)
            print(f"{BOLD}You fed {pet['name']}.{UNBOLD}")
            save_pet(pet, SAVE_FILE)
        elif choice == "4":
            clean(pet)
            print(f"{BOLD}You cleaned {pet['name']}.{UNBOLD}")
            save_pet(pet, SAVE_FILE)
        elif choice == "5":
            show_history(pet)
        elif choice == "6":
            save_pet(pet, SAVE_FILE)
            print(f"{BOLD}See you later, {pet['name']} will miss you!{UNBOLD}")
            break
        else:
            print(f"{BOLD}Please choose a valid option{UNBOLD}")

# run by typing: python3 -m package.interaction
if __name__ == "__main__":
    main()