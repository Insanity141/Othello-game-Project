import math
import random
import time

import ai_stats

from board import (
    game_over,
    get_valid_moves,
    make_move,
)

from constants import (
    EASY,
    MEDIUM,
    HARD,
)

from evaluation import evaluate_board


# Search depth for each difficulty.
MEDIUM_DEPTH = 4
HARD_DEPTH = 7


def copy_board(board):
    return [row.copy() for row in board]


def board_key(board):
    return tuple(tuple(row) for row in board)


def random_move(board, player):

    ai_stats.reset()

    start_time = time.perf_counter()

    valid_moves = get_valid_moves(board, player)

    if not valid_moves:

        ai_stats.set_algorithm("Random")
        ai_stats.set_time(
            time.perf_counter() - start_time
        )

        return None

    move = random.choice(valid_moves)

    ai_stats.add_node()

    ai_stats.set_score(0)

    ai_stats.set_time(
        time.perf_counter() - start_time
    )

    ai_stats.set_algorithm("Random")

    return move


def _move_priority(move, board, player):
    """
    Assign a priority to a move.

    Better moves are searched first so Alpha-Beta
    can prune more branches.
    """

    row, col = move

    score = 0

    corners = {
        (0, 0),
        (0, len(board) - 1),
        (len(board) - 1, 0),
        (len(board) - 1, len(board) - 1),
    }

    if (row, col) in corners:
        score += 10000

    # Corner-adjacent squares are generally dangerous.
    dangerous_squares = {

        (0, 1),
        (1, 0),
        (1, 1),

        (0, len(board) - 2),
        (1, len(board) - 2),
        (1, len(board) - 1),

        (len(board) - 2, 0),
        (len(board) - 2, 1),
        (len(board) - 1, 1),

        (len(board) - 2, len(board) - 2),
        (len(board) - 2, len(board) - 1),
        (len(board) - 1, len(board) - 2),
    }

    if (row, col) in dangerous_squares:
        score -= 500

    # Cheap positional lookahead for ordering.
    test_board = copy_board(board)

    if make_move(
        test_board,
        row,
        col,
        player,
    ):
        score += (
            evaluate_board(
                test_board,
                player,
            )
            * 0.01
        )

    return score


def order_moves(board, moves, player):

    return sorted(
        moves,
        key=lambda move: _move_priority(
            move,
            board,
            player,
        ),
        reverse=True,
    )


def minimax(
    board,
    depth,
    depth_limit,
    current_player,
    ai_player,
):

    ai_stats.add_node()

    if (
        depth >= depth_limit
        or game_over(board)
    ):
        return evaluate_board(
            board,
            ai_player,
        )

    moves = get_valid_moves(
        board,
        current_player,
    )

    # Pass turn if there are no legal moves.
    if not moves:

        return minimax(
            board,
            depth + 1,
            depth_limit,
            -current_player,
            ai_player,
        )

    maximizing = (
        current_player == ai_player
    )

    if maximizing:
        best_score = -math.inf
    else:
        best_score = math.inf

    for row, col in order_moves(
        board,
        moves,
        current_player,
    ):

        board_copy = copy_board(board)

        make_move(
            board_copy,
            row,
            col,
            current_player,
        )

        score = minimax(
            board_copy,
            depth + 1,
            depth_limit,
            -current_player,
            ai_player,
        )

        if maximizing:
            best_score = max(
                best_score,
                score,
            )
        else:
            best_score = min(
                best_score,
                score,
            )

    return best_score


def alpha_beta(
    board,
    depth,
    depth_limit,
    alpha,
    beta,
    current_player,
    ai_player,
    transposition_table,
):

    ai_stats.add_node()

    key = (
        board_key(board),
        current_player,
        depth_limit - depth,
    )

    cached = transposition_table.get(key)

    if cached is not None:
        return cached

    if (
        depth >= depth_limit
        or game_over(board)
    ):

        score = evaluate_board(
            board,
            ai_player,
        )

        transposition_table[key] = score

        return score

    moves = get_valid_moves(
        board,
        current_player,
    )

    # Pass turn
    if not moves:

        score = alpha_beta(
            board,
            depth + 1,
            depth_limit,
            alpha,
            beta,
            -current_player,
            ai_player,
            transposition_table,
        )

        transposition_table[key] = score

        return score

    maximizing = (
        current_player == ai_player
    )

    ordered_moves = order_moves(
        board,
        moves,
        current_player,
    )

    if maximizing:

        best_score = -math.inf

        for row, col in ordered_moves:

            board_copy = copy_board(
                board
            )

            make_move(
                board_copy,
                row,
                col,
                current_player,
            )

            score = alpha_beta(
                board_copy,
                depth + 1,
                depth_limit,
                alpha,
                beta,
                -current_player,
                ai_player,
                transposition_table,
            )

            best_score = max(
                best_score,
                score,
            )

            alpha = max(
                alpha,
                best_score,
            )

            if beta <= alpha:

                ai_stats.add_pruned()

                break

    else:

        best_score = math.inf

        for row, col in ordered_moves:

            board_copy = copy_board(
                board
            )

            make_move(
                board_copy,
                row,
                col,
                current_player,
            )

            score = alpha_beta(
                board_copy,
                depth + 1,
                depth_limit,
                alpha,
                beta,
                -current_player,
                ai_player,
                transposition_table,
            )

            best_score = min(
                best_score,
                score,
            )

            beta = min(
                beta,
                best_score,
            )

            if beta <= alpha:

                ai_stats.add_pruned()

                break

    transposition_table[key] = best_score

    return best_score


def get_best_move(
    board,
    player,
    difficulty,
):

    if difficulty == EASY:
        return random_move(
            board,
            player,
        )

    if difficulty == MEDIUM:

        return get_search_move(
            board,
            player,
            MEDIUM_DEPTH,
            use_alpha_beta=False,
        )

    return get_search_move(
        board,
        player,
        HARD_DEPTH,
        use_alpha_beta=True,
    )


def get_search_move(
    board,
    player,
    depth_limit,
    use_alpha_beta,
):

    ai_stats.reset()

    if use_alpha_beta:

        ai_stats.set_algorithm(
            "Minimax + Alpha-Beta"
        )

    else:

        ai_stats.set_algorithm(
            "Minimax"
        )

    start_time = time.perf_counter()

    moves = get_valid_moves(
        board,
        player,
    )

    if not moves:

        ai_stats.set_time(
            time.perf_counter()
            - start_time
        )

        return None

    best_score = -math.inf
    best_move = moves[0]

    transposition_table = (
        {}
        if use_alpha_beta
        else None
    )

    for row, col in order_moves(
        board,
        moves,
        player,
    ):

        board_copy = copy_board(
            board
        )

        make_move(
            board_copy,
            row,
            col,
            player,
        )

        if use_alpha_beta:

            score = alpha_beta(
                board_copy,
                1,
                depth_limit,
                -math.inf,
                math.inf,
                -player,
                player,
                transposition_table,
            )

        else:

            score = minimax(
                board_copy,
                1,
                depth_limit,
                -player,
                player,
            )

        if score > best_score:

            best_score = score
            best_move = (row, col)

    ai_stats.set_time(
        time.perf_counter()
        - start_time
    )

    ai_stats.set_score(
        best_score
    )

    return best_move