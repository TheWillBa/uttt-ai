"""
This is the DRIVER file of the UTTT referee implementation for the WPI course 'CS 4341:
Introduction to Artificial Intelligence' running A term of the 2022-2023 academic year. Adapted from the Othello
referee code written by Dyllan Cole <dcole@wpi.edu>

File:   external_players.py
Author: William Babincsak <wbabincsak@wpi.edu>
Date:   3 September 2022
"""

import argparse
import sys
import random
from external_players import clean, get_competitors
from uttt_game.game import Game

def main():
    """
    Main Referee function
    """

    # Read in arguments from command line
    parser = argparse.ArgumentParser(description="Referee a game of Othello between two programs")
    parser.add_argument("player_one", type=str, help="Group name of player one")
    parser.add_argument("player_two", type=str, help="Group name of player two")
    args = parser.parse_args(sys.argv[1:])


    # Select order randomly
    p1 = args.player_one
    p2 = args.player_two
    if random.choice([True, False]):
        # Swap p1 and p2
        p3 = p1
        p1 = p2
        p2 = p3

    # Clean any pre-existing files
    clean()

    # Create empty move_file
    open("move_file", "w").close()

    # Get the competitor functions
    time_limit = 10
    f_p1, f_p2 = get_competitors(p1, p2, time_limit)

    # Run game
    game = Game(f_p1, f_p2, p1_name=p1, p2_name=p2)
    game.run()


if __name__ == "__main__":
    main()