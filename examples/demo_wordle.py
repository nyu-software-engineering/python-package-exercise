from src.mini_games import play_wordle

scripted_guesses = iter(["least", "incur", "pudge", "nutty"])
result = play_wordle(
    max_attempts=3,
    secret="nutty",
    input_fn=lambda prompt: next(scripted_guesses),
)
print("Return value:", result)