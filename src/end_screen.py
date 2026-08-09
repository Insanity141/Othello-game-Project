import pygame

from constants import *
from board import count_pieces


def draw_end_screen(screen, board, winner, human_player, ai_player):

    screen.fill(BACKGROUND)

    black_count, white_count = count_pieces(board)

    title_font = pygame.font.SysFont("Arial", 44, bold=True)

    heading_font = pygame.font.SysFont("Arial", 30, bold=True)

    font = pygame.font.SysFont("Arial", 24)

    title = title_font.render("GAME OVER", True, GOLD)

    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 60))

    if winner == EMPTY:

        winner_text = "Draw!"

    elif winner == human_player:

        winner_text = "You Win!"

    else:

        winner_text = "AI Wins!"

    result = heading_font.render(winner_text, True, TEXT_COLOR)

    screen.blit(result, (WIDTH // 2 - result.get_width() // 2, 145))

    if winner == BLACK:

        color_result = "Black Wins"

    elif winner == WHITE:

        color_result = "White Wins"

    else:

        color_result = "Equal Pieces"

    color_text = font.render(color_result, True, GOLD)

    screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, 195))

    score_title = heading_font.render("Final Score", True, TEXT_COLOR)

    screen.blit(score_title, (WIDTH // 2 - score_title.get_width() // 2, 265))

    black_text = font.render(f"Black : {black_count}", True, TEXT_COLOR)

    white_text = font.render(f"White : {white_count}", True, TEXT_COLOR)

    screen.blit(black_text, (WIDTH // 2 - black_text.get_width() // 2, 315))

    screen.blit(white_text, (WIDTH // 2 - white_text.get_width() // 2, 350))

    play_again_rect = pygame.Rect(WIDTH // 2 - 240, 445, 210, 60)

    exit_rect = pygame.Rect(WIDTH // 2 + 30, 445, 210, 60)

    pygame.draw.rect(screen, BOARD_GREEN, play_again_rect)

    pygame.draw.rect(screen, GRID_COLOR, play_again_rect, 2)

    pygame.draw.rect(screen, RED, exit_rect)

    pygame.draw.rect(screen, GRID_COLOR, exit_rect, 2)

    play_text = font.render("Play Again", True, TEXT_COLOR)

    exit_text = font.render("Exit", True, TEXT_COLOR)

    screen.blit(
        play_text,
        (
            play_again_rect.centerx - play_text.get_width() // 2,
            play_again_rect.centery - play_text.get_height() // 2,
        ),
    )

    screen.blit(
        exit_text,
        (
            exit_rect.centerx - exit_text.get_width() // 2,
            exit_rect.centery - exit_text.get_height() // 2,
        ),
    )

    return play_again_rect, exit_rect


def run_end_screen(screen, board, winner, human_player, ai_player):

    clock = pygame.time.Clock()

    while True:

        clock.tick(FPS)

        play_again_rect, exit_rect = draw_end_screen(
            screen, board, winner, human_player, ai_player
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:

                if play_again_rect.collidepoint(event.pos):
                    return True

                if exit_rect.collidepoint(event.pos):
                    return False

        pygame.display.update()
