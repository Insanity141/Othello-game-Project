import random
import math
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


def minimax(board, depth, depth_limit, current_player, ai_player):

    add_node()

    if depth == depth_limit or game_over(board):
        return evaluate_board(board, ai_player)

    moves = get_valid_moves(board, current_player)

    if len(moves) == 0:
        return minimax(board, depth + 1, depth_limit, -current_player, ai_player)

    if current_player == ai_player:

        best_score = -math.inf

        for row, col in moves:

            board_copy = copy_board(board)

            make_move(board_copy, row, col, current_player)

            score = minimax(
                board_copy, depth + 1, depth_limit, -current_player, ai_player
            )

            best_score = max(best_score, score)

        return best_score

    else:

        best_score = math.inf

        for row, col in moves:

            board_copy = copy_board(board)

            make_move(board_copy, row, col, current_player)

            score = minimax(
                board_copy, depth + 1, depth_limit, -current_player, ai_player
            )

            best_score = min(best_score, score)

        return best_score

def alpha_beta(board, depth, depth_limit, alpha, beta, current_player, ai_player):

    add_node()

    if depth == depth_limit or game_over(board):
        return evaluate_board(board, ai_player)

    moves = get_valid_moves(board, current_player)

    if len(moves) == 0:

        return alpha_beta(
            board, depth + 1, depth_limit, alpha, beta, -current_player, ai_player
        )

    if current_player == ai_player:

        best_score = -math.inf

        for row, col in moves:

            board_copy = copy_board(board)

            make_move(board_copy, row, col, current_player)

            score = alpha_beta(
                board_copy,
                depth + 1,
                depth_limit,
                alpha,
                beta,
                -current_player,
                ai_player,
            )

            best_score = max(best_score, score)

            alpha = max(alpha, best_score)

            if beta <= alpha:
                add_pruned()
                break

        return best_score

    else:

        best_score = math.inf

        for row, col in moves:

            board_copy = copy_board(board)

            make_move(board_copy, row, col, current_player)

            score = alpha_beta(
                board_copy,
                depth + 1,
                depth_limit,
                alpha,
                beta,
                -current_player,
                ai_player,
            )

            best_score = min(best_score, score)

            beta = min(beta, best_score)

            if beta <= alpha:
                add_pruned()
                break

        return best_score


def get_best_move(board, player, difficulty):

    if difficulty == EASY:

        return random_move(board, player)

    if difficulty == MEDIUM:

        return get_minimax_move(board, player, 2, False)

    return get_minimax_move(board, player, MAX_DEPTH, True)


def get_minimax_move(board, player, depth_limit, use_alpha_beta):

    reset()

    if use_alpha_beta:
        set_algorithm("Minimax + Alpha-Beta")

    else:
        set_algorithm("Minimax")

    start_time = time.time()

    best_score = -math.inf
    best_move = None

    moves = get_valid_moves(board, player)

    if len(moves) == 0:
        return None

    for row, col in moves:

        board_copy = copy_board(board)

        make_move(board_copy, row, col, player)

        if use_alpha_beta:

            score = alpha_beta(
                board_copy, 1, depth_limit, -math.inf, math.inf, -player, player
            )

        else:

            score = minimax(board_copy, 1, depth_limit, -player, player)

        if score > best_score:

            best_score = score
            best_move = (row, col)

    set_time(time.time() - start_time)

    set_score(best_score)

    return best_move