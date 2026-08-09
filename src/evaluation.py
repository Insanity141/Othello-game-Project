from board import *
from constants import *


def evaluate_board(board, ai_player):

    black_count, white_count = count_pieces(board)

    if ai_player == BLACK:
        piece_score = black_count - white_count
    else:
        piece_score = white_count - black_count

    corner_score = evaluate_corners(board, ai_player)
    edge_score = evaluate_edges(board, ai_player)
    mobility_score = evaluate_mobility(board, ai_player)

    return piece_score + corner_score + edge_score + mobility_score


def evaluate_corners(board, ai_player):

    score = 0

    opponent = -ai_player

    corners = [(0, 0), (0, COLS - 1), (ROWS - 1, 0), (ROWS - 1, COLS - 1)]

    for row, col in corners:

        if board[row][col] == ai_player:
            score += 25

        elif board[row][col] == opponent:
            score -= 25

    return score


def evaluate_edges(board, ai_player):

    score = 0

    opponent = -ai_player

    for col in range(1, COLS - 1):

        if board[0][col] == ai_player:
            score += 3

        elif board[0][col] == opponent:
            score -= 3

        if board[ROWS - 1][col] == ai_player:
            score += 3

        elif board[ROWS - 1][col] == opponent:
            score -= 3

    for row in range(1, ROWS - 1):

        if board[row][0] == ai_player:
            score += 3

        elif board[row][0] == opponent:
            score -= 3

        if board[row][COLS - 1] == ai_player:
            score += 3

        elif board[row][COLS - 1] == opponent:
            score -= 3

    return score


def evaluate_mobility(board, ai_player):

    opponent = -ai_player

    ai_moves = len(get_valid_moves(board, ai_player))
    opponent_moves = len(get_valid_moves(board, opponent))

    return (ai_moves - opponent_moves) * 2
