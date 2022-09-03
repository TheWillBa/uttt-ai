import numpy as np
import pygame
import core_gameplay as gp
import display as disp

# Each AI function will have its own file to allow for more modular creation
from ai import human, random_ai, simple_local_ai

class Game:
    def __init__(self, f_p1, f_p2, p1_name=None, p2_name=None):
        self.names = [gp.PLAYER0_MARKER if p1_name is None else p1_name,
                      gp.PLAYER1_MARKER if p2_name is None else p2_name]
        self.f_p1 = f_p1
        self.f_p2 = f_p2
        # Initialize empty game state
        self.main_board = np.zeros((9, 9))
        self.main_board_wins = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.current_local_board = gp.NO_LOCAL_BOARD

        # Allows to easily change players and markers
        self.current_player = 0
        self.markers = [gp.PLAYER0_MARKER, gp.PLAYER1_MARKER]
        self.winner = gp.NO_MARKER

        # Optional Rule Variables

        # True allows you to send opponents to won boards (Thad rules)
        # False means won boards are off limits (Classic rules)
        self.can_move_in_won_board = True

        # True makes the game a draw when a player is sent to a full square (Thad rules)
        # False allows the player to play in any free space (Classic rules)
        self.send_to_full_board_is_draw = True

        #  Pygame initialization
        pygame.init()

    def run(self):
        #  Drawing function
        disp.draw_game_board(self.main_board, self.main_board_wins, self.current_local_board, disp.X_OFFSET, disp.Y_OFFSET)
        # GAME LOOP
        running = True
        while running:

            if self.winner != gp.NO_MARKER:
                self.end_game()
                running = False
                continue

            current_marker = self.markers[self.current_player]
            all_moves = gp.valid_moves(self.main_board, self.current_local_board, self.can_move_in_won_board)

            if self.current_player == 0:
                selected_move = int(self.f_p1(all_moves, self.main_board, self.current_local_board,
                                 gp.PLAYER0_MARKER, gp.PLAYER1_MARKER))
            else:
                selected_move = int(self.f_p2(all_moves, self.main_board, self.current_local_board,
                                gp.PLAYER1_MARKER, gp.PLAYER0_MARKER))

            # todo handle if selected_move is bad

            # move local pair
            move_lp = gp.global_to_local(selected_move)
            local_sq = move_lp[0]

            if gp.handle_mark_big_board(self.main_board, selected_move, current_marker, self.main_board_wins) > -1:
                self.winner = gp.check_3x3_win(self.main_board_wins)

            print(self.main_board)

            # Change global-local board to local move value from last time IF it has valid moves
            if len(gp.valid_moves_3x3(self.main_board[local_sq], self.can_move_in_won_board)) > 0:
                self.current_local_board = local_sq
            elif self.send_to_full_board_is_draw:
                self.winner = gp.DRAW
                # For display purposes
                self.current_local_board = gp.NO_LOCAL_BOARD
            else:
                self.current_local_board = gp.NO_LOCAL_BOARD

            self.current_player = int((self.current_player + 1) % 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            #  Drawing function
            disp.draw_game_board(self.main_board, self.main_board_wins, self.current_local_board, disp.X_OFFSET, disp.Y_OFFSET)

    def current_player_name(self) -> str:
        return str(self.names[int(self.current_player-1)])

    def end_game(self):
        if self.winner > gp.DRAW:
            print("Player " + str(self.names[int(self.winner-1)]) + " wins")
        else:
            print("Draw")
        disp.wait_for_player_press()


if __name__ == "__main__":
    game = Game(human.human_player, human.human_player, p1_name='Will', p2_name='Will2')
    game.run()




