ROWS = 6
COLS = 6
CELL_SIZE = 100
MAX_DEPTH = 4

# Menu and toss
MENU = 0
COIN_TOSS = 1
PLAYING = 2
GAME_OVER = 3

# AI Difficulty
EASY = 1
MEDIUM = 2
HARD = 3

BOARD_WIDTH = COLS * CELL_SIZE
BOARD_HEIGHT = ROWS * CELL_SIZE

# Info panel
INFO_PANEL_WIDTH = 300
INFO_PANEL_COLOR = (45, 45, 45)

GOLD = (212, 175, 55)
RED = (220, 60, 60)
BLUE = (70, 150, 255)

WIDTH = BOARD_WIDTH + INFO_PANEL_WIDTH
HEIGHT = BOARD_HEIGHT

EMPTY = 0
WHITE = -1
BLACK = 1

BOARD_GREEN = (34, 139, 34)
GRID_COLOR = (0, 0, 0)

BLACK_COLOR = (20, 20, 20)
WHITE_COLOR = (245, 245, 245)

BACKGROUND = (60, 60, 60)
TEXT_COLOR = (255, 255, 255)

FPS = 60
AI_MOVE_DELAY = 700
TITLE = "Othello"

# matrix directions

DIRECTIONS = [
    (-1, -1),  # up left
    (-1, 0),  # up
    (-1, 1),  # up right
    (0, -1),  # left
    (0, 1),  # right
    (1, -1),  # down left
    (1, 0),  # down
    (1, 1),  # down right
]
