import random

import numpy as np

# TODO move the game playing functions to separate file/directory

#  Constants
DRAW = -1
NO_MARKER = 0
PLAYER0_MARKER = 1
PLAYER1_MARKER = 2
NO_LOCAL_BOARD = -1

WIN_INDEXES = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8],
               [0, 4, 8],
               [6, 4, 2],
               [0, 3, 6],
               [1, 4, 7],
               [2, 5, 8]]


# Effectively functional
# Returns the winner marker of the board
def check_3x3_win(board):
    for indexes in WIN_INDEXES:
        if board[indexes[0]] == board[indexes[1]] and \
                board[indexes[1]] == board[indexes[2]] and \
                board[indexes[0]] != NO_MARKER:
            return board[indexes[0]]

    # If no one has won but the board is full, is draw
    if NO_MARKER not in board:
        return DRAW
    return NO_MARKER


# The local board numbers are
# 0 1 2
# 3 4 5
# 6 7 8
#
# The global numbers are of the form
# 0 1 2 | 09 10 11 |
# 3 4 5 | 12 13 14 |
# 6 7 8 | 15 16 17 |


# FUNCTIONAL
# Converts a global square number (0-80) to a local
# pair containing [local_square_number, board_number]
def global_to_local(g):
    lb_num = int(np.floor(g / 9))
    l = g - lb_num * 9
    return [l, lb_num]


# FUNCTIONAL
# Converts a local pair containing [local_square_number, board_number]
# to a global location 0-80
def local_to_global(l):
    return l[0] + 9 * l[1]


# Gets the valid moves based on the global board state and
# the currently active board
def valid_moves(big_board, current_local):
    moves = []
    if current_local == NO_LOCAL_BOARD:
        for i in range(0, 9):
            moves = moves + valid_moves_3x3_global(big_board[i], i)
    else:
        moves = valid_moves_3x3_global(big_board[current_local], current_local)
    return moves


# Returns the valid moves of a 3x3 board converted to global numbers
def valid_moves_3x3_global(board, board_number):
    l_moves = valid_moves_3x3(board)
    moves = []
    for move in l_moves:
        moves.append(local_to_global([move, board_number]))
    return moves


# Returns the playable moves on a basic 3x3 board
def valid_moves_3x3(board):
    moves = []
    for i in range(0, 9):
        val = board[i]
        if val == NO_MARKER:
            moves.append(i)
    return moves


# Marks a big board at the global location given
def mark_big_board(big_board, g_sq, marker):
    local = global_to_local(g_sq)
    big_board[local[1], local[0]] = marker


# Move selection functions (AI and human!)
# TODO move these to their own directory

def random_player(moves):
    return random.choice(moves)


# GAME SPACE
print("Welcome to Ultimate tic tac toe!")

# Initialize empty game state
main_board = np.zeros((9, 9))
main_board_wins = np.zeros((9, 1))
current_local_board = NO_LOCAL_BOARD

# Allows to easily swap players and markers
current_player = 0
markers = [PLAYER0_MARKER, PLAYER1_MARKER]
winner = NO_MARKER

print(main_board)

# GAME LOOP
while winner == NO_MARKER:
    current_marker = markers[current_player]
    all_moves = valid_moves(main_board, current_local_board)

    # TODO make is easy to change out players, also currently doesnt depend on player
    selected_move = random_player(all_moves)

    # move local pair
    move_lp = global_to_local(selected_move)
    local_sq = move_lp[0]
    local_board_number = move_lp[1]

    mark_big_board(main_board, selected_move, current_marker)

    local_winner = check_3x3_win(main_board[local_board_number])

    print(main_board)

    if local_winner > NO_MARKER:
        # If there was a local victory, see then if that ended the game
        main_board_wins[local_board_number] = local_winner
        winner = check_3x3_win(main_board_wins)

    if winner > NO_MARKER:
        print("Player " + str(winner) + "wins")

    elif winner == DRAW:
        print("Draw")

    # Change global-local board to local move value from last time
    current_local_board = local_sq
    current_player = (current_player + 1) % 2

