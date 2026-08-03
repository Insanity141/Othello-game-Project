import random, math

from board import *
from constants import *

def random_move(board, player):
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) == 0:
        return None

    return random.choice(valid_moves)

def copy_board(board):
    board_copy = []

    for row in board:
        board_copy.append(row.copy())

    return board_copy

def evaluate_board(board):
    black_count, white_count = count_pieces(board)

    piece_score = white_count - black_count

    corner_score = evaluate_corners(board)
    edge_score = evaluate_edges(board)
    mobility_score = evaluate_mobility(board)

    return (piece_score + corner_score + edge_score + mobility_score)


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == MAX_DEPTH or game_over(board):
        return evaluate_board(board)

    if maximizing_player:
        best_score = -math.inf

        moves = get_valid_moves(board, WHITE)

        if len(moves) == 0:
            return minimax(board, depth + 1, alpha, beta, False)

        for row, col in moves:
            board_copy = copy_board(board)

            make_move(board_copy, row, col, WHITE)

            score = minimax(board_copy, depth + 1, alpha, beta, False)

            best_score = max(best_score, score)

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = math.inf

        moves = get_valid_moves(board, BLACK)

        if len(moves) == 0:
            return minimax(board, depth + 1, alpha, beta, True)

        for row, col in moves:
            board_copy = copy_board(board)

            make_move(board_copy, row, col, BLACK)

            score = minimax(board, depth + 1, alpha, beta, True)

            best_score = min(best_score, score)

            if beta <= alpha:
                break

        return best_score

def get_best_move(board, player):
    best_score = -math.inf
    best_move = None

    moves = get_valid_moves(board, player)

    if len(moves) == 0:
        return None

    for row, col in moves:
        board_copy = copy_board(board)

        make_move(board_copy, row, col, player)

        score = minimax(board_copy, 1, -math.inf, math.inf, False)

        if score > best_score:
            best_score = score
            best_move = (row, col)

    return best_move

def evaluate_corners(board):
    score = 0

    corners = [
        (0, 0),
        (0, COLS - 1),
        (ROWS - 1, 0),
        (ROWS - 1, COLS - 1)
    ]

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

