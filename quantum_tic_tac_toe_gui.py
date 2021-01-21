from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PySide2.QtGui import QPixmap
from PySide2.QtCore import QEventLoop
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
        self.game = Quantum_Tic_Tac_Toe()
        self.player1 = Player("x")
        self.player2 = Player("o")
        self.player1_clicked_checkbox = []
        self.player2_clicked_checkbox = []
        self.player_entanglement_choice = []
        self.player_collapse_choice = 0
        self.big_button_list = []
        self.small_button_list = []
        for i in range(1, 10):
            self.big_button_list.append(eval(f"self.ui.big_label{i}"))
        for i in range(1, 10):
            small_button_square = []
            for j in range(1, 10):
                small_button_square.append(eval(f"self.ui.label{i}_{j}"))
            self.small_button_list.append(small_button_square)
        self.ui.player1Easy.clicked.connect(self.clear_player1checkboxes)
        self.ui.player1Hard.clicked.connect(self.clear_player1checkboxes)
        self.ui.player1Human.clicked.connect(self.clear_player1checkboxes)
        self.ui.player2Easy.clicked.connect(self.clear_player2checkboxes)
        self.ui.player2Hard.clicked.connect(self.clear_player2checkboxes)
        self.ui.player2Human.clicked.connect(self.clear_player2checkboxes)
        self.ui.startButton.clicked.connect(self.begin_game)
        self.ui.rulesButton.clicked.connect(self.display_rules)
        self.ui.player1Human.click()
        self.ui.player2Human.click()

    def clear_player1checkboxes(self):
        easy_checkbox = self.ui.player1Easy
        hard_checkbox = self.ui.player1Hard
        human_checkbox = self.ui.player1Human
        player_1_checkboxes = [easy_checkbox, hard_checkbox, human_checkbox]
        clicked_checkbox = self.player1_clicked_checkbox
        for checkbox in player_1_checkboxes:
            if checkbox.isChecked():
                if checkbox not in clicked_checkbox:
                    clicked_checkbox.append(checkbox)
                else:
                    clicked_checkbox.remove(checkbox)
                    checkbox.setChecked(False)
        self.player1_clicked_checkbox = clicked_checkbox

    def clear_player2checkboxes(self):
        easy_checkbox = self.ui.player2Easy
        hard_checkbox = self.ui.player2Hard
        human_checkbox = self.ui.player2Human
        player_2_checkboxes = [easy_checkbox, hard_checkbox, human_checkbox]
        clicked_checkbox = self.player2_clicked_checkbox
        for checkbox in player_2_checkboxes:
            if checkbox.isChecked():
                if checkbox not in clicked_checkbox:
                    clicked_checkbox.append(checkbox)
                else:
                    clicked_checkbox.remove(checkbox)
                    checkbox.setChecked(False)
        self.player2_clicked_checkbox = clicked_checkbox

    def begin_game(self):
        self.ui.matchOutcomeLabel.clear()
        self.ui.player1Score.setText("0")
        self.ui.player2Score.setText("0")
        number_of_rounds = self.ui.roundsSpinBox.value()
        player_1, player_2 = self.player_choice()
        for round_number in range(number_of_rounds):
            self.game = Quantum_Tic_Tac_Toe()
            if not round_number % 2:
                player_1.set_mark("x")
                player_2.set_mark("o")
                x_score, o_score = self.game.one_round(player_1, player_2)
                player_1.add_score(x_score)
                player_2.add_score(o_score)
            else:
                player_1.set_mark("o")
                player_2.set_mark("x")
                x_score, o_score = self.game.one_round(player_2, player_1)
                player_1.add_score(o_score)
                player_2.add_score(x_score)
            self.ui.matchOutcomeLabel.setText(f"X: {x_score}, O: {o_score}")
            self.ui.player1Score.setText(f'{player_1.score()}')
            self.ui.player2Score.setText(f'{player_2.score()}')
            self.display_state_of_game()
        if player_1.score() > player_2.score():
            self.ui.matchOutcomeLabel.setText("Player 1 won")
        elif player_1.score() < player_2.score():
            self.ui.matchOutcomeLabel.setText("Player 2 won")
        else:
            self.ui.matchOutcomeLabel.setText("Tie")

    def player_choice(self):
        if self.ui.player1Easy.isChecked():
            player_1 = Computer_Easy("x")
        elif self.ui.player1Hard.isChecked():
            player_1 = Computer_Hard("x")
        else:
            player_1 = Human_Player("x", self)
        if self.ui.player2Easy.isChecked():
            player_2 = Computer_Easy("o")
        elif self.ui.player2Hard.isChecked():
            player_2 = Computer_Hard("o")
        else:
            player_2 = Human_Player("o", self)
        return player_1, player_2

    def clear_squares(self):
        squares = self.game.squares()
        for square in squares:
            eval(f"self.ui.big_label{square}.clear()")
            for i in range(1, 10):
                eval(f"self.ui.label{square}_{i}.clear()")

    def display_state_of_game(self):
        self.clear_squares()
        squares = self.game.squares()
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

    def entanglement_input(self):
        event = EntanglementChoiceLoop(self)
        event.exec_()
        return self.player_entanglement_choice

    def collapse_input(self, added_mark):
        event = CollapseChoiceLoop(self, added_mark)
        event.exec_()
        return self.player_collapse_choice

    def display_rules(self):
        self.ui.rules = RulesWindow()
        self.ui.rules.show()

    def find_mark_placement(self, mark):
        squares_to_search = mark.entanglement()
        squares = self.game.squares()
        placement = {}
        for square in squares_to_search:
            placement[square] = squares[square].index(mark)
        return placement


class EntanglementChoiceLoop(QEventLoop):
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.mainwindow = ui
        self.mainwindow.player_entanglement_choice = []
        free_squares = self.mainwindow.game.available_squares()
        for i in free_squares:
            eval(f"self.mainwindow.ui.button{i}.clicked.connect" +
                 f"(self.append{i})")
            eval(f"self.mainwindow.ui.button{i}.clicked.connect(self.cleanup)")

    def cleanup(self):
        entl_len = len(self.mainwindow.player_entanglement_choice)
        if entl_len == 2:
            entl1 = self.mainwindow.player_entanglement_choice[0]
            entl2 = self.mainwindow.player_entanglement_choice[1]
            if entl1 == entl2:
                self.mainwindow.player_entanglement_choice = []
            else:
                self.quit()

    for i in range(1, 10):
        exec(f"def append{i}(self):  self.mainwindow."
             + f"player_entanglement_choice.append({i})")


class CollapseChoiceLoop(QEventLoop):
    def __init__(self, ui, added_mark, parent=None):
        super().__init__(parent)
        self.mainwindow = ui
        self.mainwindow.player_collapse_choice = 0
        sign = added_mark.mark()
        move_number = added_mark.move_number()
        mark_placement = self.mainwindow.find_mark_placement(added_mark)
        for square in added_mark.entanglement():
            pixmap = QPixmap(f"mark_pics/red_small_{sign}_{move_number}")
            eval(f"self.mainwindow.ui.label{square}_{mark_placement[square]}" +
                 ".setPixmap(pixmap)")
            eval(f"self.mainwindow.ui.button{square}.clicked.connect" +
                 f"(self.choose{square})")
            eval(f"self.mainwindow.ui.button{square}.clicked" +
                 ".connect(self.cleanup)")

    def cleanup(self):
        self.quit()

    for i in range(1, 10):
        exec(f"def choose{i}(self):  self.mainwindow.player_collapse_choice" +
             f"= {i}")


class Human_Player(Player):
    def __init__(self, mark, ui, score=0):
        super().__init__(mark, score)
        self._ui = ui

    def mark_choice(self, game):
        self._ui.display_state_of_game()
        return self._ui.entanglement_input()

    def collapse_choice(self, game, added_mark):
        self._ui.display_state_of_game()
        return self._ui.collapse_input(added_mark)


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


if __name__ == "__main__":
    guiMain(sys.argv)
