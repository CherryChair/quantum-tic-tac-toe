from player_class import Player, Computer_Hard, Computer_Easy
from quantum_tic_tac_toe_gui import QuantumTicTacToeWindow
from random import sample


class Gui_Human_Player(Player):
    pass


class Gui_Computer_Easy(Computer_Easy):
    pass


class Gui_Computer_Hard(Computer_Hard):
    def mark_choice(self, game, entanglement=None, gui=None):
        """
        Hard computer player choses two random squares
        from available squares with preffered square being middle one.
        """
        free_squares = game.available_squares()
        chosen_squares = [0, 0]
        if 5 in free_squares:
            chosen_squares = [5] + sample(free_squares.difference({5}), 1)
        else:
            chosen_squares = sample(free_squares, 2)
        if gui:
            return chosen_squares
