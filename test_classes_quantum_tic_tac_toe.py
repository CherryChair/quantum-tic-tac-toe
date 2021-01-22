from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe, mark_detection
from mark_class import Mark
import pytest


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


"""
Testy gracza
-test na dobry wybór gracza komputerowego
"""

"""
Testy gui
-test na uncheckowanie boxów
-testy na działanie wyświetlania
-test na wybór gracza
"""
