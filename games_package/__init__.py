from games_package.tetris_logic import(
    create_board,
    new_piece, 
    drop_piece,
    lock_piece,
    rotate_piece,
    placement_test,
    clear_lines
)

from games_package.hangman import (
    choose_word,
    check_guess,
    display_word,
    check_game_status
)

__all__ = [
    "create_board",
    "new_piece",
    "drop_piece",
    "lock_piece",
    "rotate_piece",
    "placement_test",
    'clear_lines',
    "choose_word",
    "check_guess",
    "display_word",
    "check_game_status"
]
