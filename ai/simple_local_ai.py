from game import core_gameplay as gp
from ai import random_ai as rai
import numpy as np


# Train ML AI to play against all the different 'naive' algorithms to see what happens
# What can advanced AI learn from naive approaches?


# This AI plays a naive, greedy approach to UTTT. It considers the current local board only
# and plays to win the local board if it can, block the other player if it can, and plays randomly
# when there isn't a local board to play on

# Inputs are: valid_moves, main_board, local_board_num, my_symbol, opponent_symbol
def simple_local_ai(valid_moves, main_board, local_board_num, my_symbol, opponent_symbol):
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
        board[move] = my_symbol
        if gp.check_3x3_win(board) == my_symbol:
            my_moves.append(gp.local_to_global([move, local_board_num]))
        board[move] = gp.NO_MARKER

    # check if opponent can win, but only add to my moves after since we will just be picking first from the list
    for move in local_valid_moves:
        board[move] = opponent_symbol
        if gp.check_3x3_win(board) == opponent_symbol:
            my_moves.append(gp.local_to_global([move, local_board_num]))
        board[move] = gp.NO_MARKER

    if len(my_moves) > 0:
        return my_moves[0]

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
