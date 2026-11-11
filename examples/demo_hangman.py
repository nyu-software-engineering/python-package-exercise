from games_package.hangman import (
    choose_word,
    check_guess,
    display_word,
    check_game_status,
    start_game
)

def main():
    print("=== Hangman Function Demo ===")

    # 1. Demonstrate choosing a word
    word = choose_word("easy", "animals")
    print("Selected word:", word)

    # Use a fixed word for the remaining examples
    word = "cat"
    guessed_letters = []

    # 2. Demonstrate checking a guess
    result = check_guess(word, "c", guessed_letters)
    print("Guess result:", result)

    # 3. Demonstrate displaying the word
    print("Displayed word:", display_word(word, guessed_letters))

    # 4. Demonstrate checking game status
    print("Game status:", check_game_status(word, guessed_letters))

    # Optionally launch the actual game
    choice = input("\nLaunch Hangman? (y/n): ")

    if choice.lower() == "y":
        start_game()


if __name__ == "__main__":
    main()
