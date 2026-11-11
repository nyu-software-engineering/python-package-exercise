import random
from collections import Counter
from spellchecker import SpellChecker

WORD_LENGTH = 5
DEFAULT_WORDS = (
    "apple", "grape", "peach", "lemon", "berry", "melon", "candy",
    "mango", "bread", "chair", "flame", "stone", "plant", "heart",
    "crane", "spear", "zebra", "brain", "tiger", "civic", "piano",
    "ocean", "cloud", "river", "beach", "storm", "snake", "sheep",
    "light", "dream", "smile", "dance", "music", "horse", "train",
    "house", "table", "clock", "phone", "brush", "queen", "magic",
    "green", "white", "black", "sweet", "fruit", "world", "happy",
    "quilt", "glyph", "nymph", "jazzy", "fuzzy", "tryst", "slyly",
    "vivid", "joker", "crypt", "waltz", "khaki", "squib", "yacht",
    "zesty", "quark", "vexed", "whisk", "blitz", "zonal", "quail",
    "pique", "axiom", "proxy", "jumpy", "shyly", "ivory", "ozone",
    "mirth", "knack", "wrath", "punch", "gnome", "abyss", "equip",
)

VALID_WORDS = SpellChecker(language="en")
VALID_WORDS.word_frequency.load_words(DEFAULT_WORDS)

def _is_valid_word(word):
    return (isinstance(word, str) and len(word) == WORD_LENGTH and word.isascii() and word.isalpha())

def _choose_word(words, rng=None):
    if not words:
        raise ValueError("Word list cannot be empty")
    picker = rng if rng is not None else random
    return picker.choice(words).lower()

def _score_guess(secret, guess):
    if not _is_valid_word(secret) or not _is_valid_word(guess):
        raise ValueError("secret and guess must both contain five letters")
    secret = secret.lower()
    guess = guess.lower()
    statuses = ["absent"] * WORD_LENGTH
    remaining = Counter()
    for index, letter in enumerate(guess):
        if letter == secret[index]:
            statuses[index] = "correct"
        else:
            remaining[secret[index]] += 1
    for index, letter in enumerate(guess):
        if statuses[index] == "correct":
            continue
        if remaining[letter] > 0:
            statuses[index] = "present"
            remaining[letter] -= 1
    return tuple(statuses)

def _format_feedback(guess, statuses):
    symbols = {"correct": "🟩", "present": "🟨", "absent": "⬛"}
    squares = "".join(symbols[status] for status in statuses)
    return f"{guess.upper()}  {squares}"

def play_wordle(max_attempts=6, *, words=None, secret=None, input_fn=input, output_fn=print, rng=None):
    if type(max_attempts) is not int or max_attempts < 1:
        raise ValueError("max_attempts must be a positive integer")
    if secret is not None and not _is_valid_word(secret):
        raise ValueError("secret must be a five-letter word")
    
    if secret is not None:
        answer = secret.lower()
    else:
        answer = _choose_word(DEFAULT_WORDS if words is None else words, rng)

    guesses = []
    output_fn(f"WORDLE: Guess the five-letter word in {max_attempts} tries!")
    output_fn("🟩 correct place  🟨 wrong place  ⬛ absent")

    while len(guesses) < max_attempts:
        try:
            guess = input_fn("Enter a guess: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            output_fn("Game cancelled.")
            return {
                "won": False,
                "secret": answer,
                "attempts": len(guesses),
                "guesses": tuple(guesses),
                "cancelled": True
            }

        if not _is_valid_word(guess):
            output_fn("Invalid guess: enter exactly five letters.")
            continue
        
        if guess not in VALID_WORDS and guess != answer:
            output_fn("Invalid guess: not a recognized English word.")
            continue

        guesses.append(guess)
        statuses = _score_guess(answer, guess)
        output_fn(_format_feedback(guess, statuses))

        if guess == answer:
            output_fn(f"You won in {len(guesses)} attempt(s)!")
            return {
                "won": True,
                "secret": answer,
                "attempts": len(guesses),
                "guesses": tuple(guesses),
                "cancelled": False
            }

    output_fn(f"Game over! The word was {answer.upper()}.")
    return {
        "won": False,
        "secret": answer,
        "attempts": len(guesses),
        "guesses": tuple(guesses),
        "cancelled": False
    }

if __name__ == "__main__":
    play_wordle()

