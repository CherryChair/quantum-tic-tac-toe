from random import sample
from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe


class Player():
    def __init__(self, mark, mode=0):
        """
        Player has one attribute:

        mark - it shows whether player is either "x" or "o".
        """
        self._mark = mark

    def mark(self):
        return self._mark

    def set_mark(self, mark):
        self._mark = mark

    def mark_choice(self, game):
        """
        This function returns squares to player chose to place spooky mark to.
        """
        free_squares = game.available_squares()
        return entanglement_input(free_squares, game)

    def collapse_choice(self, game, added_mark=None):
        """
        This function depending on player mode chooses square for him to
        collapse mark into.
        """
        return collapse_input(added_mark.entanglement())


class Computer_Easy(Player):
    """
    1 - computer player who chooses random action every move
    """
    def mark_choice(self, game):
        """
        Easy comupter player choses two random squares from available squares.
        """
        free_squares = game.available_squares()
        chosen_squares = [0, 0]
        chosen_squares = sample(free_squares, 2)
        return chosen_squares

    def collapse_choice(self, game, added_mark=None):
        """
        If computer player is in mode 1 it choses random square.
        """
        chosen_square = sample(added_mark.entanglement(), 1)[0]
        return chosen_square


class Computer_Hard(Player):
    """
    Computer player who:

    when presented with a choice of collapsing a square decides
    to collapse square that in that order - wins him the game,
    continues the game, is best scorewise. If the game is continued
    after choice and it's possible for him to collapse his mark
    in middle square he does so.

    when presented with choice of putting spooky mark opts for
    placing it in middle square but otherwise chooses everything at random

    """

    def mark_choice(self, game):
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
        return chosen_squares

    def collapse_choice(self, game, added_mark):
        """
        If hard computer player has to choose square to collapse last
        mark into, he chooses square that gives him victory if possible and
        if not, he tries to choose the least harmful outcome with least
        harmful being round continuing and most harmful being losing 0:1.
        If game continues he tries to capture middle square if possible.
        """
        game_a, game_b = game.both_options(added_mark)
        move_number = added_mark.move_number()
        score_a = game_a.win_detection()
        score_b = game_b.win_detection()
        player_mark = player_detection(move_number + 1)
        opponent_mark = player_detection(move_number)
        priority_a = 0
        priority_b = 0
        entanglement = added_mark.entanglement()
        if score_a:
            if score_a[player_mark] == 1:
                return entanglement[0]
            if score_a[opponent_mark] == 1 and score_a[player_mark] == 0:
                priority_a = 3
            if score_a[opponent_mark] == 1 and score_a[player_mark] == 0.5:
                priority_a = 2
            if score_a[opponent_mark] == 0.5 and score_a[player_mark] == 0.5:
                priority_a = 1
        if score_b:
            if score_b[player_mark] == 1:
                return entanglement[1]
            if score_b[opponent_mark] == 1 and score_b[player_mark] == 0:
                priority_b = 3
            if score_b[opponent_mark] == 1 and score_b[player_mark] == 0.5:
                priority_b = 2
            if score_b[opponent_mark] == 0.5 and score_b[player_mark] == 0.5:
                priority_b = 1
        if priority_a == 0:
            if game_a.squares()[5][0]:
                if game_a.squares()[5][1].mark() == player_mark:
                    return entanglement[0]
        if priority_b == 0:
            if game_b.squares()[5][0]:
                if game_b.squares()[5][1].mark() == player_mark:
                    return entanglement[1]
        if priority_a == priority_b:
            chosen_game = sample(entanglement, 1)[0]
            return chosen_game
        if priority_b < priority_a:
            return entanglement[0]
        return entanglement[1]


def player_detection(move_number):
    """
    Since x's move numbers are odd and o's move numbers are even we
    can use this function to determine what player's mark is when all
    we have is move number.
    """
    if move_number % 2:
        return 'x'
    return 'o'
