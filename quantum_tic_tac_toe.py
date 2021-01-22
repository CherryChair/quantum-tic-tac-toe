from quantum_tic_tac_toe_gui import QuantumTicTacToeWindow
from PySide2.QtWidgets import QApplication
import sys


def guiMain(args):
    app = QApplication(args)
    window = QuantumTicTacToeWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    guiMain(sys.argv)
