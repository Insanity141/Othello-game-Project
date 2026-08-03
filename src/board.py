from constants import *

def create_board():
    board = []

    for row in range(ROWS):
        board.append([EMPTY] * COLS)

    board[2][2] = WHITE
    board[2][3] = BLACK
    board[3][2] = BLACK
    board[3][3] = WHITE

    return board

def is_on_board(row, col):

    if row < 0 or row >= ROWS:
        return False

    if col < 0 or col >= COLS:
        return False

    return True

def is_valid_move(board, row, col, player):

    if not is_on_board(row, col):
        return False

    if board[row][col] != EMPTY:
        return False

    opponent = -player

    for row_direction, col_direction in DIRECTIONS:

        current_row = row + row_direction
        current_col = col + col_direction

        if not is_on_board(current_row, current_col):
            continue

        if board[current_row][current_col] != opponent:
            continue

        while True:

            current_row += row_direction
            current_col += col_direction

            if not is_on_board(current_row, current_col):
                break

            if board[current_row][current_col] == EMPTY:
                break

            if board[current_row][current_col] == player:
                return True

    return False

def get_valid_moves(board, player):

    valid_moves = []

    for row in range(ROWS):
        for col in range(COLS):
            if is_valid_move(board, row, col, player):
                valid_moves.append((row, col))

    return valid_moves

def count_pieces(board):
    black_count = 0
    white_count = 0

    for row in board:
        for piece in row:
            if piece == BLACK:
                black_count += 1
            elif piece == WHITE:
                white_count += 1

    return black_count, white_count

def print_board(board):
    for row in board:
        print(row)

def get_flipable_pieces(board, row, col, player):

    opponent = -player

    flippable = []

    if not is_valid_move(board, row, col, player):
        return flippable

    for row_direction, col_direction in DIRECTIONS:

        current_row = row + row_direction
        current_col = col + col_direction

        pieces = []

        if not is_on_board(current_row, current_col):
            continue

        if board[current_row][current_col] != opponent:
            continue

        while True:

            pieces.append((current_row, current_col))

            current_row += row_direction
            current_col += col_direction

            if not is_on_board(current_row, current_col):
                pieces = []
                break

            if board[current_row][current_col] == EMPTY:
                pieces = []
                break

            if board[current_row][current_col] == player:
                break

        flippable.extend(pieces)

    return flippable

def flip_pieces(board, flippable, player):

    for piece_row, piece_col in flippable:
        board[piece_row][piece_col] = player

def make_move(board, row, col, player):

    if not is_valid_move(board, row, col, player):
        return False

    flippable = get_flipable_pieces(board, row, col, player)

    board[row][col] = player

    flip_pieces(board, flippable, player)

    return True

# Checks for valid move

def has_valid_moves(board, player):

    return len(get_valid_moves(board, player)) > 0

# If the board is full

def game_over(board):

    return(
        not has_valid_moves(board, BLACK)
        and
        not has_valid_moves(board, WHITE)
    )

# Winner decider

def get_winner(board):

    black_count, white_count = count_pieces(board)

    if black_count > white_count:
        return BLACK

    if white_count > black_count:
        return WHITE

    return EMPTY
