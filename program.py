import numpy as np
import pygame
from game import core_gameplay as gp
from game import display as disp

# Each AI function will have its own file to allow for more modular creation
from ai import human, random_ai, simple_local_ai

# Initialize empty game state
# This is really all of the data the AI will have as input to
# make decisions, other than potentially whether it went first or second
# or maybe even how long the game has gone on for?
# Also all of the option rule variables
main_board = np.zeros((9, 9))
main_board_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
current_local_board = gp.NO_LOCAL_BOARD

# Allows to easily change players and markers
current_player = 0
markers = [gp.PLAYER0_MARKER, gp.PLAYER1_MARKER]
winner = gp.NO_MARKER

# Optional Rule Variables

# True allows you to send opponents to won boards (Thad rules)
# False means won boards are off limits (Real rules)
can_move_in_won_board = False

# True makes the game a draw when a player is sent to a full square (Thad rules)
# False allows the player to play in any free space (Real rules)
send_to_full_board_is_draw = False

#  Pygame initialization
pygame.init()

# Change any display defaults here
disp.draw_game_board(main_board, main_board_wins, current_local_board, disp.X_OFFSET, disp.Y_OFFSET)


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
    all_moves = gp.valid_moves(main_board, current_local_board, can_move_in_won_board)

    selected_move = -1

    if current_player == 0:
        selected_move = int(human.human_player(all_moves))
    else:  # player '1'
        pygame.time.delay(500)
        # selected_move = random_ai.random_player(all_moves)
        stime = pygame.time.get_ticks()
        mutable_move = simple_local_ai.simple_local_ai(all_moves, main_board, current_local_board, gp.PLAYER1_MARKER,
                                                       gp.PLAYER0_MARKER)
        mutable_time = pygame.time.get_ticks() - stime
        stime = pygame.time.get_ticks()
        copy_move = simple_local_ai.simple_local_ai_no_mutation(all_moves, main_board, current_local_board,
                                                                gp.PLAYER1_MARKER,
                                                                gp.PLAYER0_MARKER)
        copy_time = pygame.time.get_ticks() - stime

        print("Time for mutable: " + str(mutable_time))
        print("Time for copying: " + str(copy_time))

        if mutable_move != copy_move:
            print("FUCK")

        selected_move = copy_move

    # move local pair
    move_lp = gp.global_to_local(selected_move)
    local_sq = move_lp[0]
    local_board_number = move_lp[1]

    if gp.handle_mark_big_board(main_board, selected_move, current_marker, main_board_wins) > -1:
        winner = gp.check_3x3_win(main_board_wins)

    print(main_board)

    # Change global-local board to local move value from last time IF it has valid moves
    if len(gp.valid_moves_3x3(main_board[local_sq], can_move_in_won_board)) > 0:
        current_local_board = local_sq
    elif send_to_full_board_is_draw:
        winner = gp.DRAW
        # For display purposes
        current_local_board = gp.NO_LOCAL_BOARD
    else:
        current_local_board = gp.NO_LOCAL_BOARD

    current_player = int((current_player + 1) % 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #  Drawing function
    disp.draw_game_board(main_board, main_board_wins, current_local_board, disp.X_OFFSET, disp.Y_OFFSET)
