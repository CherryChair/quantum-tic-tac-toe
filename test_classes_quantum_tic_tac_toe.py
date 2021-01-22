from quantum_tic_tac_toe_class import (
    Quantum_Tic_Tac_Toe,
    UnresolvedCycleInGame,
    NoUnresolvedCycleInGame,
    InvalidMoveError,
    InvalidMoveNumber,
    InvalidStartingMoveError,
    InvalidStartingSquare,
    IdenticalPlayerMarks,
    SquareNumberOutOfRange,
    SamePlayerError,
    mark_detection,
    SquareOccupied
)
from mark_class import Mark, EntanglementValueError, NotProperEntanglement
from mark_class import MoveNumberOutOfRange
from player_class import Player, Computer_Easy, Computer_Hard, WrongPlayerTurn
from quantum_tic_tac_toe_gui import (
    QuantumTicTacToeWindow,
    Gui_Computer_Easy,
    Gui_Computer_Hard,
    Human_Player
)
import pytest


"""
Mark tests
"""


def test_mark_invalid_entanglement():
    with pytest.raises(TypeError):
        Mark(1, [1, 2], 1)
    with pytest.raises(TypeError):
        Mark("x", 1, 1)
    with pytest.raises(TypeError):
        Mark("x", [1, 2], "a")
    with pytest.raises(TypeError):
        Mark("x", [1, 2], "a", [])
    with pytest.raises(EntanglementValueError):
        Mark("x", [100, 2], 1)
    with pytest.raises(EntanglementValueError):
        Mark("x", [1, -1], 1)
    with pytest.raises(NotProperEntanglement):
        Mark("x", [1, 2, 3], 2)
    with pytest.raises(NotProperEntanglement):
        Mark("x", [], 2)
    with pytest.raises(MoveNumberOutOfRange):
        Mark("x", [1, 2], 120)
    with pytest.raises(MoveNumberOutOfRange):
        Mark("x", [1, 2], -12)
    with pytest.raises(ValueError):
        Mark("a", [1, 2], 4)
    o = Mark("    O   ", [1, 2], 3)
    x = Mark("    X  ", [3, 4], 5)
    assert o.mark() == "o"
    assert x.mark() == "x"


"""
Quantum_Tic_Tac_Toe tests
"""


def test_set_paths():
    q = Quantum_Tic_Tac_Toe()
    q._set_paths([{1, 2, 3}, {6, 7, 8}])
    assert q.paths() == [{1, 2, 3}, {6, 7, 8}]


def test_paths_update_initial_path():
    q = Quantum_Tic_Tac_Toe()
    new_path = q.paths_update({4, 5})
    assert new_path == {4, 5}
    assert not q._unresolved_cycle
    assert q.paths() == [{4, 5}]


def test_paths_update():
    q = Quantum_Tic_Tac_Toe()
    q._set_paths([{1, 2, 3}, {6, 7, 8}])
    new_path = q.paths_update({4, 5})
    assert new_path == {4, 5}
    assert not q._unresolved_cycle
    assert q.paths() == [{1, 2, 3}, {6, 7, 8}, {4, 5}]


def test_paths_update_joint_paths():
    q = Quantum_Tic_Tac_Toe()
    q._set_paths([{1, 2, 3}, {6, 7, 8}])
    new_path = q.paths_update({2, 6})
    assert new_path == {1, 2, 3, 6, 7, 8}
    assert not q._unresolved_cycle
    assert q.paths() == [{1, 2, 3, 6, 7, 8}]


def test_paths_update_joint_paths_with_additional():
    q = Quantum_Tic_Tac_Toe()
    q._set_paths([{1, 2}, {6, 8}, {7, 9}])
    new_path = q.paths_update({2, 6})
    assert new_path == {1, 2, 6, 8}
    assert not q._unresolved_cycle
    assert q.paths() == [{1, 2, 6, 8}, {7, 9}]


def test_paths_update_cycle():
    q = Quantum_Tic_Tac_Toe()
    q._set_paths([{1, 2, 3}, {6, 7, 8}])
    new_path = q.paths_update({2, 3})
    assert new_path == {1, 2, 3}
    assert q._unresolved_cycle
    assert q.paths() == [{1, 2, 3}, {6, 7, 8}]


def test_paths_update_path_extension():
    q = Quantum_Tic_Tac_Toe()
    q._set_paths([{1, 2, 3}, {6, 7, 8}])
    new_path = q.paths_update({3, 5})
    assert new_path == {1, 2, 3, 5}
    assert not q._unresolved_cycle
    assert q.paths() == [{1, 2, 3, 5}, {6, 7, 8}]


def test_add_entangled_mark():
    squares = {i: [False] for i in range(1, 10)}
    mark = Mark("x", [1, 2], 1)
    squares[1].append(mark)
    squares[2].append(mark)
    paths = [{1, 2}]
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(mark)
    assert q.squares() == squares
    assert q.paths() == paths
    assert not q.cycle()


def test_add_entangled_mark_cycle():
    squares = {i: [False] for i in range(1, 10)}
    x_1 = Mark("x", [1, 2], 1)
    o_2 = Mark("o", [1, 2], 2)
    squares[1].append(x_1)
    squares[2].append(x_1)
    squares[1].append(o_2)
    squares[2].append(o_2)
    paths = [{1, 2}]
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    assert q.squares() == squares
    assert q.paths() == paths
    assert q.cycle()


def test_add_entangled_mark_wrong_starting_mark():
    mark = Mark("o", [1, 2], 1)
    q = Quantum_Tic_Tac_Toe()
    with pytest.raises(InvalidStartingMoveError):
        q.add_entangled_mark(mark)


def test_add_entangled_mark_wrong_type_mark():
    q = Quantum_Tic_Tac_Toe()
    with pytest.raises(TypeError):
        q.add_entangled_mark("x")


def test_add_entangled_mark_wrong_next_mark():
    x_1 = Mark("x", [1, 2], 1)
    o_2 = Mark("x", [1, 2], 2)
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(x_1)
    with pytest.raises(InvalidMoveError):
        q.add_entangled_mark(o_2)


def test_add_entangled_mark_square_occupied():
    x_1 = Mark("x", [1, 2], 1)
    o_2 = Mark("o", [1, 2], 2)
    x_3 = Mark("x", [1, 2], 3)
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.collapse_squares(o_2, 1)
    q._unresolved_cycle = False
    with pytest.raises(SquareOccupied):
        q.add_entangled_mark(x_3)


def test_add_entangled_mark_wrong_next_mark_move_number():
    x_1 = Mark("x", [1, 2], 1)
    o_2 = Mark("o", [1, 2], 3)
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(x_1)
    with pytest.raises(InvalidMoveNumber):
        q.add_entangled_mark(o_2)


def test_add_entangled_mark_unresolved_cycle():
    x_1 = Mark("x", [1, 2], 1)
    o_2 = Mark("o", [1, 2], 2)
    x_3 = Mark("x", [4, 6], 3)
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    with pytest.raises(UnresolvedCycleInGame):
        q.add_entangled_mark(x_3)


def test_collapse_squares():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [2, 3], 2)
    x_3 = Mark('x', [6, 7], 3)
    o_4 = Mark('o', [7, 8], 4)
    x_5 = Mark('x', [2, 3], 5)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    q.add_entangled_mark(o_4)
    q.add_entangled_mark(x_5)
    q.collapse_squares(x_5, 3)
    a = q.squares()
    assert a[3] == [True, x_5]
    assert a[2] == [True, o_2]
    assert a[1] == [True, x_1]


def test_collapse_squares_2():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    x_3 = Mark('x', [1, 4], 3)
    o_4 = Mark('o', [1, 5], 4)
    x_5 = Mark('x', [1, 6], 5)
    o_6 = Mark('o', [1, 7], 6)
    x_7 = Mark('x', [1, 8], 7)
    o_8 = Mark('o', [1, 9], 8)
    x_9 = Mark('x', [4, 6], 9)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    q.add_entangled_mark(o_4)
    q.add_entangled_mark(x_5)
    q.add_entangled_mark(o_6)
    q.add_entangled_mark(x_7)
    q.add_entangled_mark(o_8)
    q.add_entangled_mark(x_9)
    q.collapse_squares(x_9, 4)
    a = q.squares()
    assert a[4] == [True, x_9]
    assert a[1] == [True, x_3]
    assert a[2] == [True, x_1]
    assert a[3] == [True, o_2]
    assert a[5] == [True, o_4]
    assert a[6] == [True, x_5]
    assert a[7] == [True, o_6]
    assert a[8] == [True, x_7]
    assert a[9] == [True, o_8]


def test_collapse_squares_3():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [2, 3], 2)
    x_3 = Mark('x', [6, 7], 3)
    o_4 = Mark('o', [7, 8], 4)
    x_5 = Mark('x', [2, 3], 5)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    q.add_entangled_mark(o_4)
    q.add_entangled_mark(x_5)
    q.collapse_squares(x_5, 3)
    a = q.squares()
    assert a[3] == [True, x_5]
    assert a[2] == [True, o_2]
    assert a[1] == [True, x_1]


def test_collapse_squares_no_unresolved_cycle():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [2, 3], 2)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    with pytest.raises(NoUnresolvedCycleInGame):
        q.collapse_squares(o_2, 3)


def test_collapse_squares_wrong_square():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [2, 3], 2)
    x_3 = Mark('x', [3, 1], 3)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    with pytest.raises(InvalidStartingSquare):
        q.collapse_squares(x_3, 2)


def test_mark_detection():
    assert mark_detection(3) == 'x'
    assert mark_detection(4) == 'o'


def test_win_detection():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    x_3 = Mark('x', [1, 4], 3)
    o_4 = Mark('o', [1, 5], 4)
    x_5 = Mark('x', [1, 6], 5)
    o_6 = Mark('o', [1, 7], 6)
    x_7 = Mark('x', [1, 8], 7)
    o_8 = Mark('o', [1, 9], 8)
    x_9 = Mark('x', [4, 6], 9)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    q.add_entangled_mark(o_4)
    q.add_entangled_mark(x_5)
    q.add_entangled_mark(o_6)
    q.add_entangled_mark(x_7)
    q.add_entangled_mark(o_8)
    q.add_entangled_mark(x_9)
    q.collapse_squares(x_9, 4)
    assert q.win_detection() == {'x': 0, 'o': 1}


def test_win_detection_false():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [2, 3], 2)
    x_3 = Mark('x', [6, 7], 3)
    o_4 = Mark('o', [7, 8], 4)
    x_5 = Mark('x', [2, 3], 5)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    q.add_entangled_mark(o_4)
    q.add_entangled_mark(x_5)
    q.collapse_squares(x_5, 3)
    assert not q.win_detection()


def test_str():
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [2, 3], 2)
    x_3 = Mark('x', [6, 7], 3)
    o_4 = Mark('o', [7, 8], 4)
    x_5 = Mark('x', [2, 3], 5)
    assert str(x_1) == 'x_1'
    assert str(o_2) == 'o_2'
    assert str(x_3) == 'x_3'
    assert str(o_4) == 'o_4'
    assert str(x_5) == 'x_5'


def test_visual_square_interior():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    a = q.visual_square_interior(1)
    assert a == '1'+' '*10+'\n'+'x_1 o_2'+' '*4+'\n'+(' '*11+'\n')*5


def test_visual_square_interior_two_rows():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    x_3 = Mark('x', [1, 7], 3)
    o_4 = Mark('o', [1, 8], 4)
    x_5 = Mark('x', [1, 3], 5)
    for i in [x_1, o_2, x_3, o_4, x_5]:
        q.add_entangled_mark(i)
    a = q.visual_square_interior(1)
    assert a == '1'+' '*10+'\n'+'x_1 o_2 x_3'+'\n'+' '*11+'\n'+'o_4 x_5' + \
                ' '*4+'\n'+(' '*11+'\n')*3


def test_visual_square_interior_wrong_type_square():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    with pytest.raises(TypeError):
        q.visual_square_interior([0])


def test_visual_square_interior_wrong_square():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    with pytest.raises(SquareNumberOutOfRange):
        q.visual_square_interior(0)


def test_str_Quantum():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 3], 2)
    x_3 = Mark('x', [1, 4], 3)
    o_4 = Mark('o', [1, 5], 4)
    x_5 = Mark('x', [1, 6], 5)
    o_6 = Mark('o', [1, 7], 6)
    x_7 = Mark('x', [1, 8], 7)
    o_8 = Mark('o', [1, 9], 8)
    x_9 = Mark('x', [4, 6], 9)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    q.add_entangled_mark(x_3)
    q.add_entangled_mark(o_4)
    q.add_entangled_mark(x_5)
    q.add_entangled_mark(o_6)
    q.add_entangled_mark(x_7)
    q.add_entangled_mark(o_8)
    q.add_entangled_mark(x_9)
    a = '1          |2          |3          \n'
    a += 'x_1 o_2 x_3|x_1        |o_2        \n'
    a += '           |           |           \n'
    a += 'o_4 x_5 o_6|           |           \n'
    a += '           |           |           \n'
    a += 'x_7 o_8    |           |           \n'
    a += '___________|___________|___________\n'
    a += '4          |5          |6          \n'
    a += 'x_3 x_9    |o_4        |x_5 x_9    \n'
    a += '           |           |           \n'
    a += '           |           |           \n'
    a += '           |           |           \n'
    a += '           |           |           \n'
    a += '___________|___________|___________\n'
    a += '7          |8          |9          \n'
    a += 'o_6        |x_7        |o_8        \n'
    a += '           |           |           \n'
    a += '           |           |           \n'
    a += '           |           |           \n'
    a += '           |           |           \n'
    assert str(q) == a


def test_both_cycle_resolution_options():
    q = Quantum_Tic_Tac_Toe()
    x_1 = Mark('x', [1, 2], 1)
    o_2 = Mark('o', [1, 2], 2)
    q.add_entangled_mark(x_1)
    q.add_entangled_mark(o_2)
    a, b = q.both_cycle_resolution_options()
    squares_1 = a.squares()
    squares_2 = b.squares()
    squares_3 = q.squares()
    for i in [1, 2]:
        assert squares_1[i][0] is True
        assert squares_2[i][0] is True
        assert squares_3[i][0] is False
        assert len(squares_1[i]) == 2
        assert len(squares_2[i]) == 2
        assert len(squares_3[i]) == 3
        assert squares_1[i][1].entanglement() == [1, 2]
        assert squares_2[i][1].entanglement() == [1, 2]
        assert squares_3[i][1].entanglement() == [1, 2]
        assert squares_1[i][1].collapsed() is True
        assert squares_2[i][1].collapsed() is True
        assert squares_3[i][1].collapsed() is False
    assert squares_1[1][1].mark() == 'o'
    assert squares_1[2][1].mark() == 'x'
    assert squares_2[1][1].mark() == 'x'
    assert squares_2[2][1].mark() == 'o'
    assert squares_3[1][1].mark() == 'x'
    assert squares_3[2][1].mark() == 'x'
    for i in range(3, 10):
        assert len(squares_1[i]) == 1
        assert len(squares_2[i]) == 1
        assert len(squares_3[i]) == 1
    for i in range(3, 10):
        assert squares_1[i][0] is False
        assert squares_2[i][0] is False
        assert squares_3[i][0] is False
    assert len(squares_1) == len(squares_2) == len(squares_3) == 9
    assert a.paths() == b.paths() == q.paths() == [{1, 2}]


def test_one_round():
    for i in range(1, 1000):
        q = Quantum_Tic_Tac_Toe()
        q.add_entangled_mark(Mark("x", [1, 2], 1))
        player_1 = Computer_Easy("x")
        player_2 = Computer_Hard("o")
        match_end = q.one_round(player_1, player_2)
        win = q.win_detection()
        x_score, o_score = match_end
        x_score_2 = win["x"]
        o_score_2 = win["o"]
        player_1, player_2 = player_2, player_1
        assert x_score == x_score_2
        assert o_score == o_score_2


def test_one_round_errors():
    q = Quantum_Tic_Tac_Toe()
    q.add_entangled_mark(Mark("x", [1, 2], 1))
    player_1 = Computer_Easy("x")
    player_2 = Computer_Hard("x")
    with pytest.raises(IdenticalPlayerMarks):
        q.one_round(player_1, player_2)
    with pytest.raises(SamePlayerError):
        player_2 = player_1
        q.one_round(player_1, player_1)
    with pytest.raises(TypeError):
        q.one_round(player_1, 1)
    with pytest.raises(TypeError):
        q.one_round(1, player_2)


"""
Player tests
"""


def test_player_bad_score():
    with pytest.raises(TypeError):
        Player("x", [1])


def test_player_wrong_mark1():
    with pytest.raises(TypeError):
        Player(1)


def test_player_wrong_mark2():
    with pytest.raises(ValueError):
        Player("a")


def test_player_mark_upper_whitespace():
    a = Player(" X    ")
    b = Player("  O  ")
    assert a.mark() == "x"
    assert b.mark() == "o"


def test_computer_player_hard_collapse_choice():
    for i in range(1, 100):
        q = Quantum_Tic_Tac_Toe()
        player = Computer_Hard("o")
        q.add_entangled_mark(Mark("x", [1, 2], 1))
        q.add_entangled_mark(Mark("o", [2, 5], 2))
        q.add_entangled_mark(Mark("x", [5, 1], 3))
        assert player.collapse_choice(q) == 1
        assert q.squares()[5][1].mark() == "o"
    for i in range(1, 100):
        q = Quantum_Tic_Tac_Toe()
        player = Computer_Hard("o")
        q.add_entangled_mark(Mark("x", [1, 5], 1))
        q.add_entangled_mark(Mark("o", [1, 2], 2))
        q.add_entangled_mark(Mark("x", [5, 9], 3))
        q.add_entangled_mark(Mark("o", [2, 6], 4))
        q.add_entangled_mark(Mark("x", [1, 2], 5))
        assert player.collapse_choice(q) == 2
    for i in range(1, 100):
        q = Quantum_Tic_Tac_Toe()
        player = Computer_Hard("x")
        q.add_entangled_mark(Mark("x", [1, 5], 1))
        q.add_entangled_mark(Mark("o", [1, 2], 2))
        q.add_entangled_mark(Mark("x", [5, 9], 3))
        q.add_entangled_mark(Mark("o", [2, 6], 4))
        assert 5 in player.mark_choice(q)
    for i in range(1, 100):
        q = Quantum_Tic_Tac_Toe()
        player = Computer_Hard("o")
        q.add_entangled_mark(Mark("x", [1, 5], 1))
        q.add_entangled_mark(Mark("o", [1, 2], 2))
        q.add_entangled_mark(Mark("x", [5, 9], 3))
        q.add_entangled_mark(Mark("o", [2, 6], 4))
        q.add_entangled_mark(Mark("x", [4, 7], 5))
        q.add_entangled_mark(Mark("o", [2, 3], 6))
        q.add_entangled_mark(Mark("x", [1, 6], 7))
        assert player.collapse_choice(q) == 6
    for i in range(1, 100):
        q = Quantum_Tic_Tac_Toe()
        player = Computer_Hard("x")
        q.add_entangled_mark(Mark("x", [1, 5], 1))
        q.add_entangled_mark(Mark("o", [1, 5], 2))
        q.collapse_squares(q.last_placed_mark(), 5)
        q._unresolved_cycle = False
        q.add_entangled_mark(Mark("x", [2, 4], 3))
        q.add_entangled_mark(Mark("o", [2, 4], 4))
        q.collapse_squares(q.last_placed_mark(), 2)
        q._unresolved_cycle = False
        q.add_entangled_mark(Mark("x", [7, 8], 5))
        q.add_entangled_mark(Mark("o", [7, 8], 6))
        assert player.collapse_choice(q) == 8


def test_wrong_player_moves():
    q = Quantum_Tic_Tac_Toe()
    player = Computer_Hard("x")
    opponent = Computer_Hard("o")
    with pytest.raises(InvalidStartingMoveError):
        opponent.mark_choice(q)
    q.add_entangled_mark(Mark("x", [1, 2], 1))
    with pytest.raises(WrongPlayerTurn):
        player.mark_choice(q)
    q.add_entangled_mark(Mark("o", [2, 5], 2))
    with pytest.raises(NoUnresolvedCycleInGame):
        player.collapse_choice(q)
    q.add_entangled_mark(Mark("x", [5, 1], 3))
    with pytest.raises(WrongPlayerTurn):
        player.collapse_choice(q)
