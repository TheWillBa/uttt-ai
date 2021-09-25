import random
import numpy as np
import pygame
from game import core_gameplay as gp


# Move selection functions (AI and human!)
# TODO move these to their own directory too

def random_player(moves):
    return random.choice(moves)


def human_player(moves):
    # move_xys = list(map(lambda move: global_to_xy(move), moves))
    # for x, y in move_xys:
    #     pygame.draw.rect(OVERLAYER, (0, 255, 0, 100), (x, y, SQUARE_SIDE, SQUARE_SIDE))

    # SCREEN.blit(OVERLAYER, (0, 0))
    # pygame.display.flip()
    # wait_for_player_press()

    move_selected = False
    move = -1
    while not move_selected:
        xy = -1
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    xy = pygame.mouse.get_pos()
                    waiting = False

        move = xy_to_global(xy)
        if move in moves:
            move_selected = True

    return move


# Returns the x, y positions in screen space of the top left corner of the
# square representing the global space given
# x and y parameters are offsets from the
def global_to_xy(move):
    square_num, board_num = gp.global_to_local(move)

    # TODO Make these local xy converters separate functions
    yls = int(np.floor(square_num / 3))
    xls = square_num - yls * 3

    ylb = int(np.floor(board_num / 3))
    xlb = board_num - ylb * 3

    x = X_OFFSET + 3 * SQUARE_SIDE * xlb + SQUARE_SIDE * xls
    y = Y_OFFSET + 3 * SQUARE_SIDE * ylb + SQUARE_SIDE * yls
    return [x, y]


def xy_to_global(xy):
    x, y = xy
    x = x - X_OFFSET
    y = y - Y_OFFSET

    ylb = np.floor(y / (3 * SQUARE_SIDE))
    xlb = np.floor(x / (3 * SQUARE_SIDE))

    yls = np.floor((y - ylb * 3 * SQUARE_SIDE) / SQUARE_SIDE)
    xls = np.floor((x - xlb * 3 * SQUARE_SIDE) / SQUARE_SIDE)

    return gp.local_to_global([xy_to_global_3x3(xls, yls), xy_to_global_3x3(xlb, ylb)])


def xy_to_global_3x3(x, y):
    return 3 * y + x


def wait_for_player_press():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                waiting = False


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
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
SCREEN = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
OVERLAYER = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
SQUARE_SIDE = 50
P0_COLOR = (0, 0, 255)
P1_COLOR = (255, 0, 0)
X_OFFSET = 0
Y_OFFSET = 0


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
def draw_board_overlay(local_num, x, y, color):
    yl = int(np.floor(local_num / 3))
    xl = local_num - yl * 3
    pygame.draw.rect(OVERLAYER, color,
                     (x + 3 * xl * SQUARE_SIDE, y + 3 * yl * SQUARE_SIDE, 3 * SQUARE_SIDE, 3 * SQUARE_SIDE))


#  Colors an overlay over all sub-boards that have been won
#  Colors based on the winner of the board
def overlay_decided(board_wins, x, y):
    for i in range(0, 9):
        marker = board_wins[i]
        color = (0, 0, 0, 0)
        if marker == gp.PLAYER0_MARKER:
            # TODO make based on color variables
            color = (0, 0, 255, 100)
        elif marker == gp.PLAYER1_MARKER:
            color = (255, 0, 0, 100)
        elif marker == gp.DRAW:
            color = (0, 0, 0, 100)
        else:
            continue

        draw_board_overlay(i, x, y, color)


draw_big_board(main_board, X_OFFSET, Y_OFFSET)
pygame.display.flip()
# GAME LOOP
# TODO CLEAN UP THE MESS OF DISPLAY FUNCTIONS UP HERE

running = True
while running:



    if winner > gp.NO_MARKER:
        print("Player " + str(winner) + " wins")
        running = False
        wait_for_player_press()
        continue

    elif winner == gp.DRAW:
        print("Draw")
        running = False
        wait_for_player_press()
        continue

    print("________________________________________")
    current_marker = markers[current_player]
    all_moves = gp.valid_moves(main_board, current_local_board)

    # TODO make is easy to change out players, also currently doesn't depend on player
    selected_move = -1

    if current_player == 0:
        selected_move = int(human_player(all_moves))
    else:  # player '1'
        pygame.time.delay(1000)
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



    # Change global-local board to local move value from last time IF it has valid moves
    if len(gp.valid_moves_3x3(main_board[local_sq])) > 0:
        current_local_board = local_sq
    else:
        current_local_board = gp.NO_LOCAL_BOARD

    current_player = int((current_player + 1) % 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_big_board(main_board, X_OFFSET, Y_OFFSET)
    OVERLAYER.fill((0, 0, 0, 0))
    overlay_decided(main_board_wins, X_OFFSET, Y_OFFSET)
    draw_board_overlay(current_local_board, X_OFFSET, Y_OFFSET, (255, 255, 0, 100))
    SCREEN.blit(OVERLAYER, (0, 0))
    pygame.display.flip()

