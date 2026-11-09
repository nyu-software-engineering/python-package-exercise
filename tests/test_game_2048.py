import random

import pytest

from games_package.game_2048 import (
    add_random_tile,
    create_board,
    has_won,
    is_game_over,
    move,
    new_game,
)


def test_create_board_default_and_custom_size():
    assert create_board() == [[0] * 4 for _ in range(4)]
    assert create_board(2) == [[0, 0], [0, 0]]


@pytest.mark.parametrize("size", [0, -1, 1.5, True])
def test_create_board_rejects_invalid_size(size):
    with pytest.raises(ValueError):
        create_board(size)


def test_move_left_merges_each_tile_once_and_scores():
    board = [[2, 2, 2, 2], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    moved, score_gained = move(board, "left")

    assert moved[0] == [4, 4, 0, 0]
    assert score_gained == 8


@pytest.mark.parametrize(
    ("direction", "start", "destination"),
    [
        ("left", (0, 2), (0, 0)),
        ("right", (0, 1), (0, 3)),
        ("up", (3, 1), (0, 1)),
        ("down", (0, 2), (3, 2)),
    ],
)
def test_move_slides_in_each_direction(direction, start, destination):
    board = create_board()
    board[start[0]][start[1]] = 2

    moved, score_gained = move(board, direction)

    assert moved[destination[0]][destination[1]] == 2
    assert sum(tile != 0 for row in moved for tile in row) == 1
    assert score_gained == 0


def test_move_preserves_input_and_rejects_invalid_inputs():
    board = [[2, 0], [0, 0]]
    original = [row[:] for row in board]

    moved, _ = move(board, "left")

    assert board == original
    assert moved is not board
    with pytest.raises(ValueError):
        move(board, "diagonal")
    with pytest.raises(ValueError):
        move([[2, 0], [0]], "left")


def test_add_random_tile_places_only_a_two_or_four_without_mutating_input():
    board = [[2, 0], [0, 0]]

    result = add_random_tile(board, random.Random(12))

    added_tiles = [
        result[row_index][column_index]
        for row_index, row in enumerate(board)
        for column_index, tile in enumerate(row)
        if tile == 0 and result[row_index][column_index] != 0
    ]
    assert sum(tile != 0 for row in result for tile in row) == 2
    assert len(added_tiles) == 1
    assert added_tiles[0] in {2, 4}
    assert board == [[2, 0], [0, 0]]
    assert add_random_tile([[2, 4], [8, 16]]) == [[2, 4], [8, 16]]


def test_new_game_starts_with_two_tiles():
    board = new_game(rng=random.Random(42))

    assert len(board) == 4
    assert all(len(row) == 4 for row in board)
    assert sum(tile != 0 for row in board for tile in row) == 2
    assert all(tile in {0, 2, 4} for row in board for tile in row)


def test_win_and_game_over_detection():
    assert has_won([[2, 4], [8, 16]], target=16)
    assert not has_won([[2, 4], [8, 16]])
    assert not is_game_over([[2, 0], [8, 16]])
    assert not is_game_over([[2, 4], [8, 8]])
    assert is_game_over([[2, 4], [8, 16]])