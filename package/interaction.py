# all user interaction goes here
import time
from pathlib import Path

from .display import show_pet
from .energy import restore_energy
from .history import get_history
from .hunger import feed
from .hygiene import clean
from .pet import MIN_STAT, MAX_STAT
from .happy import play
from .save_load import load_pet, save_pet
from .time_passed import apply_time

COLOR = "\033[34m"
BOLD = "\033[1m"
UNBOLD = "\033[0m"
CLEAR = "\033[2J\033[H"
SAVE_FILE = Path.home() / ".virtual_pet.json"
INNER = 16
INTRO = """
    *************************
    *                       *
    *   ~+ VIRTUAL PET +~   *
    *                       *
    *************************
"""
MENU_LINES = [
    "(1) rest",
    "(2) play",
    "(3) feed",
    "(4) clean",
    "(5) history",
    "(6) quit",
]
PLAY_LINES = [
    "(1) pet",
    "(2) catch",
    "(3) walk",
    "",
    "",
    "",
]
SLEEP_FRAMES = [
    ["", "     /\\_/\\", "    ( -.- )", "     > w <", "       z", ""],
    ["", "     /\\_/\\", "    ( -.- )", "     > w <", "      zZ", ""],
    ["", "     /\\_/\\", "    ( -.- )", "     > w <", "     zZz", ""],
]
FEED_FRAMES = [
    ["", "     /\\_/\\", "    ( o.o )", "     > w <", "    [bowl]", ""],
    ["", "     /\\_/\\", "    ( ^o^ )", "     > w <", "     nom", ""],
    ["", "     /\\_/\\", "    ( ^.^ )", "     > w <", "    nom!", ""],
]
CLEAN_FRAMES = [
    ["", "   ~ /\\_/\\", "    ( o.o )", "   ~ > w <", "     wash", ""],
    ["", "  *  /\\_/\\ *", "    ( ^.^ )", "     > w <", "    scrub", ""],
    ["", "     /\\_/\\", "    ( ^.^ )", "     > w <", "   sparkle", ""],
]
PET_FRAMES = [
    ["", "     /\\_/\\", "  * ( ^.^ )", "     > w <", "", ""],
    ["", "     /\\_/\\", "    ( ^.^ )* ", "     > w <", "    pets", ""],
    ["", "     /\\_/\\", "    ( ^w^ )", "     > w <", "    purr", ""],
]
CATCH_FRAMES = [
    ["", "     /\\_/\\", "    ( o.o )", "     > w <", "      o", ""],
    ["", "     /\\_/\\", "    ( O.O )", "     > o <", "     o", ""],
    ["", "     /\\_/\\", "    ( ^.^ )", "     > w <", "   got it!", ""],
]
WALK_FRAMES = [
    ["", "   /\\_/\\", "  ( ^.^ )", "   > w <", "   step", ""],
    ["", "    /\\_/\\", "   ( ^.^ )", "    > w <", "    step", ""],
    ["", "     /\\_/\\", "    ( ^.^ )", "     > w <", "     step", ""],
]
PLAY_FRAMES = {
    "1": PET_FRAMES,
    "2": CATCH_FRAMES,
    "3": WALK_FRAMES,
}

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
        "last_seen": int(time.time()),
        "hunger": MIN_STAT,
        "happiness": MAX_STAT,
        "energy": MAX_STAT,
        "health": MAX_STAT,
        "hygiene": MAX_STAT,
    }

def get_pet():
    """Loads the saved pet if there is one, otherwise creates a new pet."""
    if SAVE_FILE.exists():
        try:
            pet = load_pet(SAVE_FILE)
            return pet, f"{BOLD}Welcome back, {pet['name']}!{UNBOLD}"
        except (ValueError, TypeError):
            print(f"{BOLD}Your save file couldn't be read, so let's start a new pet.{UNBOLD}")
    pet = create_pet()
    return pet, f"{BOLD}Say hi to {pet['name']}!{UNBOLD}"

def history_text(pet):
    """Return the recent history as one block of text."""
    events = get_history(pet, 4)
    if not events:
        return f"{BOLD}No history yet.{UNBOLD}"
    lines = [f"{BOLD}Recent history:{UNBOLD}"]
    for event in events:
        detail = f" ({event['detail']})" if event["detail"] else ""
        change = ""
        if event["stat"] is not None:
            change = f": {event['stat']} {event['before']} -> {event['after']}"
        lines.append(f"{BOLD}{event['action']}{detail}{change}{UNBOLD}")
    return "\n".join(lines)

def _fit(lines):
    """Pad or trim lines so a box has six rows of the same width."""
    fitted = [line[:INNER].ljust(INNER) for line in lines[:6]]
    return fitted + [" " * INNER] * (6 - len(fitted))

def _box(lines):
    """Return one asterisk box as a list of rows."""
    rows = _fit(lines)
    edge = "*" * (INNER + 4)
    return [edge, *[f"* {row} *" for row in rows], edge]

def _screen(pet, menu_lines, pet_lines=None):
    """Build the menu, pet, and stats boxes on one row."""
    if pet_lines is None:
        cat = show_pet(pet).splitlines()
        top = (6 - len(cat)) // 2
        pet_lines = [""] * top + cat
    stats = [pet["name"]] + [
        f"{stat.capitalize()} {pet[stat]}"
        for stat in ("health", "hunger", "happiness", "hygiene", "energy")
    ]
    left, middle, right = _box(menu_lines), _box(pet_lines), _box(stats)
    return "\n".join(
        f"{BOLD}{one}  {COLOR}{two}{UNBOLD}{BOLD}  {three}{UNBOLD}"
        for one, two, three in zip(left, middle, right)
    )

def draw_screen(pet, message, menu_lines, pet_lines=None):
    """Clear the terminal and redraw the three boxes, then the last message."""
    print(CLEAR, end="")
    print(_screen(pet, menu_lines, pet_lines))
    if message:
        print(f"\n{message}")
    print(flush=True)

def animate(pet, frames, message, menu_lines):
    """Redraw the middle box once per frame."""
    for frame in frames:
        draw_screen(pet, message, menu_lines, frame)
        time.sleep(0.45)

def pass_time(pet):
    """Apply minutes since last_seen and save the pet when anything changed."""
    minutes = apply_time(pet)
    if minutes:
        save_pet(pet, SAVE_FILE)
    return minutes

# Primary function
def main():
    print(f"{BOLD}{COLOR}{INTRO}{UNBOLD}")
    pet, message = get_pet()

    while True:
        minutes = pass_time(pet)
        if minutes:
            message = f"{BOLD}{minutes} minute(s) passed. {pet['name']} grew hungrier and more tired.{UNBOLD}"
        draw_screen(pet, message, MENU_LINES)
        choice = input("> ").strip()
        if choice == "1":
            animate(pet, SLEEP_FRAMES, f"{BOLD}{pet['name']} is falling asleep...{UNBOLD}", MENU_LINES)
            before = pet["energy"]
            restore_energy(pet, 10)
            message = f"{BOLD}{pet['name']} woke up. Energy {before} -> {pet['energy']}.{UNBOLD}"
            save_pet(pet, SAVE_FILE)
        elif choice == "2":
            draw_screen(pet, f"{BOLD}Choose a type of play.{UNBOLD}", PLAY_LINES)
            play_type = input("> ").strip()
            if play_type in PLAY_FRAMES and pet["energy"] > 0:
                animate(
                    pet,
                    PLAY_FRAMES[play_type],
                    f"{BOLD}{pet['name']} is playing...{UNBOLD}",
                    PLAY_LINES,
                )
            message = play(pet, pet["name"], play_type)
            save_pet(pet, SAVE_FILE)
        elif choice == "3":
            animate(pet, FEED_FRAMES, f"{BOLD}{pet['name']} is eating...{UNBOLD}", MENU_LINES)
            feed(pet)
            message = f"{BOLD}You fed {pet['name']}.{UNBOLD}"
            save_pet(pet, SAVE_FILE)
        elif choice == "4":
            animate(pet, CLEAN_FRAMES, f"{BOLD}{pet['name']} is getting clean...{UNBOLD}", MENU_LINES)
            clean(pet)
            message = f"{BOLD}You cleaned {pet['name']}.{UNBOLD}"
            save_pet(pet, SAVE_FILE)
        elif choice == "5":
            message = history_text(pet)
        elif choice == "6":
            save_pet(pet, SAVE_FILE)
            print(f"{BOLD}See you later, {pet['name']} will miss you!{UNBOLD}")
            break
        else:
            message = f"{BOLD}Please choose a valid option{UNBOLD}"

# run by typing: python3 -m package.interaction
if __name__ == "__main__":
    main()