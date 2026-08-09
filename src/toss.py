import pygame
import random

from constants import *


def draw_toss_screen(screen, selected_choice, result=None, human_won=None):

    screen.fill(BACKGROUND)

    title_font = pygame.font.SysFont("Arial", 42, bold=True)
    heading_font = pygame.font.SysFont("Arial", 28, bold=True)
    font = pygame.font.SysFont("Arial", 26)

    title = title_font.render("COIN TOSS", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

    if result is None:

        heading = heading_font.render("Choose Heads or Tails", True, TEXT_COLOR)

        screen.blit(heading, (WIDTH // 2 - heading.get_width() // 2, 160))

        heads_rect = pygame.Rect(WIDTH // 2 - 230, 250, 180, 65)

        tails_rect = pygame.Rect(WIDTH // 2 + 50, 250, 180, 65)

        heads_color = GOLD if selected_choice == "Heads" else BOARD_GREEN
        tails_color = GOLD if selected_choice == "Tails" else BOARD_GREEN

        pygame.draw.rect(screen, heads_color, heads_rect)
        pygame.draw.rect(screen, GRID_COLOR, heads_rect, 2)

        pygame.draw.rect(screen, tails_color, tails_rect)
        pygame.draw.rect(screen, GRID_COLOR, tails_rect, 2)

        heads_text = font.render("Heads", True, TEXT_COLOR)
        tails_text = font.render("Tails", True, TEXT_COLOR)

        screen.blit(
            heads_text,
            (
                heads_rect.centerx - heads_text.get_width() // 2,
                heads_rect.centery - heads_text.get_height() // 2,
            ),
        )

        screen.blit(
            tails_text,
            (
                tails_rect.centerx - tails_text.get_width() // 2,
                tails_rect.centery - tails_text.get_height() // 2,
            ),
        )

        toss_rect = pygame.Rect(WIDTH // 2 - 110, 380, 220, 60)

        pygame.draw.rect(screen, BLUE, toss_rect)
        pygame.draw.rect(screen, GRID_COLOR, toss_rect, 2)

        toss_text = font.render("Toss Coin", True, TEXT_COLOR)

        screen.blit(
            toss_text,
            (
                toss_rect.centerx - toss_text.get_width() // 2,
                toss_rect.centery - toss_text.get_height() // 2,
            ),
        )

        return heads_rect, tails_rect, toss_rect

    result_text = heading_font.render(f"Result: {result}", True, GOLD)

    screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 190))

    if human_won:
        winner_text = font.render("You won the toss!", True, TEXT_COLOR)

        color_text = font.render("You will play Black", True, GOLD)

    else:
        winner_text = font.render("AI won the toss!", True, TEXT_COLOR)

        color_text = font.render("AI will play Black", True, WHITE_COLOR)

    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, 260))

    screen.blit(color_text, (WIDTH // 2 - color_text.get_width() // 2, 310))

    continue_rect = pygame.Rect(WIDTH // 2 - 120, 400, 240, 60)

    pygame.draw.rect(screen, BOARD_GREEN, continue_rect)
    pygame.draw.rect(screen, GRID_COLOR, continue_rect, 2)

    continue_text = font.render("Start Match", True, TEXT_COLOR)

    screen.blit(
        continue_text,
        (
            continue_rect.centerx - continue_text.get_width() // 2,
            continue_rect.centery - continue_text.get_height() // 2,
        ),
    )

    return continue_rect


def run_toss(screen):

    clock = pygame.time.Clock()

    selected_choice = None
    result = None
    human_won = None

    while True:

        clock.tick(FPS)

        if result is None:
            heads_rect, tails_rect, toss_rect = draw_toss_screen(
                screen, selected_choice
            )

        else:
            continue_rect = draw_toss_screen(screen, selected_choice, result, human_won)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:

                if result is None:

                    if heads_rect.collidepoint(event.pos):
                        selected_choice = "Heads"

                    elif tails_rect.collidepoint(event.pos):
                        selected_choice = "Tails"

                    elif toss_rect.collidepoint(event.pos):

                        if selected_choice is None:
                            continue

                        result = random.choice(["Heads", "Tails"])

                        human_won = selected_choice == result

                else:

                    if continue_rect.collidepoint(event.pos):

                        if human_won:
                            return BLACK, WHITE

                        return WHITE, BLACK

        pygame.display.update()
