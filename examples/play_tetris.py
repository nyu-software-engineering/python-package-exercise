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
            color = colors[board[r][c]] if board[r][c] else (20, 20, 20)
            pygame.draw.rect(screen, color, (c * Cell, r * Cell, Cell-1, Cell-1))
    if piece is not None:
        color = colors[piece["kind"]]
        for r, row in enumerate(piece["shape"]):
            for c, val in enumerate(row):
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

def lock_and_spawn(board, piece, score):
    board = lock_piece(board, piece)
    board, cleared = clear_lines(board)
    score += cleared
    piece = spawn(random.choice(list(colors.keys())))

    if not placement_test(board, piece):
        print("GAME OVER")
        print(f"Final Score: {score}")
        return board, piece, score, False
    return board, piece, score, True

def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("tetris")
    clock = pygame.time.Clock()
    pygame.time.set_timer(pygame.USEREVENT, Fall_event_ms)

    board = create_board(Rows, Cols)
    piece = spawn(random.choice(list(colors.keys())))
    score = 0

    running = True
    move_key = None
    move_started_at = 0
    last_move_at = 0
    DAS = 180
    ARR = 80
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP):
                    piece = try_rotate(board, piece)
                elif event.key == pygame.K_SPACE:
                    piece = drop_piece(board, piece)
                    board, piece, score, running = lock_and_spawn(board, piece, score)
            elif event.type == pygame.USEREVENT:
                candidate = try_move(board, piece, 0, 1)
                if candidate is piece:
                    board, piece, score, running = lock_and_spawn(board, piece, score)
                else:
                    piece = candidate

        keys = pygame.key.get_pressed()
        now = pygame.time.get_ticks()

        held_key = None

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            held_key = "left"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            held_key = "right"
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            held_key = "down"

        if held_key is None:
            move_key = None

        elif held_key != move_key:
            move_key = held_key
            move_started_at = now
            last_move_at = now

            if move_key == "left":
                piece = try_move(board, piece, -1, 0)
            elif move_key == "right":
                piece = try_move(board, piece, 1, 0)
            elif move_key == "down":
                piece = try_move(board, piece, 0, 1)

        elif now - move_started_at >= DAS and now - last_move_at >= ARR:
            if move_key == "left":
                piece = try_move(board, piece, -1, 0)
            elif move_key == "right":
                piece = try_move(board, piece, 1, 0)
            elif move_key == "down":
                piece = try_move(board, piece, 0, 1)

            last_move_at = now

        screen.fill((0, 0, 0))
        draw_board(screen, board, piece)
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()