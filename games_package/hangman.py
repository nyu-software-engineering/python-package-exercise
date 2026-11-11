import random
import tkinter as tk


WORDS = {
    "animals": {
        "easy": [
            "cat", "dog", "cow", "fish", "bird",
            "duck", "pig", "horse", "sheep", "goat",
            "lion", "bear", "frog", "ant", "bee",
            "crab", "deer", "wolf", "mouse", "snake"
        ],
        "medium": [
            "tiger", "rabbit", "monkey", "dolphin", "zebra",
            "giraffe", "penguin", "turtle", "shark", "eagle",
            "parrot", "donkey", "otter", "panda", "beaver",
            "falcon", "lizard", "walrus", "koala", "lobster"
        ],
        "hard": [
            "elephant", "crocodile", "chimpanzee", "rhinoceros",
            "hippopotamus", "orangutan", "chameleon", "armadillo",
            "porcupine", "platypus", "salamander", "flamingo",
            "jellyfish", "woodpecker", "grasshopper", "anteater",
            "wolverine", "meerkat", "mongoose", "alligator"
        ]
    },

    "food": {
        "easy": [
            "egg", "pie", "rice", "cake", "bread",
            "milk", "soup", "apple", "pear", "grape",
            "corn", "beef", "pork", "fish", "toast",
            "pasta", "beans", "peach", "plum", "lemon"
        ],
        "medium": [
            "pizza", "banana", "cookie", "cheese", "burger",
            "waffle", "pancake", "chicken", "salmon", "shrimp",
            "potato", "carrot", "yogurt", "cereal", "biscuit",
            "muffin", "noodles", "sausage", "avocado", "popcorn"
        ],
        "hard": [
            "spaghetti", "pineapple", "chocolate", "sandwich",
            "lasagna", "broccoli", "strawberry", "blueberry",
            "watermelon", "cheesecake", "quesadilla", "croissant",
            "guacamole", "macaroni", "mozzarella", "raspberry",
            "cappuccino", "pepperoni", "pistachio", "artichoke"
        ]
    },

    "technology": {
        "easy": [
            "app", "web", "code", "data", "wifi",
            "mouse", "phone", "screen", "email", "file",
            "game", "robot", "pixel", "video", "audio",
            "disk", "chip", "link", "text", "camera"
        ],
        "medium": [
            "python", "laptop", "tablet", "browser", "server",
            "router", "memory", "coding", "website", "console",
            "monitor", "printer", "network", "storage", "software",
            "hardware", "database", "internet", "download", "upload"
        ],
        "hard": [
            "computer", "keyboard", "algorithm", "processor",
            "encryption", "firewall", "bluetooth", "microchip",
            "motherboard", "programming", "cybersecurity",
            "authentication", "virtualization", "cryptography",
            "bandwidth", "compression", "automation",
            "microprocessor", "transistor", "blockchain"
        ]
    },

    "sports": {
        "easy": [
            "run", "bat", "golf", "ball", "kick",
            "goal", "race", "swim", "jump", "team",
            "coach", "score", "field", "court", "ring",
            "puck", "net", "skate", "bike", "throw"
        ],
        "medium": [
            "soccer", "tennis", "hockey", "boxing", "baseball",
            "football", "cycling", "skiing", "surfing", "rowing",
            "karate", "archery", "bowling", "cricket", "wrestling",
            "fencing", "running", "swimming", "judo", "rugby"
        ],
        "hard": [
            "basketball", "volleyball", "gymnastics", "badminton",
            "snowboarding", "skateboarding", "weightlifting",
            "powerlifting", "triathlon", "pentathlon",
            "kickboxing", "bodybuilding", "motocross",
            "racquetball", "pickleball", "waterpolo",
            "taekwondo", "decathlon", "handball", "lacrosse"
        ]
    },

    "superheroes": {
        "easy": [
            "batman", "superman", "spiderman", "ironman",
            "thor", "hulk", "flash", "robin", "joker",
            "venom", "thanos", "loki", "groot", "rocket",
            "shazam", "aquaman", "cyborg", "bane",
            "storm", "blade", "wanda", "vision",
            "ultron", "magneto", "wolverine", "deadpool",
            "optimus", "bumblebee", "raphael", "leonardo"
        ],
        "medium": [
            "daredevil", "punisher", "nightwing", "starfire",
            "raven", "beastboy", "supergirl", "batgirl",
            "catwoman", "mysterio", "electro", "sandman",
            "mystique", "gambit", "cyclops", "colossus",
            "carnage", "drstrange", "blackpanther",
            "moonknight", "invincible", "omniman",
            "atomeve", "megatron", "starscream",
            "soundwave", "donatello", "michelangelo",
            "splinter", "shredder"
        ],
        "hard": [
            "darkseid", "doomsday", "brainiac", "deathstroke",
            "rorschach", "constantine", "sinestro", "redhood",
            "azrael", "martianmanhunter", "silversurfer",
            "galactus", "apocalypse", "juggernaut",
            "taskmaster", "annihilus", "modok", "sentry",
            "hyperion", "bullseye", "conquest", "battlebeast",
            "thragg", "angstrom", "robot", "shockwave",
            "grimlock", "unicron", "krang", "bebop"
        ]
    },

    "professions": {
        "easy": [
            "doctor", "nurse", "teacher", "chef", "pilot",
            "farmer", "driver", "actor", "singer", "dancer",
            "artist", "writer", "judge", "lawyer", "police",
            "coach", "baker", "barber", "cashier", "dentist"
        ],
        "medium": [
            "engineer", "mechanic", "plumber", "electrician",
            "firefighter", "scientist", "architect", "surgeon",
            "journalist", "accountant", "librarian", "therapist",
            "designer", "photographer", "programmer",
            "veterinarian", "professor", "translator",
            "carpenter", "pharmacist"
        ],
        "hard": [
            "anesthesiologist", "neurosurgeon", "meteorologist",
            "paleontologist", "archaeologist", "biochemist",
            "cardiologist", "dermatologist", "psychiatrist",
            "microbiologist", "astrophysicist", "epidemiologist",
            "oceanographer", "criminologist", "radiologist",
            "endocrinologist", "optometrist", "orthodontist",
            "neurologist", "geologist"
        ]
    },

    "geography": {
        "easy": [
            "asia", "africa", "europe", "antarctica",
            "america", "pacific", "atlantic", "indian",
            "china", "japan", "india", "canada",
            "mexico", "brazil", "france", "italy",
            "egypt", "spain", "russia", "australia"
        ],
        "medium": [
            "germany", "portugal", "argentina", "colombia",
            "nigeria", "kenya", "morocco", "turkey",
            "thailand", "vietnam", "indonesia", "philippines",
            "iceland", "greenland", "madagascar", "sahara",
            "amazon", "everest", "himalayas", "arctic"
        ],
        "hard": [
            "machupicchu", "kilimanjaro", "tajmahal",
            "stonehenge", "petra", "angkorwat",
            "yellowstone", "grandcanyon", "victoriafalls",
            "greatbarrierreef", "mediterranean",
            "scandinavia", "mesopotamia", "patagonia",
            "uzbekistan", "kazakhstan", "azerbaijan",
            "kyrgyzstan", "tajikistan", "liechtenstein"
        ]
    },

    "movies_tv": {
        "easy": [
            "barbie", "frozen", "shrek", "cars", "up",
            "jaws", "rocky", "avatar", "titanic", "friends",
            "lost", "suits", "dexter", "naruto", "pokemon",
            "spongebob", "simpsons", "batman", "superman",
            "moana"
        ],
        "medium": [
            "inception", "interstellar", "gladiator",
            "deadpool", "ironman", "avengers", "transformers",
            "ratatouille", "zootopia", "coco", "encanto",
            "lucifer", "seinfeld", "futurama", "riverdale",
            "smallville", "supernatural", "theoffice",
            "breakingbad", "strangerthings"
        ],
        "hard": [
            "oppenheimer", "goodfellas", "scarface",
            "godfather", "parasite", "whiplash",
            "casablanca", "braveheart", "beetlejuice",
            "ghostbusters", "jurassicpark", "pulpfiction",
            "thematrix", "thewire", "succession",
            "chernobyl", "bettercallsaul", "blackmirror",
            "peakyblinders", "themandalorian"
        ]
    },

    "brands": {
        "easy": [
            "nike", "adidas", "apple", "google", "amazon",
            "sony", "samsung", "lego", "disney", "pepsi",
            "coke", "ford", "honda", "toyota", "tesla",
            "puma", "gucci", "vans", "gap", "target"
        ],
        "medium": [
            "microsoft", "nintendo", "playstation", "xbox",
            "netflix", "spotify", "youtube", "instagram",
            "snapchat", "tiktok", "starbucks", "walmart",
            "costco", "subway", "chipotle", "dominos",
            "reebok", "converse", "uniqlo", "versace"
        ],
        "hard": [
            "lamborghini", "maserati", "bugatti",
            "rollsroyce", "balenciaga", "givenchy",
            "burberry", "louisvuitton", "christiandior",
            "dolcegabbana", "underarmour", "newbalance",
            "americanexpress", "mastercard", "salesforce",
            "oracle", "nvidia", "qualcomm", "blackberry",
            "paramount"
        ]
    }
}


# Select a random word based on the chosen difficulty and category.
# Invalid selections raise an error instead of crashing later in the game.
def choose_word(difficulty, category):
    if category not in WORDS:
        raise ValueError("Invalid category")

    if difficulty not in WORDS[category]:
        raise ValueError("Invalid difficulty level")

    return random.choice(WORDS[category][difficulty])

# Process a player's guess and remember which letters were guessed.
# Returns whether the guess was correct, incorrect, or already used.
def check_guess(word, letter, guessed_letters):
    letter = letter.lower()

    if len(letter) != 1 or not letter.isalpha():
        raise ValueError("Enter a single letter")

    if letter in guessed_letters:
        return "already guessed"

    guessed_letters.append(letter)

    if letter in word:
        return "correct"
    else:
        return "incorrect"

# Display the word with underscores for letters not yet guessed.
def display_word(word, guessed_letters):
    display = ""

    for letter in word:
        if letter in guessed_letters:
            display += letter + " "
        else:
            display += "_ "

    return display.strip()

# Determine whether the player has won, lost, or is still playing.
# Only incorrect guesses count toward the attempt limit.
def check_game_status(word, guessed_letters, max_attempts=9):
    wrong_guesses = 0

    for letter in guessed_letters:
        if letter not in word:
            wrong_guesses += 1

    if all(letter in guessed_letters for letter in word):
        return "won"
    elif wrong_guesses >= max_attempts:
        return "lost"
    else:
        return "playing"

# Create the Hangman window and connect the interface to the game logic.
def start_game():
    word = choose_word("easy", "animals")

    window = tk.Tk()
    window.title("Hangman")
    window.geometry("600x900")
    window.configure(bg="#142B49")

    title = tk.Label(window, text="HANGMAN", font=("Arial", 24), bg="#142B49", fg="white")
    title.pack(pady=20)

    # Difficulty and category menus determine the next game's word.
    difficulty = tk.StringVar(value="easy")

    difficulty_menu = tk.OptionMenu(
        window,
        difficulty,
        "easy",
        "medium",
        "hard"
    )
    difficulty_menu.pack(pady=5)
    category = tk.StringVar(value="animals")

    category_menu = tk.OptionMenu(
        window,
        category,
        "animals",
        "food",
        "technology",
        "sports",
        "superheroes",
        "professions",
        "geography",
        "movies_tv",
        "brands"
    )
    category_menu.pack(pady=5)
    # Canvas displays the gallows and the Hangman drawing.
    canvas = tk.Canvas(window, width=200, height=180, bg="white")
    canvas.pack(pady=5)

    # Draw the gallows
    canvas.create_line(30, 160, 130, 160, width=3, fill="black")
    canvas.create_line(80, 160, 80, 20, width=3, fill="black")
    canvas.create_line(80, 20, 140, 20, width=3, fill="black")
    canvas.create_line(140, 20, 140, 40, width=3, fill="black")

    word_label = tk.Label(
        window,
        text=display_word(word, []),
        font=("Arial", 22),
        bg="#142B49",
        fg="white"
    )
    word_label.pack(pady=30)

    attempts_label = tk.Label(
        window,
        text="Attempts Remaining: 9",
        font=("Arial", 14),
        bg="#142B49",
        fg="white"
    )
    attempts_label.pack(pady=10)
    points_label = tk.Label(
        window,
        text="Points: 0",
        font=("Arial", 14),
        bg="#142B49",
        fg="white"
    )
    points_label.pack(pady=5)

    # Store the current round's guesses and the player's points.
    # Points carry over between rounds, while powerup_used resets.
    guessed_letters = []
    points = 0
    powerup_used = False

    # Draw one new body part for each incorrect guess.
    # The full drawing takes 9 incorrect guesses.
    def draw_hangman(wrong_guesses):
        if wrong_guesses == 1:
            canvas.create_oval(125, 40, 155, 70, width=3, outline="black")

        elif wrong_guesses == 2:
            canvas.create_line(140, 70, 140, 115, width=3, fill="black")

        elif wrong_guesses == 3:
            canvas.create_line(140, 85, 115, 100, width=3, fill="black")

        elif wrong_guesses == 4:
            canvas.create_line(140, 85, 165, 100, width=3, fill="black")

        elif wrong_guesses == 5:
            canvas.create_line(140, 115, 120, 145, width=3, fill="black")

        elif wrong_guesses == 6:
            canvas.create_line(140, 115, 160, 145, width=3, fill="black")

        elif wrong_guesses == 7:
            canvas.create_oval(131, 49, 135, 53, fill="black")

        elif wrong_guesses == 8:
            canvas.create_oval(145, 49, 149, 53, fill="black")

        elif wrong_guesses == 9:
            canvas.create_arc(
                133, 54, 147, 66,
                start=0, extent=180,
                style=tk.ARC, width=2,
                outline="black"
            )

    # Handle a letter button click, update the display, and check
    # whether the player has won or lost.
    def guess_letter(letter, button):
        result = check_guess(word, letter, guessed_letters)
        nonlocal points

        button.config(state="disabled")

        word_label.config(
            text=display_word(word, guessed_letters)
        )

        wrong_guesses = 0
        for guess in guessed_letters:
            if guess not in word:
                wrong_guesses += 1

        remaining = 9 - wrong_guesses

        if result == "incorrect":
            draw_hangman(wrong_guesses)

        attempts_label.config(
            text="Attempts Remaining: " + str(remaining)
        )

        status = check_game_status(word, guessed_letters)

        if status == "won":
            points += 1
            points_label.config(text="Points: " + str(points))
            message_label.config(text="You won!")
            disable_buttons()
            update_powerup_button()

        elif status == "lost":
            message_label.config(text="You lost! Word: " + word)
            disable_buttons()

    # Stop all guessing, hints, and power-ups when a round ends.
    def disable_buttons():
        for button in buttons:
            button.config(state="disabled")

        hint_button.config(state="disabled")
        powerup_button.config(state="disabled")

    # Start another round with a new word and reset the interface.
    # The player's points are intentionally kept.
    def new_game():
        nonlocal word, guessed_letters, powerup_used

        powerup_used = False
        word = choose_word(difficulty.get(), category.get())
        guessed_letters = []

        canvas.delete("all")

        # Redraw the gallows after clearing the previous Hangman.
        canvas.create_line(30, 160, 130, 160, width=3, fill="black")
        canvas.create_line(80, 160, 80, 20, width=3, fill="black")
        canvas.create_line(80, 20, 140, 20, width=3, fill="black")
        canvas.create_line(140, 20, 140, 40, width=3, fill="black")

        word_label.config(text=display_word(word, []))
        attempts_label.config(text="Attempts Remaining: 9")
        message_label.config(text="Guess a letter!")
        hint_button.config(state="normal")
        update_powerup_button()

        for button in buttons:
            button.config(state="normal")

    # Reveal one unguessed correct letter for free, once per round.
    # A hint can also complete the word and earn a point.
    def use_hint():
        hidden_letters = []
        nonlocal points

        for letter in word:
            if letter not in guessed_letters:
                hidden_letters.append(letter)

        if not hidden_letters:
            return

        hint_letter = random.choice(hidden_letters)
        guessed_letters.append(hint_letter)

        for button in buttons:
            if button.cget("text").lower() == hint_letter:
                button.config(state="disabled")

        word_label.config(
            text=display_word(word, guessed_letters)
        )

        hint_button.config(state="disabled")
        message_label.config(text="Hint revealed: " + hint_letter.upper())

        status = check_game_status(word, guessed_letters)

        if status == "won":
            points += 1
            points_label.config(text="Points: " + str(points))
            message_label.config(text="You won!")
            disable_buttons()
            update_powerup_button()

    # Enable the power-up only when the player has enough points,
    # has not used it this round, and the game is still active.
    def update_powerup_button():
        status = check_game_status(word, guessed_letters)

        if points >= 3 and not powerup_used and status == "playing":
            powerup_button.config(state="normal")
        else:
            powerup_button.config(state="disabled")

    # Spend 3 points to eliminate three incorrect letters.
    # These letters are disabled without counting as wrong guesses.
    def use_powerup():
        nonlocal points, powerup_used

        if points < 3 or powerup_used:
            return

        wrong_letters = []

        for letter in alphabet:
            if letter.lower() not in word and letter.lower() not in guessed_letters:
                wrong_letters.append(letter)

        # random.sample selects 3 different letters from the list.
        revealed_letters = random.sample(wrong_letters, 3)

        for button in buttons:
            if button.cget("text") in revealed_letters:
                button.config(state="disabled")

        points -= 3
        powerup_used = True

        points_label.config(text="Points: " + str(points))
        update_powerup_button()

        message_label.config(
            text="Eliminated: " + ", ".join(revealed_letters)
        )

    # Display messages such as hints, eliminated letters, and results.
    message_label = tk.Label(
        window,
        text="Guess a letter!",
        font=("Arial", 14),
        bg="#142B49",
        fg="white"
    )
    message_label.pack(pady=10)

    # Create the alphabet buttons in a grid.
    # Lambda remembers the letter and button for each click.
    button_frame = tk.Frame(window, bg="#142B49")
    button_frame.pack(pady=20)

    buttons = []

    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    for i, letter in enumerate(alphabet):
        button = tk.Button(
            button_frame,
            text=letter,
            width=4,
            bg="#8DD5FA",
            fg="#142B49",
            activebackground="#5BBCEB",
            activeforeground="#142B49",
            highlightbackground="#8DD5FA"
        )

        button.config(
            command=lambda l=letter, b=button: guess_letter(l, b)
        )

        button.grid(row=i // 7, column=i % 7, padx=2, pady=2)
        buttons.append(button)

    # Main controls for starting rounds and using special abilities.
    new_game_button = tk.Button(
        window,
        text="New Game",
        command=new_game,
        bg="#35A87B",
        fg="#142B49",
        highlightbackground="#35A87B"
    )
    new_game_button.pack(pady=10)
    hint_button = tk.Button(
        window,
        text="Use Hint",
        command=use_hint,
        bg="#E9A64A",
        fg="#142B49",
        highlightbackground="#E9A64A"
    )
    hint_button.pack(pady=5)
    powerup_button = tk.Button(
        window,
        text="Eliminate 3 Letters (3 Points)",
        command=use_powerup,
        bg="#A78BFA",
        fg="#142B49",
        highlightbackground="#A78BFA",
        state="disabled"
    )
    powerup_button.pack(pady=5)

    # Keep the window open and respond to player actions.
    window.mainloop()

# Launch the game only when this file is run directly.
# Importing it for pytest will not open the GUI.
if __name__ == "__main__":
    start_game()