class NotProperEntanglement(Exception):
    pass


class EntanglementValueError(ValueError):
    pass


class MoveNumberOutOfRange(ValueError):
    pass


def proper_entanglement_check(entanglement):
    if not isinstance(entanglement, list):
        raise TypeError("Entanglement must be a list")
    if not len(entanglement) == 2:
        message = "Entanglement must be contain only 2 elements"
        raise NotProperEntanglement(message)
    if entanglement[0] not in range(1, 10):
        message = "Entanglement must contain only numbers from 1-9"
        raise EntanglementValueError(message)
    if entanglement[1] not in range(1, 10):
        message = "Entanglement must contain only numbers from 1-9"
        raise EntanglementValueError(message)


def proper_mark_check(mark):
    if not isinstance(mark, str):
        raise TypeError("mark must be a string")
    mark.casefold()
    mark.strip()
    if mark not in ["x", "o"]:
        raise ValueError("mark must be either 'x' or 'o'")
    return mark


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
        proper_entanglement_check(entanglement)
        if not isinstance(move_number, int):
            raise TypeError("Move number must be an integer")
        if move_number not in range(1, 10):
            message = "Move number must be a digit form 1 to 9"
            raise MoveNumberOutOfRange(message)
        if not isinstance(collapsed, bool):
            raise TypeError("collapsed must be of boolean")
        mark = proper_mark_check(mark)
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
