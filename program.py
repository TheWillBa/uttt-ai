import random
import numpy as np
import pygame
from game import core_gameplay as gp


# Move selection functions (AI and human!)
# TODO move these to their own directory too

def random_player(moves):
    return random.choice(moves)


# GAME SPACE
print("Welcome to Ultimate tic tac toe!")

# Initialize empty game state
main_board = np.zeros((9, 9))
main_board_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
current_local_board = gp.NO_LOCAL_BOARD

# Allows to easily swap players and markers
current_player = 0
markers = [gp.PLAYER0_MARKER, gp.PLAYER1_MARKER]
winner = gp.NO_MARKER

print(main_board)

#  Pygame initialization
pygame.init()
SCREEN = pygame.display.set_mode([500, 500])
OVERLAYER = pygame.Surface((500, 500), pygame.SRCALPHA)
SQUARE_SIDE = 50
P0_COLOR = (0, 0, 255)
P1_COLOR = (255, 0, 0)


# (left, top, width, height)
def draw_3x3_board(board, x, y):
    for i in range(0, 3):
        for j in range(0, 3):
            pygame.draw.rect(SCREEN, (255, 255, 255),
                             (x + i * SQUARE_SIDE, y + j * SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE))
            pygame.draw.rect(SCREEN, (0, 0, 0),
                             (x + i * SQUARE_SIDE, y + j * SQUARE_SIDE, SQUARE_SIDE, SQUARE_SIDE), width=1)

            if board[3 * j + i] == gp.PLAYER0_MARKER:
                pygame.draw.circle(SCREEN, P0_COLOR,
                                   (x + i * SQUARE_SIDE + SQUARE_SIDE / 2, y + j * SQUARE_SIDE + SQUARE_SIDE / 2),
                                   SQUARE_SIDE / 2 * 0.9)

            if board[3 * j + i] == gp.PLAYER1_MARKER:
                pygame.draw.circle(SCREEN, P1_COLOR,
                                   (x + i * SQUARE_SIDE + SQUARE_SIDE / 2, y + j * SQUARE_SIDE + SQUARE_SIDE / 2),
                                   SQUARE_SIDE / 2 * 0.9)


def draw_big_board(bb, x, y):
    for i in range(0, 3):
        for j in range(0, 3):
            draw_3x3_board(bb[3 * j + i], x + 3 * i * SQUARE_SIDE, y + 3 * j * SQUARE_SIDE)


# Draws an overlay over board number local_num
# on big board with top left at x, y
def draw_board_overlay(local_num, x, y):
    yl = int(np.floor(local_num / 3))
    xl = local_num - yl * 3
    pygame.draw.rect(OVERLAYER, (255, 255, 0, 100),
                     (x + 3 * xl * SQUARE_SIDE, y + 3 * yl * SQUARE_SIDE, 3 * SQUARE_SIDE, 3 * SQUARE_SIDE))


draw_big_board(main_board, 0, 0)
# GAME LOOP

running = True
while winner == gp.NO_MARKER and running:
    print("________________________________________")
    current_marker = markers[current_player]
    all_moves = gp.valid_moves(main_board, current_local_board)

    # TODO fix error of playing into a full board better later
    if len(all_moves) < 1:
        current_local_board = gp.NO_LOCAL_BOARD

    all_moves = gp.valid_moves(main_board, current_local_board)

    # TODO make is easy to change out players, also currently doesn't depend on player
    selected_move = random_player(all_moves)

    # move local pair
    move_lp = gp.global_to_local(selected_move)
    local_sq = move_lp[0]
    local_board_number = move_lp[1]

    gp.mark_big_board(main_board, selected_move, current_marker)

    local_winner = gp.check_3x3_win(main_board[local_board_number])

    print(main_board)

    if local_winner != gp.NO_MARKER:
        # If there was a local victory, see then if that ended the game
        main_board_wins[local_board_number] = local_winner
        winner = gp.check_3x3_win(main_board_wins)

    # print("main wins: " + str(main_board_wins))

    if winner > gp.NO_MARKER:
        print("Player " + str(winner) + " wins")

    elif winner == gp.DRAW:
        print("Draw")

    # Change global-local board to local move value from last time
    current_local_board = local_sq
    current_player = int((current_player + 1) % 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_big_board(main_board, 0, 0)
    OVERLAYER.fill((0, 0, 0, 0))
    draw_board_overlay(current_local_board, 0, 0)
    SCREEN.blit(OVERLAYER, (0, 0))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                waiting = False
