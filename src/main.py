import pygame

from constants import *
from board import *
from ai import get_best_move
from ui import draw_game

human_player = BLACK
ai_player = WHITE

def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)

    clock = pygame.time.Clock()

    board = create_board()

    current_player = BLACK

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN and current_player == human_player:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                row = mouse_y // CELL_SIZE
                col = mouse_x // CELL_SIZE

                if not is_on_board(row, col):
                    continue

                if make_move(board, row, col, current_player):
                    current_player *= -1

                if game_over(board):

                    winner = get_winner(board)

                    if winner == BLACK:
                        print("Black Wins!")

                    elif winner == WHITE:
                        print("White Wins!")

                    else:
                        print("Draw.")

                    running = False

                elif not has_valid_moves(board, current_player):

                    print(f"{current_player} has no valid moves. Passing turn.")
                    current_player *= -1

        if current_player == ai_player:
            move = get_best_move(board, ai_player)

            if move is not None:

                row, col = move
                make_move(board, row, col, ai_player)

                current_player *= -1

                if game_over(board):

                    winner = get_winner(board)

                    if winner == BLACK:
                        print("Black Wins!")
                        
                    elif winner == WHITE:
                        print("White Wins!")
                        
                    else:
                        print("Draw.")
                        
                    running = False
                        
                elif not has_valid_moves(board, current_player):
                        
                    print(f"{current_player} has no valid moves. Passing turn.")
                    current_player *= -1

        draw_game(screen, board, current_player)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()