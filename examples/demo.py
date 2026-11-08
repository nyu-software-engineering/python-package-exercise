from games_package.tetris_logic import(
    create_board,
    new_piece, 
    drop_piece,
    lock_piece,
    rotate_piece,
    placement_test,
    clear_lines
)


board = create_board(6, 4)
piece = new_piece("T", 1, 0)
print("Initial board:", board)
print("Can place T:", placement_test(board, piece))
print("Rotated T:", rotate_piece(piece, "cw")["shape"])
board = lock_piece(board, piece)
print("Board after lock:", board)
print("After clearing line", clear_lines(board))
print("Dropped piece y:", drop_piece(create_board(6, 4), piece)["y"])


