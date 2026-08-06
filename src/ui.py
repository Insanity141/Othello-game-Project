import pygame

from constants import *
from board import *
from status import get_status
from ai_stats import get_stats


def draw_board(screen):

    screen.fill(BACKGROUND)

    for row in range(ROWS):
        for col in range(COLS):

            rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, BOARD_GREEN, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)


def draw_pieces(screen, board):

    radius = CELL_SIZE // 2 - 10  # Floor Division

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == EMPTY:
                continue

            center_x = col * CELL_SIZE + CELL_SIZE // 2
            center_y = row * CELL_SIZE + CELL_SIZE // 2

            if board[row][col] == BLACK:
                color = BLACK_COLOR
            else:
                color = WHITE_COLOR

            pygame.draw.circle(screen, color, (center_x, center_y), radius)


def draw_seperator(screen, y):

    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH + 10, y), (WIDTH - 10, y), 2)


def draw_info_panel(screen, board, player, difficulty):

    black_count, white_count = count_pieces(board)

    nodes, pruned, think_time, evaluation, algorithm = get_stats()

    panel = pygame.Rect(BOARD_WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT)

    pygame.draw.rect(screen, INFO_PANEL_COLOR, panel)

    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH, 0), (BOARD_WIDTH, HEIGHT), 3)

    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    heading_font = pygame.font.SysFont("Arial", 22, bold=True)
    font = pygame.font.SysFont("Arial", 20)
    y = 20
    title = title_font.render("OTHELLO AI", True, GOLD)

    screen.blit(title, (BOARD_WIDTH + 45, y))
    y += 45

    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH + 10, y), (WIDTH - 10, y), 2)

    y += 20

    turn = "Black" if player == BLACK else "White"

    screen.blit(
        heading_font.render("Current Turn", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )
    y += 30

    screen.blit(font.render(turn, True, GOLD), (BOARD_WIDTH + 20, y))

    y += 40

    if difficulty == EASY:
        difficulty_text = "Easy"

    elif difficulty == MEDIUM:
        difficulty_text = "Medium"

    else:
        difficulty_text = "Hard"

    screen.blit(
        heading_font.render("Difficulty", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 30

    screen.blit(font.render(difficulty_text, True, BLUE), (BOARD_WIDTH + 20, y))

    y += 40

    screen.blit(
        heading_font.render("Algorithm", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 30

    screen.blit(font.render(algorithm, True, RED), (BOARD_WIDTH + 20, y))

    y += 40

    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH + 10, y), (WIDTH - 10, y), 2)

    y += 20

    screen.blit(heading_font.render("Pieces", True, TEXT_COLOR), (BOARD_WIDTH + 20, y))

    y += 30

    screen.blit(
        font.render(f"Black : {black_count}", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 25

    screen.blit(
        font.render(f"White : {white_count}", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 40

    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH + 10, y), (WIDTH - 10, y), 2)

    y += 20

    screen.blit(
        heading_font.render("AI Statistics", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 30

    screen.blit(
        font.render(f"Nodes : {nodes}", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 25

    screen.blit(
        font.render(f"Pruned : {pruned}", True, TEXT_COLOR), (BOARD_WIDTH + 20, y)
    )

    y += 25

    screen.blit(font.render(f"Score : {evaluation}", True, GOLD), (BOARD_WIDTH + 20, y))

    y += 25

    screen.blit(
        font.render(f"{think_time*1000:.2f} ms", True, BLUE), (BOARD_WIDTH + 20, y)
    )


def draw_game(screen, board, player, difficulty):

    draw_board(screen)
    valid_moves = get_valid_moves(board, player)
    draw_valid_moves(screen, valid_moves)

    draw_pieces(screen, board)
    draw_info_panel(screen, board, player, difficulty)


def draw_valid_moves(screen, valid_moves):

    radius = 8

    for row, col in valid_moves:

        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(screen, (255, 215, 0), (center_x, center_y), radius)
