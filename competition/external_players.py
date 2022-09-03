"""
This file comprises a portion of the source code of the UTTT referee implementation for the WPI course 'CS 4341:
Introduction to Artificial Intelligence' running A term of the 2022-2023 academic year. Adapted from the Othello
referee code written by Dyllan Cole <dcole@wpi.edu>

File:   external_players.py
Author: William Babincsak <wbabincsak@wpi.edu>
Date:   3 September 2022
"""

import os
import re
import time
from functools import partial
from os import listdir
from os.path import isfile, join
from uttt_game.core_gameplay import BAD_MOVE_I_WIN, BAD_MOVE_I_LOST, local_to_global


def get_competitors(p1_name, p2_name, time_limit):
    return (partial(external_player, name=p1_name, opponent_name=p2_name, time_limit=time_limit),
            partial(external_player, name=p2_name, opponent_name=p1_name, time_limit=time_limit))


def external_player(moves, main_board, local_board_num, my_symbol, opponent_symbol, name, opponent_name, time_limit):

    # todo output some info about the board state

    # Remove old go file if there is one
    old = "{p}.go".format(p=opponent_name)
    if os.path.exists(old):
        os.remove(old)

    # Get last modified time of move file and signal next player to go
    mtime = os.path.getmtime("move_file")
    open("{p}.go".format(p=name), "w").close()

    # Sleep for time_limit seconds checking if move_file has been modified every 50 milliseconds
    modified = False
    for i in range(int(time_limit/0.05)):
        time.sleep(0.05)

        if os.path.getmtime("move_file") > mtime:
            modified = True
            break

    if modified:
        with open("move_file", "r") as fp:
            # Get last non-empty line from file
            line = ""
            for next_line in fp.readlines():
                if next_line.isspace():
                    break
                else:
                    line = next_line

            # Tokenize move
            tokens = line.split()
            group_name = tokens[0]
            global_board = tokens[1]
            local_board = tokens[2]

            # Verify that move is from expected player
            if group_name != name:
                return BAD_MOVE_I_WIN, 'Wrong player moved, causing an immediate loss'

            # Check if move is valid
            if local_to_global((local_board, global_board)) not in moves:
                return BAD_MOVE_I_LOST, f'Player {name} played an invalid move in \nboard: {global_board} \nspace: {local_board}'

    else:
        # Player didn't move in time!
        return BAD_MOVE_I_LOST, f'Player {name} did not move in {time_limit} seconds'



def clean():
    """
    Delete files maintained by Referee
    :return: None
    """
    patterns = [
        re.compile("move_file"),
        re.compile("(:?.*).go"),
        re.compile("end_game")
    ]

    files = [f for f in listdir("./") if isfile(join("./", f))]
    for file in files:
        for pattern in patterns:
            if pattern.match(file):
                os.remove(file)


