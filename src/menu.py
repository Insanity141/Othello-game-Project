import pygame
from constants import *

difficulty_options = [
    ("Easy", EASY),
    ("Medium", MEDIUM),
    ("Hard", HARD)
]

def draw_menu(screen, selected_index):

    screen.fill(BACKGROUND)

    title_font = pygame.font.SysFont("Arial", 42, bold=True)
    heading_font = pygame.font.SysFont("Arial", 28, bold=True)
    font = pygame.font.SysFont("Arial", 30)

    title = title_font.render("Othello AI", True, GOLD)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 70))

    heading = heading_font.render("Difficulty", True, TEXT_COLOR)
    screen.blit(heading, (WIDTH // 2 - heading.get_width() // 2, 180))

    difficulty_name = difficulty_options[selected_index][0]

    left_arrow = font.render("◄", True, TEXT_COLOR)
    right_arrow = font.render("►", True, TEXT_COLOR)

    difficulty = font.render(difficulty_name, True, GOLD)

    screen.blit(left_arrow, (WIDTH // 2 - 120, 250))
    screen.blit(difficulty, (WIDTH // 2 - difficulty.get_width() // 2, 250))
    screen.blit(right_arrow, (WIDTH // 2 + 90, 250))

    start_rect = pygame.Rect(WIDTH // 2 - 110, 360, 220, 60)

    pygame.draw.rect(screen, BOARD_GREEN, start_rect)
    pygame.draw.rect(screen, GRID_COLOR, start_rect, 2)

    start_text = font.render("Start Game", True, TEXT_COLOR)

    screen.blit(start_text,
        (
            start_rect.centerx - start_text.get_width() // 2,
            start_rect.centery - start_text.get_height() // 2,
        ),
    )

    return start_rect

def get_menu_rects():

    left_arrow = pygame.Rect(WIDTH // 2 - 130, 250, 40, 40)
    right_arrow = pygame.Rect(WIDTH // 2 + 90, 250, 40, 40)
    start_button = pygame.Rect(WIDTH // 2 - 110, 360, 220, 60)

    return left_arrow, right_arrow, start_button

def handle_menu_click(mouse_pos, selected_index):

    left_rect, right_rect, start_rect = get_menu_rects()

    if left_rect.collidepoint(mouse_pos):

        selected_index = (selected_index - 1) % len(difficulty_options)
        return selected_index, False

    if right_rect.collidepoint(mouse_pos):

        selected_index = (selected_index + 1) % len(difficulty_options)
        return selected_index, False

    if start_rect.collidepoint(mouse_pos):
        return selected_index, True

    return selected_index, False

def run_menu(screen):

    clock = pygame.time.Clock()

    selected_index = 2

    selected_difficulty = difficulty_options[selected_index][1]

    running = True

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.MOUSEBUTTONDOWN:

                selected_index, start_game = handle_menu_click(event.pos, selected_index)

                selected_difficulty = difficulty_options[selected_index][1]

                if start_game:
                    return selected_difficulty
            
        draw_menu(screen, selected_index)

        pygame.display.update()