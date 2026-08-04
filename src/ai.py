import random, math
import time

from ai_stats import *
from board import *
from constants import *
from evaluation import evaluate_board


def random_move(board, player):

    reset()

    start_time = time.time()
    valid_moves = get_valid_moves(board, player)

    if len(valid_moves) == 0:
        return None

    move = random.choice(valid_moves)

    add_node()
    set_score(0)
    set_time(time.time() - start_time)

    set_algorithm("Random")
    return move


def copy_board(board):
    board_copy = []

    for row in board:
        board_copy.append(row.copy())

    return board_copy


def minimax(board, depth, depth_limit, alpha, beta, maximizing_player):
    add_node()
    if depth == depth_limit or game_over(board):
        return evaluate_board(board)

    if maximizing_player:
        best_score = -math.inf

        moves = get_valid_moves(board, WHITE)

        if len(moves) == 0:
            return minimax(board, depth + 1, depth_limit, alpha, beta, False)

        for row, col in moves:
            board_copy = copy_board(board)

            make_move(board_copy, row, col, WHITE)

            score = minimax(board_copy, depth + 1, depth_limit, alpha, beta, False)

            best_score = max(best_score, score)

            alpha = max(alpha, best_score)

            if beta <= alpha:
                add_pruned()
                break

        return best_score

    else:
        best_score = math.inf

        moves = get_valid_moves(board, BLACK)

        if len(moves) == 0:
            return minimax(board, depth + 1, depth_limit, alpha, beta, True)

        for row, col in moves:
            board_copy = copy_board(board)

            make_move(board_copy, row, col, BLACK)

            score = minimax(board_copy, depth + 1, depth_limit, alpha, beta, True)

            best_score = min(best_score, score)

            beta = min(beta, best_score)

            if beta <= alpha:
                add_pruned()
                break

        return best_score


def get_best_move(board, player):

    # EASY
    if AI_DIFFICULTY == EASY:
        return random_move(board, player)

    # MEDIUM
    if AI_DIFFICULTY == MEDIUM:
        return get_minimax_move(board, player, 2)

    # HARD
    return get_minimax_move(board, player, MAX_DEPTH)


def get_minimax_move(board, player, depth_limit):

    reset()

    if depth_limit == 2:
        set_algorithm("Minimax")

    else:
        set_algorithm("Minimax + Alpha-Beta")

    start_time = time.time()

    best_score = -math.inf
    best_move = None

    moves = get_valid_moves(board, player)

    if len(moves) == 0:
        return None

    for row, col in moves:

        board_copy = copy_board(board)

        make_move(board_copy, row, col, player)

        score = minimax(board_copy, 1, depth_limit, -math.inf, math.inf, False)

        if score > best_score:
            best_score = score
            best_move = (row, col)

    set_time(time.time() - start_time)
    set_score(best_score)

    return best_move
