from game import core_gameplay as gp
from ai import random_ai as rai
import numpy as np


# Returns a list of the local indexed (0-8) moves that a given player can
# play to win the board
def local_moves_to_win(board, player):
    my_moves = []

    local_valid_moves = gp.valid_moves_3x3(board, False)
    for move in local_valid_moves:
        board[move] = player
        if gp.check_3x3_win(board) == player:
            my_moves.append(move)
        board[move] = gp.NO_MARKER

    return my_moves


def list_local_to_global(local_moves, board_number):
    return list((map(lambda m: gp.local_to_global([m, board_number]), local_moves)))


# This AI plays a naive, greedy approach to UTTT. It considers the current local board only
# and plays to win the local board if it can, block the other player if it can, and plays randomly
# when there isn't a local board to play on

# Inputs are: valid_moves, main_board, local_board_num, my_symbol, opponent_symbol
def simple_local_ai(valid_moves, main_board, local_board_num, my_symbol, opponent_symbol):
    # Only handles cases when there is a local board
    if local_board_num == gp.NO_LOCAL_BOARD:
        return rai.random_player(valid_moves)

    board = main_board[local_board_num]

    my_winning_moves = list_local_to_global(local_moves_to_win(board, my_symbol), local_board_num)
    opponent_winning_moves = list_local_to_global(local_moves_to_win(board, opponent_symbol), local_board_num)

    # check if opponent can win, but only add to my moves after since we will just be picking first from the list

    if len(my_winning_moves) > 0:
        return my_winning_moves[0]

    if len(opponent_winning_moves) > 0:
        return opponent_winning_moves[0]

    return rai.random_player(valid_moves)


# For comparision against the version that uses mutation
# Inputs are: valid_moves, main_board, local_board_num, my_symbol, opponent_symbol
def simple_local_ai_no_mutation(valid_moves, main_board, local_board_num, my_symbol, opponent_symbol):
    # Only handles cases when there is a local board
    if local_board_num == gp.NO_LOCAL_BOARD:
        return rai.random_player(valid_moves)

    board = main_board[local_board_num]

    my_moves = []
    # This method is not like racket, actually modifies the game board while doing processing,
    # I imagine that this is faster than copying it a million times, but perhaps less scalable?
    # Definitely not scalable to parallel processing
    local_valid_moves = gp.valid_moves_3x3(board, False)
    for move in local_valid_moves:
        board_copy = np.copy(board)
        board_copy[move] = my_symbol
        if gp.check_3x3_win(board_copy) == my_symbol:
            my_moves.append(gp.local_to_global([move, local_board_num]))

    # check if opponent can win, but only add to my moves after since we will just be picking first from the list
    for move in local_valid_moves:
        board_copy = np.copy(board)
        board_copy[move] = opponent_symbol
        if gp.check_3x3_win(board_copy) == opponent_symbol:
            my_moves.append(gp.local_to_global([move, local_board_num]))

    if len(my_moves) > 0:
        return my_moves[0]

    return rai.random_player(valid_moves)
