class Mark():
    def __init__(self, mark, entanglement, move_number, collapsed=False):
        """
        Mark has four attributes:

        mark - which is equal to "x" or "o".

        entanglement - represents squares on which mark was initialy placed.

        move_number - represents round of Quantum Tic Tac Toe on which Mark was
        placed.

        collapsed - determines whether mark is measured defaultly equals False.
        """
        self._mark = mark
        self._entanglement = entanglement
        self._move_number = move_number
        self._collapsed = collapsed

    def mark(self):
        """
        Returns mark which is either "x" or "o"
        """
        return self._mark

    def move_number(self):
        """
        Returns move number associated with mark.
        """
        return self._move_number

    def set_entanglement(self, entanglement):
        self._entanglement = entanglement

    def entanglement(self):
        """
        Returns list of two squares in which mark is or originally was
        placed.
        """
        return self._entanglement

    def collapse(self):
        """
        Collapses mark.
        """
        self._collapsed = True

    def collapsed(self):
        """
        If mark is collapsed returns True if it isn't returns False.
        """
        return self._collapsed

    def __str__(self):
        """
        Returns string with visual representation of a mark in format
        *mark*_*move number*
        """
        return f'{self.mark()}_{self.move_number()}'
