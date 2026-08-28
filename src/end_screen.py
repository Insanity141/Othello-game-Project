import pygame

from constants import *

from ui import (
    get_font,
    draw_text,
    draw_rounded_panel,
)


# =============================================================================
# END SCREEN THEME
# =============================================================================

END_BG = (12, 19, 24)

END_PANEL = (20, 29, 36)
END_PANEL_LIGHT = (27, 39, 47)
END_BORDER = (53, 70, 80)

END_TEXT = (239, 244, 246)
END_TEXT_SECONDARY = (161, 181, 190)
END_TEXT_MUTED = (108, 130, 141)

END_GOLD = (215, 176, 68)
END_GOLD_LIGHT = (240, 204, 104)

END_GREEN = (53, 185, 131)
END_GREEN_DARK = (32, 130, 91)

END_RED = (215, 88, 93)

UI_BLACK = (10, 12, 14)
UI_BLACK_HIGHLIGHT = (57, 62, 66)

UI_WHITE = (240, 243, 240)


# =============================================================================
# BACKGROUND
# =============================================================================

def draw_end_background(screen):

    screen.fill(END_BG)

    glow = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA,
    )

    pygame.draw.circle(
        glow,
        (*END_GOLD, 10),
        (
            WIDTH // 2,
            HEIGHT // 2,
        ),
        250,
    )

    pygame.draw.circle(
        glow,
        (53, 185, 131, 7),
        (
            80,
            HEIGHT - 60,
        ),
        180,
    )

    screen.blit(
        glow,
        (0, 0),
    )


# =============================================================================
# HEADER
# =============================================================================

def draw_end_header(screen):

    center_x = WIDTH // 2

    draw_text(
        screen,
        "OTHELLO",
        (
            center_x,
            42,
        ),
        size=38,
        color=END_TEXT,
        bold=True,
        center=True,
    )

    draw_text(
        screen,
        "STRATEGY • PATIENCE • CONTROL",
        (
            center_x,
            78,
        ),
        size=10,
        color=END_TEXT_MUTED,
        bold=True,
        center=True,
    )

    pygame.draw.line(
        screen,
        END_GOLD,
        (
            center_x - 30,
            101,
        ),
        (
            center_x + 30,
            101,
        ),
        2,
    )


# =============================================================================
# SCORE PIECE
# =============================================================================

def draw_result_piece(
    screen,
    center,
    radius,
    piece_color,
):

    x, y = center

    # Shadow
    pygame.draw.circle(
        screen,
        (5, 8, 10),
        (
            x + 4,
            y + 5,
        ),
        radius,
    )

    # Piece
    pygame.draw.circle(
        screen,
        piece_color,
        center,
        radius,
    )

    # Highlight ring
    highlight = (
        (57, 62, 66)
        if piece_color == UI_BLACK
        else (255, 255, 255)
    )

    pygame.draw.arc(
        screen,
        highlight,
        (
            x - radius + 5,
            y - radius + 5,
            (radius - 5) * 2,
            (radius - 5) * 2,
        ),
        3.5,
        5.8,
        2,
    )


# =============================================================================
# WINNER MESSAGE
# =============================================================================

def get_result_text(
    winner,
    human_player,
):

    if winner == EMPTY:

        return (
            "DRAW",
            END_GOLD_LIGHT,
            "No winner — an even game",
        )

    if winner == human_player:

        return (
            "YOU WIN",
            END_GREEN,
            "Excellent play!",
        )

    return (
        "AI WINS",
        END_RED,
        "Better luck next time!",
    )


# =============================================================================
# SCORE CARDS
# =============================================================================

def draw_final_scores(
    screen,
    board,
    human_player,
):

    # Import here to avoid making the entire
    # module depend on board implementation at import time.
    from board import count_pieces

    black_score, white_score = count_pieces(
        board
    )

    center_x = WIDTH // 2

    card_width = 180
    card_height = 100

    gap = 22

    black_rect = pygame.Rect(
        center_x
        - card_width
        - gap // 2,
        265,
        card_width,
        card_height,
    )

    white_rect = pygame.Rect(
        center_x
        + gap // 2,
        265,
        card_width,
        card_height,
    )

    black_active = (
        human_player == BLACK
    )

    white_active = (
        human_player == WHITE
    )

    draw_rounded_panel(
        screen,
        black_rect,
        fill=END_PANEL_LIGHT,
        border=(
            END_GOLD
            if black_active
            else END_BORDER
        ),
        radius=16,
        border_width=2 if black_active else 1,
    )

    draw_rounded_panel(
        screen,
        white_rect,
        fill=END_PANEL_LIGHT,
        border=(
            END_GOLD
            if white_active
            else END_BORDER
        ),
        radius=16,
        border_width=2 if white_active else 1,
    )

    # Black piece
    draw_result_piece(
        screen,
        (
            black_rect.left + 32,
            black_rect.centery,
        ),
        19,
        UI_BLACK,
    )

    # White piece
    draw_result_piece(
        screen,
        (
            white_rect.left + 32,
            white_rect.centery,
        ),
        19,
        UI_WHITE,
    )

    # Labels
    draw_text(
        screen,
        "BLACK",
        (
            black_rect.left + 62,
            black_rect.top + 18,
        ),
        size=11,
        color=END_TEXT_MUTED,
        bold=True,
    )

    draw_text(
        screen,
        str(black_score),
        (
            black_rect.left + 62,
            black_rect.top + 39,
        ),
        size=28,
        color=END_TEXT,
        bold=True,
    )

    draw_text(
        screen,
        "WHITE",
        (
            white_rect.left + 62,
            white_rect.top + 18,
        ),
        size=11,
        color=END_TEXT_MUTED,
        bold=True,
    )

    draw_text(
        screen,
        str(white_score),
        (
            white_rect.left + 62,
            white_rect.top + 39,
        ),
        size=28,
        color=END_TEXT,
        bold=True,
    )


# =============================================================================
# END SCREEN
# =============================================================================

def draw_end_screen(
    screen,
    board,
    winner,
    human_player,
):

    draw_end_background(
        screen
    )

    draw_end_header(
        screen
    )

    center_x = WIDTH // 2

    # Main result panel
    panel = pygame.Rect(
        center_x - 270,
        125,
        540,
        410,
    )

    draw_rounded_panel(
        screen,
        panel,
        fill=END_PANEL,
        border=END_BORDER,
        radius=22,
        border_width=1,
    )

    # -------------------------------------------------------------------------
    # Game Over
    # -------------------------------------------------------------------------

    draw_text(
        screen,
        "GAME OVER",
        (
            center_x,
            panel.top + 50,
        ),
        size=26,
        color=END_GOLD_LIGHT,
        bold=True,
        center=True,
    )

    winner_text, winner_color, subtitle = (
        get_result_text(
            winner,
            human_player,
        )
    )

    draw_text(
        screen,
        winner_text,
        (
            center_x,
            panel.top + 90,
        ),
        size=32,
        color=winner_color,
        bold=True,
        center=True,
    )

    draw_text(
        screen,
        subtitle,
        (
            center_x,
            panel.top + 123,
        ),
        size=14,
        color=END_TEXT_SECONDARY,
        center=True,
    )

    # -------------------------------------------------------------------------
    # Scores
    # -------------------------------------------------------------------------

    draw_final_scores(
        screen,
        board,
        human_player,
    )

    # -------------------------------------------------------------------------
    # Buttons
    # -------------------------------------------------------------------------

    mouse_pos = pygame.mouse.get_pos()

    play_again_rect = pygame.Rect(
        center_x - 125,
        390,
        250,
        58,
    )

    menu_rect = pygame.Rect(
        center_x - 125,
        460,
        250,
        52,
    )

    play_hovered = play_again_rect.collidepoint(
        mouse_pos
    )

    menu_hovered = menu_rect.collidepoint(
        mouse_pos
    )

    # Play Again
    draw_rounded_panel(
        screen,
        play_again_rect,
        fill=(
            END_GREEN
            if play_hovered
            else END_GREEN_DARK
        ),
        border=END_GREEN,
        radius=14,
        border_width=1,
    )

    draw_text(
        screen,
        "PLAY AGAIN",
        play_again_rect.center,
        size=17,
        color=END_TEXT,
        bold=True,
        center=True,
    )

    # Main Menu
    draw_rounded_panel(
        screen,
        menu_rect,
        fill=(
            END_PANEL_LIGHT
            if menu_hovered
            else END_PANEL
        ),
        border=(
            END_TEXT_SECONDARY
            if menu_hovered
            else END_BORDER
        ),
        radius=14,
        border_width=1,
    )

    draw_text(
        screen,
        "MAIN MENU",
        menu_rect.center,
        size=15,
        color=END_TEXT_SECONDARY,
        bold=True,
        center=True,
    )

    return (
        play_again_rect,
        menu_rect,
    )


# =============================================================================
# END SCREEN LOOP
# =============================================================================

def run_end_screen(
    screen,
    board,
    winner,
    human_player,
):

    clock = pygame.time.Clock()

    while True:

        clock.tick(FPS)

        (
            play_again_rect,
            menu_rect,
        ) = draw_end_screen(
            screen,
            board,
            winner,
            human_player,
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return "QUIT"

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                if play_again_rect.collidepoint(
                    event.pos
                ):

                    return "PLAY_AGAIN"

                if menu_rect.collidepoint(
                    event.pos
                ):

                    return "MENU"

        pygame.display.flip()