import pytest
from games_package.tetris_logic import (shapes, placement_test, create_board, rotate_piece, new_piece, drop_piece, lock_piece, clear_lines)

#testing board
def test_create_board_size():
    board = create_board(20, 10)
    assert len(board) == 20
    assert all(len(row) == 10 for row in board)

def test_create_board_empty():
    board = create_board(4, 4)
    assert all(cell == 0 for row in board for cell in row)

#testing piece creation
def test_new_piece_shape():
    p1 = new_piece("T", 3, 0)
    p2 = new_piece("T", 3, 0)
    assert p1["shape"] == p2["shape"]
    assert p1["shape"] is not p2["shape"]

def test_new_piece_attributes():
    p=new_piece("O", 4, 1)
    assert p["kind"] == "O"
    assert p["x"] == 4 and p["y"] == 1
    assert p["shape"] == shapes["O"]

#testing piece rotation
def test_rotate_t_cw():
    p = new_piece("T", 0, 0)
    rotated = rotate_piece(p, "cw")
    assert rotated["shape"] == [[1,0], [1,1], [1,0]]

def test_rotate_twice_for_identity_for_t():
    p = new_piece("T", 0, 0)
    origin = [row[:] for row in p["shape"]]
    rotate_piece(p, "cw")
    assert p["shape"] == origin

#testing placement test
def test_placement_on_empty_board():
    board = create_board(5, 5)
    p = new_piece("O", 1, 1)
    assert placement_test(board, p)

def test_out_of_bound():
    board = create_board(5, 5)
    p = new_piece("O", 4, 4)
    assert not placement_test(board, p)

def test_negative_position_placement():
    board = create_board(5,5)
    p = new_piece("O", -1, 0)
    assert not placement_test(board, p)

def test_overlapping_placement():
    board = create_board(5, 5)
    board[2][2] = 1
    p = new_piece("O", 1, 1)
    assert not placement_test(board, p)

#testing lock piece
def test_lock_piece_marks_cell():
    board = create_board(5, 5)
    p = new_piece("O", 1, 1)
    locked = lock_piece(board, p)
    assert locked[1][1] == 1 and locked[1][2] == 1
    assert locked[2][1] == 1 and locked[2][2] == 1

def test_lock_prevent_mutate_original():
    board = create_board(5, 5)
    p = new_piece("O", 1, 1)
    lock_piece(board, p)
    assert all(cell == 0 for row in board for cell in row)

#testing clear line
def test_clear_lines_none():
    board = create_board(4, 3)
    new_board, cleared = clear_lines(board)
    assert cleared == 0
    assert new_board == board

def test_clear_lines_one():
    board = create_board(3,3)
    board[2] = [1,1,1]
    new_board, cleared = clear_lines(board)
    assert cleared == 1
    assert new_board[0] == [0,0,0]
    assert new_board[1] == [0,0,0]
    assert new_board[2] == [0,0,0]

def test_clear_multiple_lines():
    board = create_board(4,3)
    board[1] = [1,1,1]
    board[3] = [1,1,1]
    new_board, cleared = clear_lines(board)
    assert cleared == 2
    assert len(new_board) == 4

def test_clear_empty_board():
    assert clear_lines([]) == ([], 0)

#test drop piece
def test_drop_to_bottom():
    board = create_board(5,5)
    p = new_piece("O", 0, 0)
    dropped = drop_piece(board, p)
    assert dropped["y"] == 3

def test_drop_stops_on_block():
    board = create_board(5,5)
    board[4][0] = 1
    p = new_piece("I", 0, 0)
    dropped = drop_piece(board, p)
    assert dropped["y"] == 3

def test_drop_invalid_returns_unchanged():
    board = create_board(3, 3)
    p = new_piece("O", 5, 5)
    dropped = drop_piece(board, p)
    assert dropped["y"] == 5
