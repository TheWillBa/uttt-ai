import numpy as np
import pygame
from game import core_gameplay as gp
from game import display as disp

# Each AI function will have its own file to allow for more modular creation
from ai import human, random_ai

# Initialize empty game state
main_board = [0, 0, 0, 0, 0, 0, 0, 0, 0]

# Allows to easily change players and markers
current_player = 0
markers = [gp.PLAYER0_MARKER, gp.PLAYER1_MARKER]
winner = gp.NO_MARKER


#  Pygame initialization
pygame.init()

# Change any display defaults here
disp.SQUARE_SIDE = 100
disp.draw_3x3_board(main_board, disp.X_OFFSET, disp.Y_OFFSET)
pygame.display.flip()


def end_game(w):
    if w > gp.DRAW:
        print("Player " + str(int(w)) + " wins")
    else:
        print("Draw")
    disp.wait_for_player_press()


# GAME LOOP
running = True
while running:

    if winner != gp.NO_MARKER:
        end_game(winner)
        running = False
        continue

    current_marker = markers[current_player]
    all_moves = gp.valid_moves_3x3(main_board, False)

    selected_move = -1

    if current_player == 0:
        selected_move = int(human.human_player(all_moves))
    else:  # player '1'
        pygame.time.delay(1000)
        selected_move = random_ai.random_player(all_moves)

    # move local pair
    move_lp = gp.global_to_local(selected_move)
    local_sq = move_lp[0]

    main_board[local_sq] = current_marker

    winner = gp.check_3x3_win(main_board)

    print(main_board)

    current_player = int((current_player + 1) % 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #  Drawing function
    disp.draw_3x3_board(main_board, disp.X_OFFSET, disp.Y_OFFSET)
    pygame.display.flip()
