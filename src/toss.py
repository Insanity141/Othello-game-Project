import math
import random
import pygame

from constants import *

from ui import (
    get_font,
    draw_text,
    draw_rounded_panel,
)


# =============================================================================
# TOSS THEME
# =============================================================================

TOSS_BG = (12, 19, 24)

COIN_GOLD = (215, 176, 68)
COIN_GOLD_LIGHT = (240, 204, 104)
COIN_GOLD_DARK = (145, 111, 32)

TOSS_PANEL = (20, 29, 36)
TOSS_PANEL_LIGHT = (27, 39, 47)
TOSS_BORDER = (53, 70, 80)

TOSS_TEXT = (239, 244, 246)
TOSS_TEXT_SECONDARY = (161, 181, 190)
TOSS_TEXT_MUTED = (108, 130, 141)

TOSS_GREEN = (53, 185, 131)
TOSS_GREEN_DARK = (32, 130, 91)

TOSS_RED = (215, 88, 93)


# =============================================================================
# LAYOUT
# =============================================================================

def get_toss_layout():

    center_x = WIDTH // 2

    panel_width = min(
        560,
        WIDTH - 80,
    )

    panel_height = 455

    panel_rect = pygame.Rect(
        center_x - panel_width // 2,
        125,
        panel_width,
        panel_height,
    )

    return panel_rect


# =============================================================================
# BACKGROUND
# =============================================================================

def draw_toss_background(screen):

    screen.fill(TOSS_BG)

    glow_surface = pygame.Surface(
        (WIDTH, HEIGHT),
        pygame.SRCALPHA,
    )

    # Soft decorative glow
    pygame.draw.circle(
        glow_surface,
        (*COIN_GOLD, 12),
        (
            WIDTH // 2,
            HEIGHT // 2,
        ),
        230,
    )

    pygame.draw.circle(
        glow_surface,
        (53, 185, 131, 8),
        (
            100,
            HEIGHT - 60,
        ),
        180,
    )

    screen.blit(
        glow_surface,
        (0, 0),
    )


# =============================================================================
# COIN
# =============================================================================

def draw_coin(
    screen,
    center,
    radius,
    face,
    scale_x=1.0,
    rotation_progress=0.0,
):

    center_x, center_y = center

    width = max(
        4,
        int(radius * 2 * scale_x),
    )

    height = radius * 2

    coin_surface = pygame.Surface(
        (
            width + 20,
            height + 20,
        ),
        pygame.SRCALPHA,
    )

    coin_center = (
        coin_surface.get_width() // 2,
        coin_surface.get_height() // 2,
    )

    coin_rect = pygame.Rect(
        10,
        10,
        width,
        height,
    )

    # ---------------------------------------------------------
    # Shadow
    # ---------------------------------------------------------

    shadow_rect = pygame.Rect(
        coin_rect.left + 4,
        coin_rect.top + 6,
        coin_rect.width,
        coin_rect.height,
    )

    pygame.draw.ellipse(
        coin_surface,
        (5, 8, 10, 150),
        shadow_rect,
    )

    # ---------------------------------------------------------
    # Outer rim
    # ---------------------------------------------------------

    pygame.draw.ellipse(
        coin_surface,
        COIN_GOLD_DARK,
        coin_rect,
    )

    # ---------------------------------------------------------
    # Main coin
    # ---------------------------------------------------------

    inner_rect = coin_rect.inflate(
        -5,
        -5,
    )

    pygame.draw.ellipse(
        coin_surface,
        COIN_GOLD,
        inner_rect,
    )

    # ---------------------------------------------------------
    # Inner rim
    # ---------------------------------------------------------

    pygame.draw.ellipse(
        coin_surface,
        COIN_GOLD_LIGHT,
        inner_rect,
        2,
    )

    # ---------------------------------------------------------
    # Face
    # ---------------------------------------------------------

    if scale_x > 0.16:

        face_font_size = max(
            12,
            int(radius * 0.32),
        )

        face_font = get_font(
            face_font_size,
            bold=True,
        )

        face_surface = face_font.render(
            face,
            True,
            (87, 63, 15),
        )

        compressed_width = max(
            2,
            int(
                face_surface.get_width()
                * scale_x
            ),
        )

        face_surface = pygame.transform.smoothscale(
            face_surface,
            (
                compressed_width,
                face_surface.get_height(),
            ),
        )

        face_rect = face_surface.get_rect(
            center=coin_center
        )

        coin_surface.blit(
            face_surface,
            face_rect,
        )

    # ---------------------------------------------------------
    # Small highlight
    # ---------------------------------------------------------

    if scale_x > 0.35:

        pygame.draw.arc(
            coin_surface,
            (255, 236, 157),
            (
                coin_rect.left + 9,
                coin_rect.top + 9,
                max(
                    2,
                    coin_rect.width - 18,
                ),
                max(
                    2,
                    coin_rect.height - 18,
                ),
            ),
            math.radians(205),
            math.radians(325),
            2,
        )

    # ---------------------------------------------------------
    # Blit
    # ---------------------------------------------------------

    screen.blit(
        coin_surface,
        (
            center_x
            - coin_surface.get_width() // 2,

            center_y
            - coin_surface.get_height() // 2,
        ),
    )


# =============================================================================
# STATIC HEADER
# =============================================================================

def draw_toss_header(screen):

    center_x = WIDTH // 2

    draw_text(
        screen,
        "OTHELLO",
        (
            center_x,
            42,
        ),
        size=38,
        color=TOSS_TEXT,
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
        color=TOSS_TEXT_MUTED,
        bold=True,
        center=True,
    )

    pygame.draw.line(
        screen,
        COIN_GOLD,
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
# SELECTION SCREEN
# =============================================================================

def draw_choice_screen(
    screen,
    selected_choice,
):

    panel_rect = get_toss_layout()

    draw_rounded_panel(
        screen,
        panel_rect,
        fill=TOSS_PANEL,
        border=TOSS_BORDER,
        radius=22,
        border_width=1,
    )

    center_x = panel_rect.centerx

    draw_text(
        screen,
        "COIN TOSS",
        (
            center_x,
            panel_rect.top + 48,
        ),
        size=27,
        color=COIN_GOLD_LIGHT,
        bold=True,
        center=True,
    )

    draw_text(
        screen,
        "Choose your side",
        (
            center_x,
            panel_rect.top + 84,
        ),
        size=15,
        color=TOSS_TEXT_SECONDARY,
        center=True,
    )

    # -------------------------------------------------------------------------
    # Choice buttons
    # -------------------------------------------------------------------------

    button_width = 185
    button_height = 62

    heads_rect = pygame.Rect(
        center_x
        - button_width
        - 12,
        panel_rect.top + 128,
        button_width,
        button_height,
    )

    tails_rect = pygame.Rect(
        center_x + 12,
        panel_rect.top + 128,
        button_width,
        button_height,
    )

    mouse_pos = pygame.mouse.get_pos()

    heads_hovered = heads_rect.collidepoint(
        mouse_pos
    )

    tails_hovered = tails_rect.collidepoint(
        mouse_pos
    )

    heads_selected = (
        selected_choice == "Heads"
    )

    tails_selected = (
        selected_choice == "Tails"
    )

    # Heads
    heads_fill = (
        COIN_GOLD
        if heads_selected
        else TOSS_PANEL_LIGHT
    )

    heads_border = (
        COIN_GOLD_LIGHT
        if heads_selected or heads_hovered
        else TOSS_BORDER
    )

    draw_rounded_panel(
        screen,
        heads_rect,
        fill=heads_fill,
        border=heads_border,
        radius=14,
        border_width=2 if heads_selected else 1,
    )

    draw_text(
        screen,
        "HEADS",
        heads_rect.center,
        size=17,
        color=(
            TOSS_BG
            if heads_selected
            else TOSS_TEXT
        ),
        bold=True,
        center=True,
    )

    # Tails
    tails_fill = (
        COIN_GOLD
        if tails_selected
        else TOSS_PANEL_LIGHT
    )

    tails_border = (
        COIN_GOLD_LIGHT
        if tails_selected or tails_hovered
        else TOSS_BORDER
    )

    draw_rounded_panel(
        screen,
        tails_rect,
        fill=tails_fill,
        border=tails_border,
        radius=14,
        border_width=2 if tails_selected else 1,
    )

    draw_text(
        screen,
        "TAILS",
        tails_rect.center,
        size=17,
        color=(
            TOSS_BG
            if tails_selected
            else TOSS_TEXT
        ),
        bold=True,
        center=True,
    )

    # -------------------------------------------------------------------------
    # Coin preview
    # -------------------------------------------------------------------------

    preview_face = (
        selected_choice.upper()
        if selected_choice
        else "?"
    )

    draw_coin(
        screen,
        (
            center_x,
            panel_rect.top + 245,
        ),
        48,
        preview_face,
        scale_x=1.0,
    )

    # -------------------------------------------------------------------------
    # Toss button
    # -------------------------------------------------------------------------

    toss_rect = pygame.Rect(
        center_x - 120,
        panel_rect.top + 316,
        240,
        60,
    )

    toss_hovered = toss_rect.collidepoint(
        mouse_pos
    )

    toss_fill = (
        TOSS_GREEN
        if toss_hovered
        else TOSS_GREEN_DARK
    )

    draw_rounded_panel(
        screen,
        toss_rect,
        fill=toss_fill,
        border=TOSS_GREEN,
        radius=14,
        border_width=1,
    )

    draw_text(
        screen,
        "TOSS COIN",
        toss_rect.center,
        size=17,
        color=TOSS_TEXT,
        bold=True,
        center=True,
    )

    # -------------------------------------------------------------------------
    # Hint
    # -------------------------------------------------------------------------

    if selected_choice is None:

        hint = "Select Heads or Tails"

    else:

        hint = (
            f"You selected {selected_choice}"
        )

    draw_text(
        screen,
        hint,
        (
            center_x,
            panel_rect.bottom - 35,
        ),
        size=12,
        color=TOSS_TEXT_MUTED,
        center=True,
    )

    return (
        heads_rect,
        tails_rect,
        toss_rect,
    )


# =============================================================================
# ANIMATION SCREEN
# =============================================================================

def draw_toss_animation(
    screen,
    elapsed,
    duration,
):

    panel_rect = get_toss_layout()

    draw_rounded_panel(
        screen,
        panel_rect,
        fill=TOSS_PANEL,
        border=TOSS_BORDER,
        radius=22,
        border_width=1,
    )

    center_x = panel_rect.centerx
    center_y = panel_rect.centery + 25

    draw_text(
        screen,
        "COIN TOSS",
        (
            center_x,
            panel_rect.top + 55,
        ),
        size=27,
        color=COIN_GOLD_LIGHT,
        bold=True,
        center=True,
    )

    # Normalized progress
    progress = min(
        elapsed / duration,
        1.0,
    )

    # Ease out near the end.
    eased = 1 - (1 - progress) ** 2

    # Several rotations.
    rotations = 6

    rotation = (
        eased
        * rotations
        * math.pi
    )

    # Cosine gives us the apparent horizontal width.
    scale_x = abs(
        math.cos(rotation)
    )

    # Alternate visible faces.
    face_index = int(
        rotation / math.pi
    ) % 2

    face = (
        "HEADS"
        if face_index == 0
        else "TAILS"
    )

    draw_coin(
        screen,
        (
            center_x,
            center_y,
        ),
        78,
        face,
        max(
            0.06,
            scale_x,
        ),
        rotation,
    )

    draw_text(
        screen,
        "Tossing...",
        (
            center_x,
            panel_rect.bottom - 55,
        ),
        size=15,
        color=TOSS_TEXT_SECONDARY,
        center=True,
    )


# =============================================================================
# RESULT SCREEN
# =============================================================================

def draw_result_screen(
    screen,
    result,
    human_won,
):

    panel_rect = get_toss_layout()

    draw_rounded_panel(
        screen,
        panel_rect,
        fill=TOSS_PANEL,
        border=TOSS_BORDER,
        radius=22,
        border_width=1,
    )

    center_x = panel_rect.centerx

    draw_text(
        screen,
        "COIN TOSS",
        (
            center_x,
            panel_rect.top + 46,
        ),
        size=27,
        color=COIN_GOLD_LIGHT,
        bold=True,
        center=True,
    )

    draw_text(
        screen,
        "RESULT",
        (
            center_x,
            panel_rect.top + 79,
        ),
        size=10,
        color=TOSS_TEXT_MUTED,
        bold=True,
        center=True,
    )

    # -------------------------------------------------------------------------
    # Final coin
    # -------------------------------------------------------------------------

    draw_coin(
        screen,
        (
            center_x,
            panel_rect.top + 145,
        ),
        58,
        result.upper(),
        scale_x=1.0,
    )

    # -------------------------------------------------------------------------
    # Result text
    # -------------------------------------------------------------------------

    if human_won:

        winner_text = "You won the toss!"

        assignment_text = "You will play Black"

        assignment_color = TOSS_GREEN

    else:

        winner_text = "AI won the toss!"

        assignment_text = "AI will play Black"

        assignment_color = TOSS_RED

    draw_text(
        screen,
        winner_text,
        (
            center_x,
            panel_rect.top + 255,
        ),
        size=22,
        color=TOSS_TEXT,
        bold=True,
        center=True,
    )

    draw_text(
        screen,
        assignment_text,
        (
            center_x,
            panel_rect.top + 292,
        ),
        size=16,
        color=assignment_color,
        bold=True,
        center=True,
    )

    # -------------------------------------------------------------------------
    # Continue button
    # -------------------------------------------------------------------------

    continue_rect = pygame.Rect(
        center_x - 120,
        panel_rect.bottom - 83,
        240,
        60,
    )

    mouse_pos = pygame.mouse.get_pos()

    hovered = continue_rect.collidepoint(
        mouse_pos
    )

    fill = (
        TOSS_GREEN
        if hovered
        else TOSS_GREEN_DARK
    )

    draw_rounded_panel(
        screen,
        continue_rect,
        fill=fill,
        border=TOSS_GREEN,
        radius=14,
        border_width=1,
    )

    draw_text(
        screen,
        "START MATCH",
        continue_rect.center,
        size=17,
        color=TOSS_TEXT,
        bold=True,
        center=True,
    )

    return continue_rect


# =============================================================================
# MAIN TOSS LOOP
# =============================================================================

def run_toss(screen):

    clock = pygame.time.Clock()

    selected_choice = None

    result = None

    human_won = None

    # Animation state
    animating = False
    animation_start = 0

    ANIMATION_DURATION = 1800

    while True:

        clock.tick(FPS)

        # ---------------------------------------------------------------------
        # Draw current state
        # ---------------------------------------------------------------------

        draw_toss_background(screen)

        draw_toss_header(screen)

        if animating:

            elapsed = (
                pygame.time.get_ticks()
                - animation_start
            )

            draw_toss_animation(
                screen,
                elapsed,
                ANIMATION_DURATION,
            )

            if elapsed >= ANIMATION_DURATION:

                animating = False

        elif result is None:

            (
                heads_rect,
                tails_rect,
                toss_rect,
            ) = draw_choice_screen(
                screen,
                selected_choice,
            )

        else:

            continue_rect = draw_result_screen(
                screen,
                result,
                human_won,
            )

        # ---------------------------------------------------------------------
        # Events
        # ---------------------------------------------------------------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                return None

            if (
                event.type
                == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                # Ignore clicks during animation.
                if animating:
                    continue

                # -------------------------------------------------------------
                # Choice screen
                # -------------------------------------------------------------

                if result is None:

                    if heads_rect.collidepoint(
                        event.pos
                    ):

                        selected_choice = "Heads"

                    elif tails_rect.collidepoint(
                        event.pos
                    ):

                        selected_choice = "Tails"

                    elif toss_rect.collidepoint(
                        event.pos
                    ):

                        if selected_choice is None:
                            continue

                        # Determine actual result now.
                        result = random.choice(
                            [
                                "Heads",
                                "Tails",
                            ]
                        )

                        human_won = (
                            selected_choice == result
                        )

                        # But don't immediately reveal it.
                        # First play the animation.
                        animating = True

                        animation_start = (
                            pygame.time.get_ticks()
                        )

                # -------------------------------------------------------------
                # Result screen
                # -------------------------------------------------------------

                else:

                    if continue_rect.collidepoint(
                        event.pos
                    ):

                        if human_won:

                            return BLACK, WHITE

                        return WHITE, BLACK

        # ---------------------------------------------------------------------
        # Display
        # ---------------------------------------------------------------------

        pygame.display.flip()