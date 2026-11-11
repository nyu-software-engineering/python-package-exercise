# team-a-games-package

A lighthearted collection of terminal and pygame mini-games, package as a single installable python library. Includes **Tetris**, **Hangman**, **Wordle**, **2048**, and **Blackjack**.

Playable from the terminal after 'pip install team-a-games-package==0.1.0':

    play_tetris
    play_hangman
    play_wordle
    play_2048
    play_blackjack

Pypi: [Team-a minigames](https://pypi.org/project/team-a-games-package/0.1.0/)

## Installation
**Requirements:** Python 3.11+

    pip install team-a-games-package==0.1.0

This install 'pygame' and 'pyspellchecker' automatically as dependencies 

### Run a game
    play_tetris     # Tetris (pygame window)
    play_hangman    # Hangman (pygame window)
    play_wordle     # Wordle (terminal)
    play_2048       # 2048 (terminal)
    play_blackjack  # blackjack (terminal)

### Use the library in your own code

All game logic functions are importable:

```python
from games_package import(
    # Tetris
    create_board, new_piece,  drop_piece, lock_piece, rotate_piece, placement_test, clear_lines，
    # Wordle
    _is_valid_word, _choose_word, _score_guess, _format_feedback，
    # Hangman
    choose_word, check_guess, display_word, check_game_status，
    # Blackjack
    create_deck, display_hand, play_blackjack, shuffle_deck, sum_hand，
    # 2048
    add_random_tile, create_board, has_won, is_game_over, move， new_game,
)
```
---

## Playing the games

Each game has a concsole command and all commands work from any directory while the virtual environment is actived.

| Game | Command | Interface |
|---|---|---|
| Tetris | `play_tetris` | pygame window |
| Hangman | `play_hangman` | pygame window|
| Wordle | `play_worlde` | terminal |
| 2048 | `play_2048` | terminal |
| Blackjacl | `play_blackjack`| terminal |

You can also launch games via Python's module runner:

    python -m games_package.tetris
    python -m games_package.hangman
    python -m games_package.wordle
    python -m games_package.game_2048
    python -m games_package.blackjack

## Contributing (for anyone who want to work on it)

### Setup

Requirements: **Python 3.11+**, **Git**, **pipenv**.

    git clone https://github.com/software-students-fall2026/python-package-exercise-team-a
    cd python-package-exercise-team-a

    pipenv install --dev                #installs dev dependencies from Pipfile
    pinenv run pip install -e.          # installs the package itself

### Run tests

    pipenv run pytest -v

### Buld the package locally
If uploading to the PyPi

    pipenv run python -m build          # build create the package artifacts/files
    pipenv run twine check dist/*       # twine upload the package to pypi

### Clean up

    pipenv --rm

## Environment variable and secrets
This project requires **no enviorment variables** and **no secret configuration files**. Also no database and no external service authentication. Every game runs offline with only its python dependencies installed.

## Team

- [Andy Chi](https://github.com/ac11238)
- [Kathy Lin](https://github.com/lkykathy)
- [Sean Alliman](https://github.com/SeanA12)
- [Tyler Wu](https://github.com/uwtz)
- [Monica Lee](http://github.com/monica9482)