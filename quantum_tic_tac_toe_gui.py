from PySide2.QtWidgets import QMainWindow, QApplication, QWidget
from PySide2.QtGui import QPixmap
from ui_quantum_tic_tac_toe import Ui_MainWindow
from ui_rules_window import Ui_rulesWidget

import sys

from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe
from player_class import Player, Computer_Easy, Computer_Hard
from mark_class import Mark


class QuantumTicTacToeWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.squares = {}
        self.ui.player1Easy.stateChanged.connect(self.display_state_of_game)
        self.ui.player1Hard.stateChanged.connect(self.display_state_of_game)
        self.ui.player1Human.stateChanged.connect(self.display_state_of_game)
        self.ui.player2Easy.stateChanged.connect(self.display_state_of_game)
        self.ui.player2Hard.stateChanged.connect(self.display_state_of_game)
        self.ui.player2Human.stateChanged.connect(self.display_state_of_game)
        self.ui.startButton.clicked.connect(self.begin_game)
        self.ui.rulesButton.clicked.connect(self.display_rules)

    def clear_player2checkboxes(self):
        easy_checkbox = self.ui.player2Easy
        hard_checkbox = self.ui.player2Hard
        human_checkbox = self.ui.player2Human
        list_of_player_2_checkboxes = [easy_checkbox, hard_checkbox, human_checkbox]
        for checkbox in list_of_player_2_checkboxes:
            if checkbox.isChecked():
                checkbox.nextCheckState()

    def begin_game(self):
        self.ui.matchOutcomeLabel.clear()
        self.ui.player1Score.setText("0")
        self.ui.player2Score.setText("0")
        number_of_rounds = self.ui.roundsSpinBox.value()
        player_1, player_2 = self.player_choice()
        for round_number in range(number_of_rounds):
            player_1_score = float(self.ui.player1Score.text())
            player_2_score = float(self.ui.player2Score.text())
            if not round_number % 2:
                player_1.set_mark("x")
                player_2.set_mark("o")
                x_score, o_score = self.one_round(player_1, player_2)
                self.ui.matchOutcomeLabel.setText(f"X: {x_score}, O: {o_score}")
                self.ui.player1Score.setText(f'{player_1_score + x_score}')
                self.ui.player2Score.setText(f'{player_2_score + o_score}')
            else:
                player_1.set_mark("o")
                player_2.set_mark("x")
                x_score, o_score = self.one_round(player_2, player_1)
                self.ui.matchOutcomeLabel.setText(f"X: {x_score}, O: {o_score}")
                self.ui.player1Score.setText(f'{player_1_score + o_score}')
                self.ui.player2Score.setText(f'{player_2_score + x_score}')
            self.display_state_of_game()
        player_1_score = float(self.ui.player1Score.text())
        player_2_score = float(self.ui.player2Score.text())
        if player_1_score > player_2_score:
            self.ui.matchOutcomeLabel.setText("Player 1 won")
        elif player_1_score < player_2_score:
            self.ui.matchOutcomeLabel.setText("Player 2 won")
        else:
            self.ui.matchOutcomeLabel.setText("Tie")

    def player_choice(self):
        if self.ui.player1Easy.isChecked():
            player_1 = Computer_Easy("x")
        elif self.ui.player1Hard.isChecked():
            player_1 = Computer_Hard("x")
        else:
            player_1 = Player("x")
        if self.ui.player2Easy.isChecked():
            player_2 = Computer_Easy("o")
        elif self.ui.player2Hard.isChecked():
            player_2 = Computer_Hard("o")
        else:
            player_2 = Player("o")
        return player_1, player_2

    def clear_squares(self):
        squares = self.squares
        for square in squares:
            pixmap = QPixmap()
            self.ui.big_label9.setPixmap(pixmap)
            eval(f"self.ui.big_label{square}.clear()")
            for i in range(1, 10):
                eval(f"self.ui.label{square}_{i}.clear()")

    def display_state_of_game(self):
        self.clear_squares()
        squares = self.squares
        for square in squares:
            if squares[square][0]:
                collapsed_mark = squares[square][1]
                mark = collapsed_mark.mark()
                move_number = collapsed_mark.move_number()
                pixmap = QPixmap(f"mark_pics/big_{mark}_{move_number}")
                eval(f"self.ui.big_label{square}.setPixmap(pixmap)")
            else:
                for index, mark in enumerate(squares[square][1:]):
                    sign = mark.mark()
                    move_number = mark.move_number()
                    pixmap = QPixmap(f"mark_pics/small_{sign}_{move_number}")
                    eval(f"self.ui.label{square}_{index+1}.setPixmap(pixmap)")

    def entanglement_input(self, free_squares):
        pass

    def collapse_input(self, entanglement):
        pass

    def one_round(self, player_1, player_2):
        q = Quantum_Tic_Tac_Toe()
        move_number = 0
        winner = False
        while not winner:
            move_number += 1
            winner = move(q, move_number, player_1, player_2)
            self.squares = q.squares()
            self.display_state_of_game()
            player_1, player_2 = player_2, player_1
        x_score = winner['x']
        o_score = winner['o']
        if x_score == 1:
            pass
        elif o_score == 1:
            pass
        else:
            pass
        return x_score, o_score

    def mark_choice(self, game):
        free_squares = game.available_squares()
        for square in free_squares:
            eval(f"self.ui.button{square}.clicked.connect(self.entanglement_choice)")

    def display_rules(self):
        new_window = RulesWindow()
        new_window.exec_()

class RulesWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_rulesWidget()
        self.ui.setupUi(self)



def guiMain(args):
    app = QApplication(args)
    window = QuantumTicTacToeWindow()
    window.show()
    return app.exec_()


def move(game, move_number, player, opponent):
    """
    We use this function to go through one placement of mark during
    Quantum Tic Tac Toe game.
    First variable is quantum_tic_tac_toe game.
    Second variable is current move number.
    Third is player who is moving.
    Fourth is opponent of the player who is moving.
    """
    mark = player.mark()
    entanglement = player.mark_choice(game)
    mark = Mark(mark, entanglement, move_number)
    game.add_entangled_mark(mark)
    new_path, cycle = game.paths_update(entanglement)
    if cycle:
        choice = player.collapse_choice(game, mark)
        game.collapse_squares(mark, choice)
    win = game.win_detection()
    if not win:
        return False
    return win


if __name__ == "__main__":
    guiMain(sys.argv)
