#logic for board, pieces, movmeent

#the 7 shapes w/ color in tetris, also called tetrominoes
shapes = {
    "I": [[1,1,1,1]],
    "O": [[1,1], [1,1]],
    "T": [[0,1,0], [1,1,1]],
    "S": [[0,1,1], [1,1,0]],
    "Z": [[1,1,0], [0,1,1]],
    "J": [[1,0,0], [1,1,1]],
    "L": [[0,0,1], [1,1,1]]
}

colors = {
    "I": (0, 240, 240),
    "O": (240, 240, 0),
    "T": (160, 0, 240),
    "S": (0, 240, 0),
    "Z": (240, 0, 0),
    "J": (0, 0, 240),
    "L": (240, 160, 0)
}

def create_board(rows: int=20, cols: int = 10) -> list[list[int]]:
    return [[0] * cols for _ in range(rows)]

def new_piece(kind: str, x: int, y: int) -> dict:
    return{
        "kind": kind,
        "shape": [row[:] for row in shapes[kind]],
        "x": x,
        "y": y
    }

def rotate_piece(piece: dict, direction: str = "cw") -> dict:
    shape = piece["shape"]
    if direction == "cw":
        rotated = [list(row) for row in zip(*shape[::-1])]
    else:
        rotated = [list(row) for row in zip(*shape)][::-1]
    return {**piece, "shape":rotated}

def placement_test(board: list[list[int]], piece: dict) -> bool:
    rows = len(board)
    cols = len(board[0]) if rows else 0
    for r, row in enumerate(piece["shape"]):
        for c, val in enumerate(row):
            if not val:
                continue
            br = piece["y"] + r
            bc = piece["x"] + c
            if br<0 or br>= rows or bc < 0 or bc >= cols:
                return False
            if board[br][bc]:
                return False
    return True

def lock_piece(board: list[list[int]], piece: dict) -> list[list[int]]:
    new_board = [row[:] for row in board]
    for r, row in enumerate(piece["shape"]):
        for c, val in enumerate(row):
            if val:
                new_board[piece["y"] + r][piece["x"]+c] = piece["kind"]
    return new_board

def clear_lines(board: list[list[int]]) -> tuple[list[list[int]], int]:
    if not board:
        return board, 0
    cols = len(board[0])
    kept = [row for row in board if not all(row)]
    cleared = len(board) - len(kept)
    new_board = [[0] * cols for _ in range(cleared)] + kept
    return new_board, cleared

def drop_piece(board: list[list[int]], piece: dict) -> dict:
    if not placement_test(board, piece):
        return {**piece}
    moved = {**piece}
    while True:
        candidate = {**moved, "y": moved["y"]+1}
        if not placement_test(board, candidate):
            return moved
        moved = candidate