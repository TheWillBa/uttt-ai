import numpy as np

#  Constants
NO_MARKER = 0
PLAYER1_MARKER = 1
PLAYER2_MARKER = 2
X = PLAYER1_MARKER
O = PLAYER2_MARKER

NO_LOCAL_BOARD = -1

main_board = np.zeros((9, 9))
main_board_wins = np.zeros((3, 3))

current_local_board = NO_LOCAL_BOARD


# Places the player marker pm in the square sq of the current local board
# sq must be between 1 and 9, inclusive

def play_local_in_current(sq, pm):
    # TODO check for invalid input
    main_board[current_local_board, sq] = pm


win_indexes = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8],
               [0, 4, 8],
               [6, 4, 2],
               [0, 3, 6],
               [1, 4, 7],
               [2, 5, 8]]


# Returns the winner marker of the board,
def check_3x3_win(board):
    for indexes in win_indexes:
        if board[indexes[0]] == board[indexes[1]] and \
                board[indexes[1]] == board[indexes[2]] and \
                board[indexes[0]] != NO_MARKER:
            return indexes[0]
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


# Converts a global square number (0-80) to a local
# pair containing [local_square_number, board_number]
def global_to_local(g):
    lb_num = int(np.floor(g / 9))
    l = g - lb_num * 9
    return [l, lb_num]


# Converts a local pair containing [local_square_number, board_number]
# to a global location 0-80
def local_to_global(l):
    return l[0] + 9 * l[1]


for i in range(0, 81):
    print(str(i) + " " + str(local_to_global(global_to_local(i))))
