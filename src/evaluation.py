from board import *
from constants import *


def evaluate_board(board):
    black_count, white_count = count_pieces(board)

    piece_score = white_count - black_count

    corner_score = evaluate_corners(board)
    edge_score = evaluate_edges(board)
    mobility_score = evaluate_mobility(board)

    return piece_score + corner_score + edge_score + mobility_score


def evaluate_corners(board):

    score = 0

    corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]

    for row, col in corners:

        if board[row][col] == WHITE:
            score += 25

        elif board[row][col] == BLACK:
            score -= 25

    return score


def evaluate_edges(board):

    score = 0

    for col in range(1, COLS - 1):

        if board[0][col] == WHITE:
            score += 3

        elif board[0][col] == BLACK:
            score -= 3

        if board[ROWS - 1][col] == WHITE:
            score += 3

        elif board[ROWS - 1][col] == BLACK:
            score -= 3

    for row in range(1, ROWS - 1):

        if board[row][0] == WHITE:
            score += 3

        elif board[row][0] == BLACK:
            score -= 3

        if board[row][COLS - 1] == WHITE:
            score += 3

        elif board[row][COLS - 1] == BLACK:
            score -= 3

    return score


def evaluate_mobility(board):

    white_moves = len(get_valid_moves(board, WHITE))
    black_moves = len(get_valid_moves(board, BLACK))

    return (white_moves - black_moves) * 2
