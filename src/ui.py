import pygame

from constants import *
from board import count_pieces, get_valid_moves, get_flipable_pieces
from ai_stats import get_stats


# =============================================================================
# THEME
# =============================================================================

BG_COLOR = (12, 19, 24)
PANEL_COLOR = (20, 29, 36)
PANEL_LIGHT = (27, 39, 47)
PANEL_BORDER = (53, 70, 80)

BOARD_COLOR = (31, 114, 83)
BOARD_DARK = (24, 91, 67)
BOARD_EDGE = (12, 45, 37)
GRID_COLOR = (19, 66, 51)

UI_WHITE = (240, 243, 240)
UI_WHITE_SOFT = (210, 217, 214)

UI_BLACK = (20, 23, 26)
UI_BLACK_SOFT = (10, 12, 14)

ACCENT = (215, 176, 68)
ACCENT_BRIGHT = (240, 204, 104)

GREEN = (53, 185, 131)
GREEN_DARK = (32, 130, 91)

TEXT_PRIMARY = (239, 244, 246)
TEXT_SECONDARY = (161, 181, 190)
TEXT_MUTED = (108, 130, 141)

RED = (215, 88, 93)
BLUE = (92, 164, 235)

MOVE_HINT = (235, 196, 74)


# =============================================================================
# FONT CACHE
# =============================================================================

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


# =============================================================================
# SMALL DRAWING HELPERS
# =============================================================================

def draw_text(
    screen,
    text,
    position,
    size=18,
    color=TEXT_PRIMARY,
    bold=False,
    center=False,
):

    font = get_font(size, bold)

    surface = font.render(
        text,
        True,
        color,
    )

    if center:

        rect = surface.get_rect(
            center=position
        )

        screen.blit(
            surface,
            rect,
        )

    else:

        screen.blit(
            surface,
            position,
        )

def draw_right_text(
    screen,
    text,
    position,
    size=18,
    color=TEXT_PRIMARY,
    bold=False,
):
    font = get_font(size, bold)

    surface = font.render(
        text,
        True,
        color,
    )

    rect = surface.get_rect(
        midright=position
    )

    screen.blit(
        surface,
        rect,
    )

def draw_rounded_panel(
    screen,
    rect,
    fill=PANEL_COLOR,
    border=PANEL_BORDER,
    radius=16,
    border_width=1,
):

    pygame.draw.rect(
        screen,
        fill,
        rect,
        border_radius=radius,
    )

    if border_width > 0:

        pygame.draw.rect(
            screen,
            border,
            rect,
            width=border_width,
            border_radius=radius,
        )


def draw_separator(
    screen,
    x1,
    y,
    x2,
    color=PANEL_BORDER,
    width=1,
):

    pygame.draw.line(
        screen,
        color,
        (x1, y),
        (x2, y),
        width,
    )


# =============================================================================
# BACKGROUND
# =============================================================================

def draw_background(screen):

    screen.fill(BG_COLOR)

    # Slightly lighter top area
    pygame.draw.rect(
        screen,
        (15, 24, 30),
        (0, 0, WIDTH, 82),
    )

    # Decorative circles
    glow = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA,
    )

    pygame.draw.circle(
        glow,
        (215, 176, 68, 10),
        (BOARD_WIDTH - 70, 60),
        180,
    )

    pygame.draw.circle(
        glow,
        (53, 185, 131, 8),
        (WIDTH - 40, HEIGHT - 100),
        220,
    )

    screen.blit(
        glow,
        (0, 0),
    )


# =============================================================================
# BOARD
# =============================================================================

def get_cell_rect(row, col):

    return pygame.Rect(
        col * CELL_SIZE,
        row * CELL_SIZE,
        CELL_SIZE,
        CELL_SIZE,
    )


def draw_board(screen):

    draw_background(screen)

    # Board outer shadow
    board_outer = pygame.Rect(
        8,
        8,
        BOARD_WIDTH - 16,
        BOARD_HEIGHT - 16,
    )

    pygame.draw.rect(
        screen,
        BOARD_EDGE,
        board_outer,
        border_radius=20,
    )

    # Board surface
    board_surface = pygame.Rect(
        14,
        14,
        BOARD_WIDTH - 28,
        BOARD_HEIGHT - 28,
    )

    pygame.draw.rect(
        screen,
        BOARD_DARK,
        board_surface,
        border_radius=16,
    )

    # Individual cells
    padding = 6

    for row in range(ROWS):

        for col in range(COLS):

            outer_rect = pygame.Rect(
                col * CELL_SIZE + padding,
                row * CELL_SIZE + padding,
                CELL_SIZE - padding * 2,
                CELL_SIZE - padding * 2,
            )

            pygame.draw.rect(
                screen,
                BOARD_COLOR,
                outer_rect,
                border_radius=10,
            )

            # Slight cell highlight
            pygame.draw.line(
                screen,
                (42, 128, 94),
                (
                    outer_rect.left + 7,
                    outer_rect.top + 7,
                ),
                (
                    outer_rect.right - 7,
                    outer_rect.top + 7,
                ),
                1,
            )

    # Outer border
    pygame.draw.rect(
        screen,
        GRID_COLOR,
        board_surface,
        width=2,
        border_radius=16,
    )


# =============================================================================
# PIECES
# =============================================================================

def draw_piece(
    screen,
    center_x,
    center_y,
    piece,
    radius,
):

    # Piece shadow
    pygame.draw.circle(
        screen,
        (7, 11, 13),
        (
            center_x + 4,
            center_y + 5,
        ),
        radius,
    )

    if piece == BLACK:

        base_color = UI_BLACK_SOFT
        highlight_color = (57, 62, 66)

    else:

        base_color = UI_WHITE_SOFT
        highlight_color = (255, 255, 255)

    # Main disc
    pygame.draw.circle(
        screen,
        base_color,
        (
            center_x,
            center_y,
        ),
        radius,
    )

    # Inner shading
    pygame.draw.circle(
        screen,
        (
            max(0, base_color[0] - 10),
            max(0, base_color[1] - 10),
            max(0, base_color[2] - 10),
        ),
        (
            center_x,
            center_y + 2,
        ),
        radius - 3,
    )

    # Subtle highlight arc
    pygame.draw.arc(
        screen,
        highlight_color,
        (
            center_x - radius + 5,
            center_y - radius + 5,
            (radius - 5) * 2,
            (radius - 5) * 2,
        ),
        3.5,
        5.8,
        2,
    )


def draw_pieces(
    screen,
    board,
):

    radius = int(CELL_SIZE * 0.34)

    for row in range(ROWS):

        for col in range(COLS):

            piece = board[row][col]

            if piece == EMPTY:
                continue

            center_x = (
                col * CELL_SIZE
                + CELL_SIZE // 2
            )

            center_y = (
                row * CELL_SIZE
                + CELL_SIZE // 2
            )

            draw_piece(
                screen,
                center_x,
                center_y,
                piece,
                radius,
            )


# =============================================================================
# LEGAL MOVE INDICATORS
# =============================================================================

def draw_valid_moves(
    screen,
    valid_moves,
):

    for row, col in valid_moves:

        center_x = (
            col * CELL_SIZE
            + CELL_SIZE // 2
        )

        center_y = (
            row * CELL_SIZE
            + CELL_SIZE // 2
        )

        # Outer glow
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (
                center_x,
                center_y,
            ),
            12,
            2,
        )

        # Main indicator
        pygame.draw.circle(
            screen,
            MOVE_HINT,
            (
                center_x,
                center_y,
            ),
            6,
        )

        # Tiny central highlight
        pygame.draw.circle(
            screen,
            ACCENT_BRIGHT,
            (
                center_x - 1,
                center_y - 1,
            ),
            2,
        )


# =============================================================================
# TOP BAR
# =============================================================================

def draw_top_bar(
    screen,
    player,
    difficulty,
):
    
    pass

# =============================================================================
# Side BAR
# =============================================================================

def draw_sidebar_header(
    screen,
):

    sidebar_x = BOARD_WIDTH

    # Sidebar background
    sidebar_rect = pygame.Rect(
        sidebar_x,
        0,
        INFO_PANEL_WIDTH,
        HEIGHT,
    )

    pygame.draw.rect(
        screen,
        (14, 23, 29),
        sidebar_rect,
    )

    # Small vertical accent line
    pygame.draw.rect(
        screen,
        ACCENT,
        (
            sidebar_x + 18,
            20,
            4,
            45,
        ),
        border_radius=2,
    )

    # Othello title
    draw_text(
        screen,
        "OTHELLO",
        (
            sidebar_x + 34,
            15,
        ),
        size=25,
        color=TEXT_PRIMARY,
        bold=True,
    )

    draw_text(
        screen,
        "STRATEGY • PATIENCE • CONTROL",
        (
            sidebar_x + 35,
            47,
        ),
        size=9,
        color=TEXT_MUTED,
        bold=True,
    )

    # Difficulty badge

    difficulty_rect = pygame.Rect(
        sidebar_x + INFO_PANEL_WIDTH - 120,
        22,
        95,
        34,
    )

    draw_rounded_panel(
        screen,
        difficulty_rect,
        fill=PANEL_LIGHT,
        border=ACCENT,
        radius=17,
    )

    draw_text(
        screen,
        "Insanity",
        difficulty_rect.center,
        size=11,
        color=ACCENT_BRIGHT,
        bold=True,
        center=True,
    )

# =============================================================================
# SCORE CARDS
# =============================================================================

def draw_score_card(
    screen,
    rect,
    label,
    value,
    piece_color,
    active,
):

    border = (
        ACCENT
        if active
        else PANEL_BORDER
    )

    draw_rounded_panel(
        screen,
        rect,
        fill=PANEL_COLOR,
        border=border,
        radius=15,
        border_width=2 if active else 1,
    )

    # Piece indicator
    piece_radius = 14

    pygame.draw.circle(
        screen,
        (8, 10, 12),
        (
            rect.left + 29,
            rect.top + 28,
        ),
        piece_radius + 2,
    )

    pygame.draw.circle(
        screen,
        piece_color,
        (
            rect.left + 29,
            rect.top + 26,
        ),
        piece_radius,
    )

    # Label
    draw_text(
        screen,
        label,
        (
            rect.left + 53,
            rect.top + 12,
        ),
        size=11,
        color=TEXT_MUTED,
        bold=True,
    )

    # Score
    draw_text(
        screen,
        str(value),
        (
            rect.left + 53,
            rect.top + 27,
        ),
        size=25,
        color=TEXT_PRIMARY,
        bold=True,
    )


def draw_score_area(
    screen,
    board,
    player,
):

    black_count, white_count = count_pieces(
        board
    )

    panel_y = 92

    card_width = 123
    card_height = 65

    left_card = pygame.Rect(
        BOARD_WIDTH + 18,
        panel_y,
        card_width,
        card_height,
    )

    right_card = pygame.Rect(
        BOARD_WIDTH + 159,
        panel_y,
        card_width,
        card_height,
    )

    draw_score_card(
        screen,
        left_card,
        "BLACK",
        black_count,
        UI_BLACK_SOFT,
        player == BLACK,
    )

    draw_score_card(
        screen,
        right_card,
        "WHITE",
        white_count,
        UI_WHITE,
        player == WHITE,
    )


# =============================================================================
# TURN CARD
# =============================================================================

def draw_turn_card(
    screen,
    player,
    human_player,
):

    rect = pygame.Rect(
        BOARD_WIDTH + 18,
        178,
        INFO_PANEL_WIDTH - 36,
        67,
    )

    draw_rounded_panel(
        screen,
        rect,
        fill=PANEL_LIGHT,
        border=ACCENT,
        radius=15,
        border_width=1,
    )

    if player == human_player:

        label = "PLAYER'S TURN"
        piece_color = UI_BLACK_SOFT if human_player == BLACK else UI_WHITE

    else:

        label = "AI'S TURN"
        piece_color = UI_BLACK_SOFT if player == BLACK else UI_WHITE

    pygame.draw.circle(
        screen,
        piece_color,
        (
            rect.left + 28,
            rect.centery,
        ),
        13,
    )

    pygame.draw.circle(
        screen,
        (8, 10, 12),
        (
            rect.left + 28,
            rect.centery + 3,
        ),
        13,
        1,
    )

    draw_text(
        screen,
        label,
        (
            rect.left + 52,
            rect.centery,
        ),
        size=17,
        color=TEXT_PRIMARY,
        bold=True,
        center=False,
    )


# =============================================================================
# GAME / AI INFORMATION
# =============================================================================

def difficulty_name(difficulty):

    if difficulty == EASY:
        return "Easy"

    if difficulty == MEDIUM:
        return "Medium"

    return "Hard"


def draw_game_info(
    screen,
    difficulty,
):

    nodes, pruned, think_time, evaluation, algorithm = (
        get_stats()
    )

    # Difficulty
    difficulty_rect = pygame.Rect(
        BOARD_WIDTH + 18,
        264,
        INFO_PANEL_WIDTH - 36,
        72,
    )

    draw_rounded_panel(
        screen,
        difficulty_rect,
        fill=PANEL_COLOR,
        border=PANEL_BORDER,
        radius=15,
    )

    draw_text(
        screen,
        "DIFFICULTY",
        (
            difficulty_rect.left + 14,
            difficulty_rect.top + 10,
        ),
        size=10,
        color=TEXT_MUTED,
        bold=True,
    )

    draw_text(
        screen,
        difficulty_name(difficulty),
        (
            difficulty_rect.left + 14,
            difficulty_rect.top + 30,
        ),
        size=18,
        color=ACCENT_BRIGHT,
        bold=True,
    )

    # Algorithm
    algorithm_rect = pygame.Rect(
        BOARD_WIDTH + 18,
        348,
        INFO_PANEL_WIDTH - 36,
        72,
    )

    draw_rounded_panel(
        screen,
        algorithm_rect,
        fill=PANEL_COLOR,
        border=PANEL_BORDER,
        radius=15,
    )

    draw_text(
        screen,
        "ALGORITHM",
        (
            algorithm_rect.left + 14,
            algorithm_rect.top + 10,
        ),
        size=10,
        color=TEXT_MUTED,
        bold=True,
    )

    draw_text(
        screen,
        algorithm,
        (
            algorithm_rect.left + 14,
            algorithm_rect.top + 30,
        ),
        size=14,
        color=BLUE,
        bold=True,
    )

    # AI Analysis panel
    stats_rect = pygame.Rect(
        BOARD_WIDTH + 18,
        432,
        INFO_PANEL_WIDTH - 36,
        145,
    )

    draw_rounded_panel(
        screen,
        stats_rect,
        fill=PANEL_COLOR,
        border=PANEL_BORDER,
        radius=15,
    )

    draw_text(
        screen,
        "AI ANALYSIS",
        (
            stats_rect.left + 14,
            stats_rect.top + 10,
        ),
        size=11,
        color=TEXT_MUTED,
        bold=True,
    )

    draw_separator(
        screen,
        stats_rect.left + 14,
        stats_rect.top + 32,
        stats_rect.right - 14,
    )

    # Row 1
    draw_text(
        screen,
        "Nodes",
        (
            stats_rect.left + 14,
            stats_rect.top + 43,
        ),
        size=13,
        color=TEXT_SECONDARY,
    )

    draw_text(
        screen,
        f"{nodes:,}",
        (
            stats_rect.right - 60,
            stats_rect.top + 43,
        ),
        size=13,
        color=TEXT_PRIMARY,
        bold=True,
    )

    # Row 2
    draw_text(
        screen,
        "Pruned",
        (
            stats_rect.left + 14,
            stats_rect.top + 67,
        ),
        size=13,
        color=TEXT_SECONDARY,
    )

    draw_text(
        screen,
        f"{pruned:,}",
        (
            stats_rect.right - 60,
            stats_rect.top + 67,
        ),
        size=13,
        color=TEXT_PRIMARY,
        bold=True,
    )

    # Row 3
    draw_text(
        screen,
        "Evaluation",
        (
            stats_rect.left + 14,
            stats_rect.top + 91,
        ),
        size=13,
        color=TEXT_SECONDARY,
    )

    draw_text(
        screen,
        f"{evaluation:.2f}",
        (
            stats_rect.right - 60,
            stats_rect.top + 91,
        ),
        size=13,
        color=ACCENT_BRIGHT,
        bold=True,
    )

    # Row 4
    draw_text(
        screen,
        "Think Time",
        (
            stats_rect.left + 14,
            stats_rect.top + 115,
        ),
        size=13,
        color=TEXT_SECONDARY,
    )

    draw_text(
        screen,
        f"{think_time * 1000:.1f} ms",
        (
            stats_rect.right - 60,
            stats_rect.top + 115,
        ),
        size=13,
        color=BLUE,
        bold=True,
    )

# =============================================================================
# MAIN GAME DRAW
# =============================================================================

def draw_game(
    screen,
    board,
    player,
    difficulty,
    human_player,
):

    # Background + board
    draw_board(screen)

    # Side bar top section
    draw_sidebar_header(
        screen,
    )

    # Legal moves
    valid_moves = get_valid_moves(
        board,
        player,
    )

    draw_valid_moves(
        screen,
        valid_moves,
    )

    # Pieces must be drawn after indicators
    draw_pieces(
        screen,
        board,
    )

    # Sidebar
    draw_score_area(
        screen,
        board,
        player,
    )

    draw_turn_card(
        screen,
        player,
        human_player,
    )

    draw_game_info(
        screen,
        difficulty,
    )
