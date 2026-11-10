# all user interaction goes here
from .pet import MIN_STAT, MAX_STAT
from .play import play

COLOR = "\033[34m"
BOLD = "\033[1m"
UNBOLD = "\033[0m"
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
    *   (3) QUIT            *
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
        "hunger": MIN_STAT,
        "happiness": MAX_STAT,
        "energy": MAX_STAT,
        "health": MAX_STAT,
        "hygiene": MAX_STAT,
    }

def show_stats(pet):
    print(f"{BOLD}{pet['name']}'s stats:{UNBOLD}")
    for stat in ("health", "hunger", "happiness", "hygiene", "energy"):
        print(f"{BOLD}{stat.capitalize()}: {pet[stat]}%{UNBOLD}")

# Primary function
def main():
    print(f"{BOLD}{COLOR}{INTRO}{UNBOLD}")
    pet = create_pet()

    while True:
        print(f"{BOLD}{MENU}{UNBOLD}")
        choice = input("> ").strip()
        if choice == "1":
            show_stats(pet)
        elif choice == "2":
            print(f"{BOLD}Chose a type of play: (1) pet, (2) catch, or (3) walk{UNBOLD}")
            play_type = input("> ").strip()
            print(play(pet, pet['name'], play_type))
        elif choice == "3":
            print(f"{BOLD}See you later, {pet['name']} will miss you!{UNBOLD}")
            break
        else:
            print(f"{BOLD}Please choose a valid option{UNBOLD}")

# run by typing: python3 -m package.interaction
if __name__ == "__main__":
    main()