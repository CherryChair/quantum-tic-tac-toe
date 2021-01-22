from random import sample, choice
from mark_class import Mark, proper_mark_check
from quantum_tic_tac_toe_class import (
    NoUnresolvedCycleInGame,
    UnresolvedCycleInGame,
    InvalidStartingMoveError
)


class WrongPlayerTurn(Exception):
    pass


def collapse_data_check(game):
    from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe
    if not isinstance(game, Quantum_Tic_Tac_Toe):
        raise TypeError("Game must be of Quantum_Tic_Tac_Toe_Type")
    if not game._unresolved_cycle:
        message = "Game does not have unresolved cycle"
        raise NoUnresolvedCycleInGame(message)


def mark_data_check(game):
    from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe
    if not isinstance(game, Quantum_Tic_Tac_Toe):
        raise TypeError("Game must be of Quantum_Tic_Tac_Toe_Type")
    if game._unresolved_cycle:
        raise UnresolvedCycleInGame("Game has unresolved cycle")


class Player():
    def __init__(self, mark, score=0):
        """
        Player has two attributes:

        mark - it shows whether player is either "x" or "o".

        player_score - shows player score
        """
        if not isinstance(score, (float, int)):
            raise TypeError("Score must be a number")
        mark = proper_mark_check(mark)
        self._mark = mark
        self._score = score

    def mark(self):
        return self._mark

    def set_mark(self, mark):
        mark = proper_mark_check(mark)
        self._mark = mark

    def score(self):
        return self._score

    def add_score(self, score):
        if not isinstance(score, (float, int)):
            raise TypeError("Score must be a number")
        self._score += score

    """
    mark_choice and collapse_choice function are used when we want player to
    make a decision, but decision-making functions are _mark_decision and
    _collapse_choice. This separation lets us implement gui easier and better,
    because we do not need to copy decision-making function for each player,
    we only need to change function returning decision to game
    """
    def mark_choice(self, game):
        """
        Returns choice of spooky mark placement for player who is using it.
        """
        if game.last_placed_mark() is None:
            if self.mark() == "o":
                raise InvalidStartingMoveError
        elif game.last_placed_mark().mark() == self.mark():
            message = "It is other players' turn to choose"
            raise WrongPlayerTurn(message)
        chosen_squares = self._mark_decision(game)
        return chosen_squares

    def collapse_choice(self, game):
        """
        Given game with unresolved cycle returns collapse choice of player
        who is using it.
        """
        added_mark = game.last_placed_mark()
        if added_mark.mark() == self.mark():
            message = "It is other players' turn to choose"
            raise WrongPlayerTurn(message)
        chosen_square = self._collapse_decision(game, added_mark)
        return chosen_square

    def _mark_decision(self, game, user_input=None):
        """
        This function returns decision of player who has to move when there's
        no unresolved cycle.
        """
        mark_data_check(game)
        return user_input

    def _collapse_decision(self, game, added_mark, user_input=None):
        """
        This function returns decision of player who has to resolve cycle.
        """
        collapse_data_check(game)
        return user_input


class Computer_Easy(Player):
    """
    Computer player who chooses random action every move
    """

    def _mark_decision(self, game):
        """
        Easy comupter player choses two random squares from available squares.
        """
        mark_data_check(game)
        free_squares = game.available_squares()
        chosen_squares = [0, 0]
        chosen_squares = sample(free_squares, 2)
        return chosen_squares

    def _collapse_decision(self, game, added_mark):
        """
        If computer player is in mode 1 it choses random square.
        """
        if not isinstance(added_mark, Mark):
            raise TypeError("added_mark must be a Mark class instance")
        collapse_data_check(game)
        chosen_square = choice(added_mark.entanglement())
        return chosen_square


class Computer_Hard(Player):
    """
    Computer player who:

    when presented with a choice of collapsing a square decides
    to collapse square that in that order:
    - wins him the game,
    - continues the game,
    - is best scorewise.
    If the game is continued after choice and it's possible for him
    to collapse his mark in middle square he does so.

    when presented with choice of putting spooky mark opts for
    placing it in middle square but if it's not possible
    chooses everything at random

    """

    def _mark_decision(self, game):
        """
        Hard computer player choses two random squares
        from available squares with preffered square being middle one.
        """
        mark_data_check(game)
        free_squares = game.available_squares()
        chosen_squares = [0, 0]
        if 5 in free_squares:
            chosen_squares = [5] + sample(free_squares.difference({5}), 1)
        else:
            chosen_squares = sample(free_squares, 2)
        return chosen_squares

    def _collapse_decision(self, game, added_mark):
        """
        If hard computer player has to choose square to collapse last
        mark into, he chooses square that gives him victory if possible and
        if not, he tries to choose the least harmful outcome with least
        harmful being round continuing and most harmful being losing 0:1.
        If game continues he tries to capture middle square if possible.
        """
        collapse_data_check(game)
        game_a, game_b = game.both_cycle_resolution_options()
        score_a = game_a.win_detection()
        score_b = game_b.win_detection()
        player_mark = self.mark()
        opponent_mark = added_mark.mark()
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
            chosen_game = choice(entanglement)
            return chosen_game
        if priority_b < priority_a:
            return entanglement[1]
        return entanglement[0]
