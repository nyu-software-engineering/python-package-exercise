import random
import sys
import pygame
from games_package.tetris_logic import (shapes, colors, placement_test, create_board, rotate_piece, new_piece, drop_piece, lock_piece, clear_lines)

Cell = 30
Cols = 10
Rows = 20
width = Cols * Cell
height = Rows * Cell
FPS = 60
Fall_event_ms = 500

def draw_board(screen, board, piece):
    for r in range(Rows):
        for c in range(Cols):
            color = (40, 40, 40) if board[r][c] else (20, 20, 20)
            pygame.draw.rect(screen, color, (c * Cell, r * Cell, Cell-1, Cell-1))
    if piece is not None:
        color = colors[piece["kind"]]
        for c, val in enumerate(piece["shape"]):
            if val:
                pr = piece["y"] + r
                pc = piece["x"] + c
                if 0<= pr < Rows and 0<= pc < Cols:
                    pygame.draw.rect(screen, color, (pc*Cell, pr*Cell, Cell-1, Cell-1))

def spawn(kind):
    return new_piece(kind, Cols//2 - 1, 0)

def try_move(board, piece, dx, dy):
    candidate = {**piece, "x": piece["x"] + dx, "y": piece["y"] + dy}
    return candidate if placement_test(board, candidate) else piece

def try_rotate(board, piece):
    rotated = rotate_piece(piece, "cw")
    if placement_test(board, rotated):
        return rotated
    for dx in (-1,1):
        kicked = {**rotated, "x": rotated["x"] + dx}
        if placement_test(board, kicked):
            return kicked
    return piece

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_cpation("tetris")
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, Fall_event_ms)

    board = create_board(Rows, Cols)
    piece = spawn(random.choice(list(colors.keys())))
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_a, pygame.K_LEFT):
                    piece = try_move(board, piece, -1, 0)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    piece = try_move(board, piece, 1, 0)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    piece = try_move(board, piece, 0, 1)
                elif event.key in (pygame.K_w, pygame.K_UP):
                    piece = try_rotate(board, piece)
                elif event.key == pygame.K_SPACE:
                    piece = drop_piece(board, piece)
            elif event.type == pygame.USEREVENT:
                candidate = try_move(board, piece, 0, 1)
                if candidate is piece:
                    board = lock_piece(board, piece)
                    board, cleared = clear_lines(board)
                    score += cleared
                    piece = spawn(random.choice(list(colors.keys())))
                    if not placement_test(board, piece):
                        print(f"Game Over. Score: {score}")
                        running = False
                    else:
                        piece = candidate
        screen.fill((0, 0, 0))
        draw_board(screen, board, piece)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()