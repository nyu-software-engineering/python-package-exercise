from games_package.wordle import (
    _is_valid_word,
    _choose_word,
    _score_guess,
    _format_feedback,
    play_wordle
)


def main():
    print("1. Word Validation")
    print("apple:", _is_valid_word("apple"))
    print("cat:", _is_valid_word("cat"))
    print()

    print("2. Choose Word")
    word = _choose_word(["apple", "grape", "peach"])
    print("Selected word:", word)
    print()

    print("3. Score Guess")
    secret = "apple"
    guess = "grape"
    statuses = _score_guess(secret, guess)
    print("Secret:", secret)
    print("Guess:", guess)
    print("Statuses:", statuses)
    print()

    print("4. Format Feedback")
    feedback = _format_feedback(guess, statuses)
    print(feedback)
    print()

    print("5. Play Wordle")
    result = play_wordle()
    print("Game result:", result)


if __name__ == "__main__":
    main()
