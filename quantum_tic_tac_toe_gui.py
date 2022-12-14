from PySide2.QtWidgets import QMainWindow, QApplication, QWidget
from PySide2.QtGui import QPixmap, QFont, QCursor
from PySide2.QtCore import QEventLoop, Qt
from PySide2.QtTest import QTest
from ui_quantum_tic_tac_toe import Ui_MainWindow
from ui_rules_window import Ui_rulesWidget

from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe
from player_class import (
    Player,
    Computer_Easy,
    Computer_Hard,
    collapse_data_check,
    mark_data_check
)
from mark_class import Mark
from datetime import datetime as datetime_, timedelta


@staticmethod
def qWait(t):
    """
    Makes application wait for t miliseconds while not freezing its thread
    unlike time.sleep.
    """
    end = datetime_.now() + timedelta(milliseconds=t)
    while datetime_.now() < end:
        QApplication.processEvents()


QTest.qWait = qWait


class QuantumTicTacToeWindow(QMainWindow):
    """
    GUI window for Quantum_Tic_Tac_Toe game.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.game = Quantum_Tic_Tac_Toe()
        """
        We use
        """
        self.player1_clicked_checkbox = []
        self.player2_clicked_checkbox = []
        self.player_entanglement_choice = []
        self.player_collapse_choice = 0
        self.big_label_list = []
        self.small_label_list = []
        """
        Below we create list of labels that are on the board, labeli_j
        means small label in i-th button on j-th position. with 1-3 being
        left to right upper squares, 4-6 left to right middle squares and
        7-9 being left to right bottom squares, big_labeli means big label
        on i-th positoin on the board.
        """
        for i in range(1, 10):
            self.big_label_list.append(eval(f"self.ui.big_label{i}"))
        for i in range(1, 10):
            small_labels_square = []
            for j in range(1, 10):
                small_labels_square.append(eval(f"self.ui.label{i}_{j}"))
            self.small_label_list.append(small_labels_square)
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
        """
        This function makes sure that player1 checkboxes are checked
        one at a time.
        """
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
            elif checkbox in clicked_checkbox:
                checkbox.setChecked(True)
        self.player1_clicked_checkbox = clicked_checkbox

    def clear_player2checkboxes(self):
        """
        This function makes sure that player2 checkboxes are checked
        one at a time.
        """
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
            elif checkbox in clicked_checkbox:
                checkbox.setChecked(True)
        self.player2_clicked_checkbox = clicked_checkbox

    def begin_game(self):
        """
        This function begins playing quantum tic tac toe game.
        """
        self.ui.startButton.clicked.disconnect()
        cursor = QCursor(Qt.ForbiddenCursor)
        self.ui.startButton.setCursor(cursor)
        self.ui.matchOutcomeLabel.clear()
        self.ui.player1Score.setText("0")
        self.ui.player2Score.setText("0")
        number_of_rounds = self.ui.roundsSpinBox.value()
        player_1, player_2 = self.player_choice()
        x_pixmap = QPixmap("mark_pics/x_label_green")
        o_pixmap = QPixmap("mark_pics/o_label_green")
        for round_number in range(number_of_rounds):
            self.game = Quantum_Tic_Tac_Toe()
            self.player_entanglement_choice = []
            self.player_collapse_choice = 0
            if not round_number % 2:
                self.ui.player1MarkLabel.setPixmap(x_pixmap)
                self.ui.player2MarkLabel.setPixmap(o_pixmap)
                player_1.set_mark("x")
                player_2.set_mark("o")
                x_score, o_score = self.game.one_round(player_1, player_2)
                player_1.add_score(x_score)
                player_2.add_score(o_score)
            else:
                self.ui.player1MarkLabel.setPixmap(o_pixmap)
                self.ui.player2MarkLabel.setPixmap(x_pixmap)
                player_1.set_mark("o")
                player_2.set_mark("x")
                x_score, o_score = self.game.one_round(player_2, player_1)
                player_1.add_score(o_score)
                player_2.add_score(x_score)
            self.display_state_of_game()
            self.round_end_event()
            self.ui.player1Score.setText(f'{player_1.score()}')
            self.ui.player2Score.setText(f'{player_2.score()}')
        if player_1.score() > player_2.score():
            self.ui.matchOutcomeLabel.setText("Player 1 won")
        elif player_1.score() < player_2.score():
            self.ui.matchOutcomeLabel.setText("Player 2 won")
        else:
            self.ui.matchOutcomeLabel.setText("Tie")
        cursor = QCursor(Qt.ArrowCursor)
        self.ui.startButton.setCursor(cursor)
        self.ui.startButton.clicked.connect(self.begin_game)

    def player_choice(self):
        """
        This function detects what players are chosen and returns them.
        """
        if self.ui.player1Easy.isChecked():
            player_1 = Gui_Computer_Easy("x", self)
        elif self.ui.player1Hard.isChecked():
            player_1 = Gui_Computer_Hard("x", self)
        else:
            player_1 = Human_Player("x", self)
        if self.ui.player2Easy.isChecked():
            player_2 = Gui_Computer_Easy("o", self)
        elif self.ui.player2Hard.isChecked():
            player_2 = Gui_Computer_Hard("o", self)
        else:
            player_2 = Human_Player("o", self)
        return player_1, player_2

    def clear_squares(self):
        """
        This function clears all the labels on board.
        """
        for big_label in self.big_label_list:
            big_label.clear()
        for square in self.small_label_list:
            for label in square:
                label.clear()

    def display_state_of_game(self):
        """
        This function displays state of quantum tic tac toe game
        on board.
        """
        self.clear_squares()
        squares = self.game.squares()
        for square in squares:
            if squares[square][0]:
                collapsed_mark = squares[square][1]
                mark = collapsed_mark.mark()
                move_number = collapsed_mark.move_number()
                pixmap = QPixmap(f"mark_pics/big_{mark}_{move_number}")
                self.big_label_list[square-1].setPixmap(pixmap)
            else:
                for index, mark in enumerate(squares[square][1:], 1):
                    sign = mark.mark()
                    move_number = mark.move_number()
                    pixmap = QPixmap(f"mark_pics/small_{sign}_{move_number}")
                    self.small_label_list[square-1][index-1].setPixmap(pixmap)

    def round_end_event(self):
        """
        This function shows outcome of round and makes player
        click middle square to continue
        """
        event = RoundEndEventLoop(self)
        event.exec_()

    def display_rules(self):
        """
        This function displays window with wikipedia page of quantum
        tic tac toe.
        """
        self.ui.rules = RulesWindow()
        self.ui.rules.show()

    def find_mark_placement(self, mark):
        """
        This function finds placement of a mark on game board. It returns
        dictionary with keys being squares of mark and values under keys
        being indexes of mark in those squares. See Quantum_Tic_Tac_Toe
        squares.
        """
        if not isinstance(mark, Mark):
            raise TypeError("mark must be a Mark class instance")
        squares_to_search = mark.entanglement()
        squares = self.game.squares()
        placement = {}
        for square in squares_to_search:
            placement[square] = squares[square].index(mark)
        return placement

    def highlight_added_mark(self, added_mark):
        """
        This function changes labels of added mark to red to show that
        it started a cycle.
        """
        sign = added_mark.mark()
        move_number = added_mark.move_number()
        mark_placement = self.find_mark_placement(added_mark)
        for square in added_mark.entanglement():
            pixmap = QPixmap(f"mark_pics/red_small_{sign}_{move_number}")
            eval(f"self.ui.label{square}_{mark_placement[square]}" +
                 ".setPixmap(pixmap)")


class RoundEndEventLoop(QEventLoop):
    """
    This is event loop that we use on end of quantum tic tac toe round.
    """
    def __init__(self, ui, parent=None):
        super().__init__(parent)
        self.mainwindow = ui
        win_data = self.mainwindow.game.win_detection()
        if not win_data:
            self.quit()
        x_score = win_data['x']
        o_score = win_data['o']
        message = f"X: {x_score} O: {o_score}, to continue click"
        message += " the middle square of the board"
        font = QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.mainwindow.ui.matchOutcomeLabel.setFont(font)
        self.mainwindow.ui.matchOutcomeLabel.setText(message)
        self.mainwindow.ui.button5.clicked.connect(self.cleanup)

    def cleanup(self):
        font = QFont()
        font.setPointSize(23)
        font.setBold(True)
        font.setWeight(75)
        self.mainwindow.ui.matchOutcomeLabel.setFont(font)
        self.quit()


class EntanglementChoiceLoop(QEventLoop):
    """
    This is event loop that we use when in quantum tic tac toe game
    it is normal move of human player.
    """
    def __init__(self, ui, mark, parent=None):
        super().__init__(parent)
        self.mainwindow = ui
        self.mark = mark
        self.entanglement_choice = []
        free_squares = self.mainwindow.game.available_squares()
        for square in free_squares:
            eval(f"self.mainwindow.ui.button{square}.clicked.connect" +
                 f"(self.append{square})")
            eval(f"self.mainwindow.ui.button{square}.clicked.connect" +
                 "(self.cleanup)")

    def cleanup(self):
        """
        This cleanup function highlights place we want to choose on first
        press of a button and unhighlights it when we click it again,
        after proper squares are chosen it quits event loop
        """
        entl_len = len(self.entanglement_choice)
        if entl_len == 1:
            highlight = self.entanglement_choice[0]
            highlight -= 1
            if self.mark == "x":
                pixmap = QPixmap("mark_pics/choice_x")
            if self.mark == "o":
                pixmap = QPixmap("mark_pics/choice_o")
            self.mainwindow.big_label_list[highlight].setPixmap(pixmap)
        if entl_len == 2:
            entl1 = self.entanglement_choice[0]
            entl2 = self.entanglement_choice[1]
            self.mainwindow.big_label_list[entl1-1].clear()
            if entl1 == entl2:
                self.entanglement_choice = []
            else:
                self.mainwindow.player_entanglement_choice = [entl1, entl2]
                self.quit()
        if entl_len > 2:
            self.entanglement_choice.clear()

    for i in range(1, 10):
        exec(f"def append{i}(self):  self.entanglement_choice.append({i})")


class CollapseChoiceLoop(QEventLoop):
    """
    This is event loop that we use when there is cycle and human player needs
    to choose initial collapse square.
    """
    def __init__(self, ui, added_mark, parent=None):
        super().__init__(parent)
        self.mainwindow = ui
        self.mainwindow.player_collapse_choice = 0
        for square in added_mark.entanglement():
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
    """
    This is human player linked to GUI.
    """
    def __init__(self, mark, ui, score=0):
        super().__init__(mark, score)
        self._ui = ui

    def mark_choice(self, game):
        self._ui.display_state_of_game()
        message = self.mark().upper()
        message += " moves"
        self._ui.ui.matchOutcomeLabel.setText(message)
        return self._mark_decision(self.mark())

    def collapse_choice(self, game):
        added_mark = game.last_placed_mark()
        self._ui.display_state_of_game()
        self._ui.highlight_added_mark(added_mark)
        message = "Cycle!!! "
        message += self.mark().upper()
        message += " chooses"
        self._ui.ui.matchOutcomeLabel.setText(message)
        return self._collapse_decision(added_mark)

    def _mark_decision(self, mark):
        mark_data_check(self._ui.game)
        event = EntanglementChoiceLoop(self._ui, mark)
        event.exec_()
        return self._ui.player_entanglement_choice

    def _collapse_decision(self, added_mark):
        if not isinstance(added_mark, Mark):
            raise TypeError("added_mark must be a Mark class instance")
        collapse_data_check(self._ui.game)
        event = CollapseChoiceLoop(self._ui, added_mark)
        event.exec_()
        return self._ui.player_collapse_choice


class Gui_Computer_Easy(Computer_Easy):
    """
    This is easy computer player linked to GUI.
    """
    def __init__(self, mark, ui, score=0, simulation=False):
        super().__init__(mark, score)
        self._ui = ui

    def mark_choice(self, game):
        self._ui.display_state_of_game()
        message = self.mark().upper()
        message += " moves"
        self._ui.ui.matchOutcomeLabel.setText(message)
        QTest.qWait(500)
        chosen_squares = self._mark_decision(game)
        return chosen_squares

    def collapse_choice(self, game):
        added_mark = game.last_placed_mark()
        self._ui.display_state_of_game()
        self._ui.highlight_added_mark(added_mark)
        message = "Cycle!!! "
        message += self.mark().upper()
        message += " chooses"
        self._ui.ui.matchOutcomeLabel.setText(message)
        QTest.qWait(500)
        chosen_square = self._collapse_decision(game, added_mark)
        return chosen_square


class Gui_Computer_Hard(Computer_Hard):
    """
    This is hard computer player linked to GUI.
    """
    def __init__(self, mark, ui, score=0, simulation=False):
        super().__init__(mark, score)
        self._ui = ui

    def mark_choice(self, game):

        self._ui.display_state_of_game()
        message = self.mark().upper()
        message += " moves"
        self._ui.ui.matchOutcomeLabel.setText(message)
        QTest.qWait(500)
        chosen_squares = self._mark_decision(game)
        return chosen_squares

    def collapse_choice(self, game):
        added_mark = game.last_placed_mark()
        self._ui.display_state_of_game()
        self._ui.highlight_added_mark(added_mark)
        message = "Cycle!!! "
        message += self.mark().upper()
        message += " chooses"
        self._ui.ui.matchOutcomeLabel.setText(message)
        QTest.qWait(500)
        chosen_square = self._collapse_decision(game, added_mark)
        return chosen_square


class RulesWindow(QWidget):
    """
    This is rules window.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_rulesWidget()
        self.ui.setupUi(self)
