import pygame

from constants import *
from board import *
from ai import get_best_move
from ui import draw_game
from menu import run_menu
from toss import run_toss
from end_screen import run_end_screen


def play_match(screen, selected_difficulty, human_player, ai_player):

    clock = pygame.time.Clock()

    board = create_board()

    current_player = BLACK

    running = True
    winner = EMPTY

    while running:

        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return None, None

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == human_player:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                if not is_on_board(row, col):
                    continue

                if make_move(board, row, col, human_player):

                    current_player *= -1

                    if game_over(board):

                        winner = get_winner(board)
                        running = False

                    elif not has_valid_moves(board, current_player):

                        current_player *= -1

        if running and current_player == ai_player:

            draw_game(screen, board, current_player, selected_difficulty)

            pygame.display.update()

            pygame.time.delay(AI_MOVE_DELAY)

            move = get_best_move(board, ai_player, selected_difficulty)

            if move is not None:

                row, col = move

                make_move(board, row, col, ai_player)

                current_player *= -1

                if game_over(board):

                    winner = get_winner(board)
                    running = False

                elif not has_valid_moves(board, current_player):

                    current_player *= -1

            else:

                if game_over(board):

                    winner = get_winner(board)
                    running = False

                else:

                    current_player *= -1

        if running:

            draw_game(screen, board, current_player, selected_difficulty)

            pygame.display.update()

    return board, winner


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(TITLE)

    app_running = True

    while app_running:

        selected_difficulty = run_menu(screen)

        if selected_difficulty is None:
            break

        toss_result = run_toss(screen)

        if toss_result is None:
            break

        human_player, ai_player = toss_result

        board, winner = play_match(screen, selected_difficulty, human_player, ai_player)

        if board is None:
            break

        play_again = run_end_screen(screen, board, winner, human_player, ai_player)

        if not play_again:
            app_running = False

    pygame.quit()


if __name__ == "__main__":
    main()