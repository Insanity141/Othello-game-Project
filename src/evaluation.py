from board import get_valid_moves, count_pieces, game_over
from constants import BLACK, COLS, EMPTY, ROWS, WHITE


# Positional priorities for a 6x6 Othello board.
# Corners are extremely valuable, squares beside corners are dangerous,
# and stable edge territory is generally better than central discs.
POSITION_WEIGHTS = (
    (100, -25, 10, 10, -25, 100),
    (-25, -25, 2, 2, -25, -25),
    (10, 2, 5, 5, 2, 10),
    (10, 2, 5, 5, 2, 10),
    (-25, -25, 2, 2, -25, -25),
    (100, -25, 10, 10, -25, 100),
)


def _ratio(my_value, opponent_value):
    total = my_value + opponent_value

    if total == 0:
        return 0

    return 100 * (my_value - opponent_value) / total


def _disc_difference(board, ai_player):
    black, white = count_pieces(board)

    mine = black if ai_player == BLACK else white
    theirs = white if ai_player == BLACK else black

    return _ratio(mine, theirs)


def _corner_difference(board, ai_player):
    opponent = -ai_player

    corners = (
        (0, 0),
        (0, COLS - 1),
        (ROWS - 1, 0),
        (ROWS - 1, COLS - 1),
    )

    mine = sum(
        board[row][col] == ai_player
        for row, col in corners
    )

    theirs = sum(
        board[row][col] == opponent
        for row, col in corners
    )

    return _ratio(mine, theirs)


def _mobility_difference(board, ai_player):
    opponent = -ai_player

    mine = len(get_valid_moves(board, ai_player))
    theirs = len(get_valid_moves(board, opponent))

    return _ratio(mine, theirs)


def _potential_mobility(board, ai_player):
    """
    Count empty squares adjacent to opponent discs.
    This is a rough measure of future mobility potential.
    """

    opponent = -ai_player

    seen_mine = set()
    seen_theirs = set()

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] != EMPTY:
                continue

            adjacent_opponent = False
            adjacent_ai = False

            for dr, dc in (
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1),           (0, 1),
                (1, -1),  (1, 0),  (1, 1),
            ):
                nr = row + dr
                nc = col + dc

                if 0 <= nr < ROWS and 0 <= nc < COLS:

                    if board[nr][nc] == opponent:
                        adjacent_opponent = True

                    if board[nr][nc] == ai_player:
                        adjacent_ai = True

            if adjacent_opponent:
                seen_mine.add((row, col))

            if adjacent_ai:
                seen_theirs.add((row, col))

    mine = len(seen_mine)
    theirs = len(seen_theirs)

    return _ratio(mine, theirs)


def _positional_score(board, ai_player):
    opponent = -ai_player
    score = 0

    for row in range(ROWS):
        for col in range(COLS):

            if board[row][col] == ai_player:
                score += POSITION_WEIGHTS[row][col]

            elif board[row][col] == opponent:
                score -= POSITION_WEIGHTS[row][col]

    return score


def evaluate_board(board, ai_player):
    """
    Evaluate a position from the AI player's perspective.
    """

    # Terminal position
    if game_over(board):

        black_count, white_count = count_pieces(board)

        mine = (
            black_count
            if ai_player == BLACK
            else white_count
        )

        theirs = (
            white_count
            if ai_player == BLACK
            else black_count
        )

        if mine > theirs:
            return 100000 + (mine - theirs)

        if mine < theirs:
            return -100000 - (theirs - mine)

        return 0

    black_count, white_count = count_pieces(board)

    empty_count = (
        ROWS * COLS
        - black_count
        - white_count
    )

    # Early game
    if empty_count > (ROWS * COLS) * 0.60:

        piece_weight = 0.5
        mobility_weight = 4.0
        positional_weight = 1.0
        corner_weight = 7.0
        potential_weight = 1.0

    # Mid game
    elif empty_count > (ROWS * COLS) * 0.25:

        piece_weight = 1.0
        mobility_weight = 3.0
        positional_weight = 1.5
        corner_weight = 8.0
        potential_weight = 0.5

    # End game
    else:

        piece_weight = 5.0
        mobility_weight = 2.0
        positional_weight = 1.0
        corner_weight = 10.0
        potential_weight = 0.0

    return (
        piece_weight
        * _disc_difference(board, ai_player)

        + mobility_weight
        * _mobility_difference(board, ai_player)

        + positional_weight
        * _positional_score(board, ai_player)

        + corner_weight
        * _corner_difference(board, ai_player)

        + potential_weight
        * _potential_mobility(board, ai_player)
    )