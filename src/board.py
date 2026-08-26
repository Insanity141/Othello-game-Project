from constants import *


def create_board():
    board = [[EMPTY] * COLS for _ in range(ROWS)]

    # Standard starting position, centered for even-sized boards.
    mid_row = ROWS // 2 - 1
    mid_col = COLS // 2 - 1

    board[mid_row][mid_col] = WHITE
    board[mid_row][mid_col + 1] = BLACK
    board[mid_row + 1][mid_col] = BLACK
    board[mid_row + 1][mid_col + 1] = WHITE

    return board


def is_on_board(row, col):
    return 0 <= row < ROWS and 0 <= col < COLS


def get_flipable_pieces(board, row, col, player):
    """Return all opponent pieces flipped by placing player at (row, col)."""
    if not is_on_board(row, col) or board[row][col] != EMPTY:
        return []

    opponent = -player
    flippable = []

    for row_direction, col_direction in DIRECTIONS:
        current_row = row + row_direction
        current_col = col + col_direction
        line = []

        # We need at least one opponent piece followed by our own piece.
        while (
            is_on_board(current_row, current_col)
            and board[current_row][current_col] == opponent
        ):
            line.append((current_row, current_col))
            current_row += row_direction
            current_col += col_direction

        if (
            line
            and is_on_board(current_row, current_col)
            and board[current_row][current_col] == player
        ):
            flippable.extend(line)

    return flippable


def is_valid_move(board, row, col, player):
    return bool(get_flipable_pieces(board, row, col, player))


def get_valid_moves(board, player):
    return [
        (row, col)
        for row in range(ROWS)
        for col in range(COLS)
        if board[row][col] == EMPTY
        and get_flipable_pieces(board, row, col, player)
    ]


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


def flip_pieces(board, flippable, player):
    for piece_row, piece_col in flippable:
        board[piece_row][piece_col] = player


def make_move(board, row, col, player):
    flippable = get_flipable_pieces(board, row, col, player)

    if not flippable:
        return False

    board[row][col] = player
    flip_pieces(board, flippable, player)

    return True


def has_valid_moves(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            if (
                board[row][col] == EMPTY
                and get_flipable_pieces(board, row, col, player)
            ):
                return True

    return False


def game_over(board):
    return (
        not has_valid_moves(board, BLACK)
        and not has_valid_moves(board, WHITE)
    )


def get_winner(board):
    black_count, white_count = count_pieces(board)

    if black_count > white_count:
        return BLACK

    if white_count > black_count:
        return WHITE

    return EMPTY