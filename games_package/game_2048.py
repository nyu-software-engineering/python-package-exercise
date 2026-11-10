"""2048 game logic and a small terminal interface."""

import os
import random
import sys
from typing import Optional

Board = list[list[int]]
GRID_SIZE = 4
TARGET_TILE = 2048


def _validate_board(board: Board) -> None:
    if not board or any(len(row) != len(board) for row in board):
        raise ValueError("board must be a non-empty square grid")
    if any(type(tile) is not int or tile < 0 for row in board for tile in row):
        raise ValueError("tiles must be non-negative integers")


def create_board(size: int = GRID_SIZE) -> Board:
    """Return an empty square board."""
    if type(size) is not int or size < 1:
        raise ValueError("size must be a positive integer")
    return [[0] * size for _ in range(size)]


def _merge_row_left(row: list[int]) -> tuple[list[int], int]:
    tiles = [tile for tile in row if tile]
    merged: list[int] = []
    score_gained = 0
    index = 0

    while index < len(tiles):
        if index + 1 < len(tiles) and tiles[index] == tiles[index + 1]:
            value = tiles[index] * 2
            merged.append(value)
            score_gained += value
            # Skip both inputs so the new tile cannot merge again this turn.
            index += 2
        else:
            merged.append(tiles[index])
            index += 1

    return merged + [0] * (len(row) - len(merged)), score_gained


def _transpose(board: Board) -> Board:
    return [list(column) for column in zip(*board)]


def move(board: Board, direction: str) -> tuple[Board, int]:
    """Slide and merge tiles; return the new board and score gained.

    The input board is not modified. Direction is one of left, right, up, down.
    """
    _validate_board(board)
    if direction not in {"left", "right", "up", "down"}:
        raise ValueError("direction must be left, right, up, or down")

    # Convert vertical moves to row moves, then reverse rows for right/down.
    working = _transpose(board) if direction in {"up", "down"} else [row[:] for row in board]
    reverse = direction in {"right", "down"}
    moved_rows: list[list[int]] = []
    score_gained = 0

    for row in working:
        source = row[::-1] if reverse else row
        merged, row_score = _merge_row_left(source)
        moved_rows.append(merged[::-1] if reverse else merged)
        score_gained += row_score

    result = _transpose(moved_rows) if direction in {"up", "down"} else moved_rows
    return result, score_gained


def add_random_tile(board: Board, rng: Optional[random.Random] = None) -> Board:
    """Return a copy with a 2 (90%) or 4 (10%) in a random empty cell."""
    _validate_board(board)
    generator = rng if rng is not None else random
    result = [row[:] for row in board]
    empty_cells = [
        (row_index, column_index)
        for row_index, row in enumerate(result)
        for column_index, tile in enumerate(row)
        if tile == 0
    ]
    if empty_cells:
        row_index, column_index = generator.choice(empty_cells)
        result[row_index][column_index] = 2 if generator.random() < 0.9 else 4
    return result


def new_game(size: int = GRID_SIZE, rng: Optional[random.Random] = None) -> Board:
    """Create a board with two initial tiles."""
    board = create_board(size)
    return add_random_tile(add_random_tile(board, rng), rng)


def has_won(board: Board, target: int = TARGET_TILE) -> bool:
    """Return whether the target tile is present."""
    _validate_board(board)
    return any(tile >= target for row in board for tile in row)


def is_game_over(board: Board) -> bool:
    """Return whether no empty cell or matching adjacent pair remains."""
    _validate_board(board)
    if any(tile == 0 for row in board for tile in row):
        return False

    for row_index, row in enumerate(board):
        for column_index, tile in enumerate(row):
            if column_index + 1 < len(row) and tile == row[column_index + 1]:
                return False
            if row_index + 1 < len(board) and tile == board[row_index + 1][column_index]:
                return False
    return True


def _read_key() -> str:
    if os.name == "nt":
        import msvcrt

        # Windows provides a direct single-key console read.
        key = msvcrt.getwch()
        if key in {"\x00", "\xe0"}:
            msvcrt.getwch()
            return ""
        return key

    import termios
    import tty

    file_descriptor = sys.stdin.fileno()
    previous_settings = termios.tcgetattr(file_descriptor)
    try:
        # Raw mode delivers one key immediately instead of waiting for Enter.
        tty.setraw(file_descriptor)
        return sys.stdin.read(1)
    finally:
        # Restore normal line input even if reading is interrupted.
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, previous_settings)


def _render(board: Board, score: int, message: str = "") -> None:
    cell_width = max(4, max(len(str(tile)) for row in board for tile in row))
    border = "+" + "+".join("-" * (cell_width + 2) for _ in board) + "+"

    print("\033[2J\033[H", end="")
    print(f"2048    Score: {score}\n")
    print(border)
    for row in board:
        print("|" + "|".join(f" {tile:>{cell_width}} " for tile in row) + "|")
        print(border)
    print("\nPress W/A/S/D to move. Q to quit.")
    if message:
        print(message)


def play_2048(size: int = GRID_SIZE) -> None:
    """Run the terminal game with immediate W/A/S/D keypresses."""
    board = new_game(size)
    score = 0
    message = ""
    announced_win = False
    directions = {"w": "up", "a": "left", "s": "down", "d": "right"}

    while True:
        _render(board, score, message)
        if is_game_over(board):
            print(f"Game over. Final score: {score}")
            return

        try:
            print("Move: ", end="", flush=True)
            command = _read_key().lower()
            # Ctrl-C is read as a character while the terminal is in raw mode.
            if command == "\x03":
                raise KeyboardInterrupt
            print(command)
        except (EOFError, KeyboardInterrupt):
            print("\nGame ended.")
            return

        if command == "q":
            print(f"Quit game. Final score: {score}")
            return
        if command not in directions:
            message = "Please enter W, A, S, D, or Q."
            continue

        next_board, score_gained = move(board, directions[command])

        board = add_random_tile(next_board)
        score += score_gained
        message = ""
        if not announced_win and has_won(board):
            message = "You reached 2048! Keep playing or press Q to quit."
            announced_win = True


if __name__ == "__main__":
    play_2048()