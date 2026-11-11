from games_package.tetris_logic import(
    create_board,
    new_piece, 
    drop_piece,
    lock_piece,
    rotate_piece,
    placement_test,
    clear_lines
)

#demo new 6x4 board works, using a smaller board for easier visualization
board = create_board(6, 4)

#demo piece or tetrominoes could be created, placed, and rotated
piece = new_piece("T", 1, 0)
print("Initial board:", board)
print("Can place T:", placement_test(board, piece))
print("Rotated T:", rotate_piece(piece, "cw")["shape"])

#demo for locking, clearing lines, and droping the tetrominoes
board = lock_piece(board, piece)
print("Board after lock:", board)
print("After clearing line", clear_lines(board))
print("Dropped piece y:", drop_piece(create_board(6, 4), piece)["y"])


