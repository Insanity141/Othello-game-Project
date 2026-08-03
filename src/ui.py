import pygame

from constants import *
from board import *
from status import get_status

def draw_board(screen):

    screen.fill(BACKGROUND)

    for row in range(ROWS):
        for col in range(COLS):

            rect = (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            pygame.draw.rect(screen, BOARD_GREEN, rect)
            pygame.draw.rect(screen, GRID_COLOR, rect, 2)


def draw_pieces(screen, board):

    radius = CELL_SIZE // 2 - 10

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

            pygame.draw.circle(
                screen, color, (center_x, center_y), radius
            )

def draw_seperator(screen, y):

    pygame.draw.line(
        screen,
        GRID_COLOR, 
        (BOARD_WIDTH + 10, y), 
        (WIDTH - 10, y), 2 
    )

def draw_info_panel(screen, board, player):

    black_count, white_count = count_pieces(board)

    panel = pygame.Rect(BOARD_WIDTH, 0, INFO_PANEL_WIDTH, HEIGHT)

    pygame.draw.rect(screen, INFO_PANEL_COLOR, panel)

    pygame.draw.line(screen, GRID_COLOR, (BOARD_WIDTH, 0), (BOARD_WIDTH, HEIGHT), 3)

    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    font = pygame.font.SysFont("Arial", 24)

    title = title_font.render("OTHELLO", True, TEXT_COLOR)
    screen.blit(title, (BOARD_WIDTH + 55, 20))

    draw_seperator(screen, 55)
    draw_seperator(screen, 145)
    draw_seperator(screen, 270)
    draw_seperator(screen, 410)

    turn_title = font.render("Current Turn", True, TEXT_COLOR)
    screen.blit(turn_title, (BOARD_WIDTH + 20, 70))

    if player == BLACK:
        turn = "Black Turn"

    else:
        turn = "White Turn"

    turn_text = font.render(turn, True, GOLD)
    screen.blit(turn_text, (BOARD_WIDTH + 20, 100))

    black_text = font.render(
        f"BLACK : {black_count}",
        True, 
        TEXT_COLOR
    )

    white_text = font.render(
        f"White : {white_count}",
        True,
        TEXT_COLOR
    )

    screen.blit(black_text, (BOARD_WIDTH + 20, 190))
    screen.blit(white_text, (BOARD_WIDTH + 20, 220))

    status_title = font.render("Status", True, TEXT_COLOR)
    screen.blit(status_title, (BOARD_WIDTH + 20, 290))

    time = font.render("Timers", True, TEXT_COLOR)
    screen.blit(time, (BOARD_WIDTH + 20, 430))

    pieces_title = font.render("Pieces", True, TEXT_COLOR)
    screen.blit(pieces_title, (BOARD_WIDTH + 20, 160))

    black_timer = font.render(
        "Black : 5:00",
        True, 
        TEXT_COLOR
    )

    white_timer = font.render(
        "White : 5:00",
        True, 
        TEXT_COLOR
    )

    screen.blit(black_timer, (BOARD_WIDTH + 20, 460))
    screen.blit(white_timer, (BOARD_WIDTH + 20, 490))

def draw_game(screen, board, player):

    draw_board(screen)
    valid_moves = get_valid_moves(board, player)
    draw_valid_moves(screen, valid_moves)
    
    draw_pieces(screen, board)
    draw_info_panel(screen, board, player)

def draw_valid_moves(screen, valid_moves):

    radius = 8

    for row, col in valid_moves:

        center_x = col * CELL_SIZE + CELL_SIZE // 2
        center_y = row * CELL_SIZE + CELL_SIZE // 2

        pygame.draw.circle(
            screen,
            (255, 215, 0),
            (center_x, center_y),
            radius
        )