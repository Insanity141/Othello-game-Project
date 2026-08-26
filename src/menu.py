import math
import pygame

from constants import *


difficulty_options = [
    ("Easy", EASY),
    ("Medium", MEDIUM),
    ("Hard", HARD),
]

# -----------------------------------------------------------------------------
# Menu theme
# -----------------------------------------------------------------------------

BG_TOP = (13, 22, 30)
BG_BOTTOM = (24, 38, 48)

PANEL_COLOR = (24, 35, 44)
PANEL_BORDER = (67, 88, 101)

BUTTON_COLOR = (34, 139, 104)
BUTTON_HOVER = (48, 170, 126)
BUTTON_BORDER = (90, 210, 166)

TEXT_PRIMARY = (241, 246, 248)
TEXT_SECONDARY = (166, 184, 194)
TEXT_MUTED = (116, 138, 149)

ACCENT = (213, 176, 67)
ACCENT_SOFT = (235, 204, 117)

DANGER = (182, 68, 72)

DARK_PIECE = (18, 21, 24)
LIGHT_PIECE = (232, 235, 231)


# -----------------------------------------------------------------------------
# Font cache
# -----------------------------------------------------------------------------

_FONT_CACHE = {}


def get_font(size, bold=False):
    key = (size, bold)

    if key not in _FONT_CACHE:
        _FONT_CACHE[key] = pygame.font.SysFont(
            "Arial",
            size,
            bold=bold,
        )

    return _FONT_CACHE[key]


# -----------------------------------------------------------------------------
# Background
# -----------------------------------------------------------------------------

def draw_vertical_gradient(screen):
    """Draw a subtle dark vertical gradient for the menu background."""

    width, height = screen.get_size()

    for y in range(height):

        t = y / max(height - 1, 1)

        color = tuple(
            int(
                BG_TOP[i] * (1 - t)
                + BG_BOTTOM[i] * t
            )
            for i in range(3)
        )

        pygame.draw.line(
            screen,
            color,
            (0, y),
            (width, y),
        )


def draw_soft_circle(
    surface,
    center,
    radius,
    color,
    alpha,
):
    """
    Draw a soft decorative glow behind the board emblem.
    """

    glow = pygame.Surface(
        (radius * 2, radius * 2),
        pygame.SRCALPHA,
    )

    pygame.draw.circle(
        glow,
        (*color, alpha),
        (radius, radius),
        radius,
    )

    surface.blit(
        glow,
        (
            center[0] - radius,
            center[1] - radius,
        ),
    )


# -----------------------------------------------------------------------------
# Othello pieces
# -----------------------------------------------------------------------------

def draw_piece_icon(
    surface,
    center,
    radius,
    color,
):
    """
    Draw a small polished Othello disc
    for the menu emblem.
    """

    x, y = center

    # Shadow
    pygame.draw.circle(
        surface,
        (5, 8, 10),
        (x + 3, y + 5),
        radius,
    )

    # Main disc
    pygame.draw.circle(
        surface,
        color,
        center,
        radius,
    )

    # Highlight
    highlight = tuple(
        min(255, channel + 28)
        for channel in color
    )

    pygame.draw.arc(
        surface,
        highlight,
        (
            x - radius + 5,
            y - radius + 5,
            radius * 2 - 10,
            radius * 2 - 10,
        ),
        math.radians(205),
        math.radians(330),
        2,
    )


# -----------------------------------------------------------------------------
# Text
# -----------------------------------------------------------------------------

def draw_centered_text(
    screen,
    text,
    font,
    color,
    center,
):
    rendered = font.render(
        text,
        True,
        color,
    )

    screen.blit(
        rendered,
        (
            center[0]
            - rendered.get_width() // 2,

            center[1]
            - rendered.get_height() // 2,
        ),
    )


# -----------------------------------------------------------------------------
# Buttons
# -----------------------------------------------------------------------------

def draw_button(
    screen,
    rect,
    text,
    hovered,
    accent=False,
):
    """
    Draw a rounded modern button.
    """

    if accent:

        fill = (
            BUTTON_HOVER
            if hovered
            else BUTTON_COLOR
        )

        border = BUTTON_BORDER

    else:

        fill = (
            (50, 67, 78)
            if hovered
            else (38, 52, 62)
        )

        border = PANEL_BORDER

    # Button body
    pygame.draw.rect(
        screen,
        fill,
        rect,
        border_radius=14,
    )

    # Border
    pygame.draw.rect(
        screen,
        border,
        rect,
        width=1,
        border_radius=14,
    )

    # Button text
    rendered = get_font(
        22,
        bold=True,
    ).render(
        text,
        True,
        TEXT_PRIMARY,
    )

    screen.blit(
        rendered,
        (
            rect.centerx
            - rendered.get_width() // 2,

            rect.centery
            - rendered.get_height() // 2,
        ),
    )


# -----------------------------------------------------------------------------
# Menu layout
# -----------------------------------------------------------------------------

def get_menu_rects():

    center_x = WIDTH // 2

    difficulty_panel = pygame.Rect(
        center_x - 235,
        265,
        470,
        115,
    )

    left_arrow = pygame.Rect(
        difficulty_panel.left + 14,
        difficulty_panel.top + 20,
        66,
        74,
    )

    right_arrow = pygame.Rect(
        difficulty_panel.right - 80,
        difficulty_panel.top + 20,
        66,
        74,
    )

    start_button = pygame.Rect(
        center_x - 150,
        430,
        300,
        64,
    )

    return (
        left_arrow,
        right_arrow,
        start_button,
    )


# -----------------------------------------------------------------------------
# Main menu rendering
# -----------------------------------------------------------------------------

def draw_menu(
    screen,
    selected_index,
):

    # Background
    draw_vertical_gradient(screen)

    width, height = screen.get_size()

    center_x = width // 2

    # -------------------------------------------------------------------------
    # Decorative glows
    # -------------------------------------------------------------------------

    draw_soft_circle(
        screen,
        (
            center_x - 185,
            150,
        ),
        115,
        ACCENT,
        12,
    )

    draw_soft_circle(
        screen,
        (
            center_x + 185,
            150,
        ),
        115,
        BUTTON_BORDER,
        10,
    )

    # -------------------------------------------------------------------------
    # Othello emblem
    # -------------------------------------------------------------------------

    draw_piece_icon(
        screen,
        (
            center_x - 34,
            143,
        ),
        29,
        DARK_PIECE,
    )

    draw_piece_icon(
        screen,
        (
            center_x + 34,
            143,
        ),
        29,
        LIGHT_PIECE,
    )

    # -------------------------------------------------------------------------
    # Title
    # -------------------------------------------------------------------------

    title = get_font(
        54,
        bold=True,
    ).render(
        "OTHELLO",
        True,
        TEXT_PRIMARY,
    )

    screen.blit(
        title,
        (
            center_x
            - title.get_width() // 2,

            38,
        ),
    )

    subtitle = get_font(
        15,
        bold=True,
    ).render(
        "STRATEGY  •  PATIENCE  •  CONTROL",
        True,
        TEXT_SECONDARY,
    )

    screen.blit(
        subtitle,
        (
            center_x
            - subtitle.get_width() // 2,

            98,
        ),
    )

    # -------------------------------------------------------------------------
    # Difficulty panel
    # -------------------------------------------------------------------------

    difficulty_panel = pygame.Rect(
        center_x - 235,
        265,
        470,
        115,
    )

    pygame.draw.rect(
        screen,
        PANEL_COLOR,
        difficulty_panel,
        border_radius=18,
    )

    pygame.draw.rect(
        screen,
        PANEL_BORDER,
        difficulty_panel,
        width=1,
        border_radius=18,
    )

    section_title = get_font(
        14,
        bold=True,
    ).render(
        "DIFFICULTY",
        True,
        TEXT_MUTED,
    )

    screen.blit(
        section_title,
        (
            center_x
            - section_title.get_width() // 2,

            278,
        ),
    )

    # Get button rectangles
    left_arrow, right_arrow, start_button = (
        get_menu_rects()
    )

    # Current mouse position
    mouse_pos = pygame.mouse.get_pos()

    left_hovered = left_arrow.collidepoint(
        mouse_pos
    )

    right_hovered = right_arrow.collidepoint(
        mouse_pos
    )

    start_hovered = start_button.collidepoint(
        mouse_pos
    )

    # -------------------------------------------------------------------------
    # Arrow buttons
    # -------------------------------------------------------------------------

    draw_button(
        screen,
        left_arrow,
        "‹",
        left_hovered,
        accent=False,
    )

    draw_button(
        screen,
        right_arrow,
        "›",
        right_hovered,
        accent=False,
    )

    # -------------------------------------------------------------------------
    # Difficulty name
    # -------------------------------------------------------------------------

    difficulty_name = (
        difficulty_options[selected_index][0]
    )

    difficulty = get_font(
        32,
        bold=True,
    ).render(
        difficulty_name,
        True,
        ACCENT_SOFT,
    )

    screen.blit(
        difficulty,
        (
            center_x
            - difficulty.get_width() // 2,

            318,
        ),
    )

    # -------------------------------------------------------------------------
    # Difficulty description
    # -------------------------------------------------------------------------

    descriptions = {

        EASY:
            "A relaxed opponent for learning the game",

        MEDIUM:
            "A tactical opponent with deeper search",

        HARD:
            "A stronger opponent with advanced search",
    }

    description = get_font(
        14
    ).render(
        descriptions[
            difficulty_options[
                selected_index
            ][1]
        ],
        True,
        TEXT_SECONDARY,
    )

    screen.blit(
        description,
        (
            center_x
            - description.get_width() // 2,

            355,
        ),
    )

    # -------------------------------------------------------------------------
    # Start button
    # -------------------------------------------------------------------------

    draw_button(
        screen,
        start_button,
        "START GAME",
        start_hovered,
        accent=True,
    )

    # -------------------------------------------------------------------------
    # Footer
    # -------------------------------------------------------------------------

    footer = get_font(
        13
    ).render(
        "Choose your difficulty and prepare to play.",
        True,
        TEXT_MUTED,
    )

    screen.blit(
        footer,
        (
            center_x
            - footer.get_width() // 2,

            height - 42,
        ),
    )

    return start_button


# -----------------------------------------------------------------------------
# Mouse handling
# -----------------------------------------------------------------------------

def handle_menu_click(
    mouse_pos,
    selected_index,
):

    left_rect, right_rect, start_rect = (
        get_menu_rects()
    )

    # Previous difficulty
    if left_rect.collidepoint(mouse_pos):

        selected_index = (
            selected_index - 1
        ) % len(difficulty_options)

        return (
            selected_index,
            False,
        )

    # Next difficulty
    if right_rect.collidepoint(mouse_pos):

        selected_index = (
            selected_index + 1
        ) % len(difficulty_options)

        return (
            selected_index,
            False,
        )

    # Start game
    if start_rect.collidepoint(mouse_pos):

        return (
            selected_index,
            True,
        )

    return (
        selected_index,
        False,
    )


# -----------------------------------------------------------------------------
# Menu loop
# -----------------------------------------------------------------------------

def run_menu(screen):

    clock = pygame.time.Clock()

    # Start on Hard
    selected_index = 2

    while True:

        clock.tick(FPS)

        start_game = False

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                selected_index, start_game = (
                    handle_menu_click(
                        event.pos,
                        selected_index,
                    )
                )

                if start_game:
                    return difficulty_options[
                        selected_index
                    ][1]

        draw_menu(
            screen,
            selected_index,
        )

        pygame.display.flip()