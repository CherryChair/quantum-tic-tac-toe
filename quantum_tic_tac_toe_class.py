from copy import deepcopy
from mark_class import Mark


class Quantum_Tic_Tac_Toe():
    def __init__(self, marks=None):
        """
        Quantum Tic Tac Toe has two attributes:

        squares - dictionary which represents squares of Quantum Tic Tac Toe.
        Squares are represented in form of dictionary keys numbered 1-9.
        Each square contains list of it's marks, but first entry on the
        list is always equal True or False so that we may know whether
        this square is collapsed.

        paths - stores information on which squares are connected through a
        "path" of entangled marks. paths are in form of a list of sets, sets
        symbolize mentioned "paths".
        """
        self._squares = {}
        self._paths = []
        for i in range(1, 10):
            self._squares[i] = [False]
        if marks is not None:
            for mark in marks:
                self.add_entangled_mark(mark)
                self.paths_update(mark.entanglement())

    def squares(self):
        """
        Returns dictionary symbolizing squares.
        """
        return self._squares

    def set_squares(self, squares):
        """
        Sets value of squares.
        """
        self._squares = squares

    def paths(self):
        """
        Returns list of paths.
        """
        return self._paths

    def set_paths(self, paths):
        """
        Sets paths.
        """
        self._paths = paths

    def add_mark(self, square, mark):
        """
        Adds mark to given square.
        """
        self._squares[square] += [mark]

    def add_entangled_mark(self, mark):
        """
        Adds a spooky mark to appropriate squares which are taken
        from it's entanglement.
        """
        for i in mark.entanglement():
            self.add_mark(i, mark)

    def clear_square(self, square):
        """
        Completely clears square.
        """
        self._squares[square].clear()

    def paths_update(self, entanglement):
        """
        Updates paths and returns tuple of new path and boolean value which
        determines whether this new path started a cycle.
        """
        initial_path = set(entanglement)
        new_path = initial_path
        paths = []
        potential_connection = 0
        for path in self.paths():
            if initial_path.issubset(path):
                """
                If a entanglement is susbset of some path that already exists
                we have a cycle.
                """
                new_path = path
                return new_path, True
            elif potential_connection:
                """
                If earlier in the loop we've found a path that connects with
                our entanglement it is possible that entanglement will connect
                two already existing paths.
                """
                if not initial_path.isdisjoint(path):
                    index_of_joint_path = paths.index(new_path)
                    paths[index_of_joint_path] = path.union(new_path)
                    new_path = paths[index_of_joint_path]
                    path = []
                else:
                    path = [path]
            elif not initial_path.isdisjoint(path):
                """
                If entanglement has common term with already existing path
                we need to broaden that path. In potential_connection we
                store information that it is possible that new entanglement
                connects two already existing paths.
                """
                new_path = path.union(initial_path)
                path = [new_path]
                potential_connection = 1
            else:
                path = [path]
            paths += path
        if new_path == initial_path:
            """
            If entanglement didn't have any common factors with already
            existing paths it is a start of a new path.
            """
            paths += [new_path]
        self.set_paths(paths)
        return new_path, False

    def collapse_squares(self, starting_mark, starting_square):
        """
        It is a recursive function that collapses marks starting
        with starting_mark. starting_square represents the choice of
        square in which we want start collapsing starting_mark. This
        fuction could be used for mark that isn't in a cycle
        """

        starting_mark.collapse()
        for mark in self.squares()[starting_square]:
            if mark is False:
                pass
            elif not mark.collapsed():
                """
                At beginning of this function we collapsed mark that started
                a cycle now we are going through all marks in the same square
                and we collapse them as soon as we enter entangled squares with
                recursion. Mark we placed started a cycle so eventually we will
                arrive at a square that doesn't have any path forward or we
                will arrive at a square that is connected with the square that
                we started with. We already set out initial mark to be
                collapsed so from this point we can only go to paths that end
                without a cycle and slowly but surely exit our recursion.
                """
                path = mark.entanglement()
                path_forward = path[0]
                if path[0] == starting_square:
                    path_forward = path[1]
                self.collapse_squares(mark, path_forward)
        self.clear_square(starting_square)
        self.add_mark(starting_square, True)
        self.add_mark(starting_square, starting_mark)

    def same_collapsed_marks(self, list_of_squares):
        """
        We use this function on triples of collapsed marks which we detected in
        win_detection function. This function determines whether all collapsed
        marks are "x" or "o".
        """
        game = self.squares()
        if all(game[square][1].mark() == 'x' for square in list_of_squares):
            return True
        if all(game[square][1].mark() == 'o' for square in list_of_squares):
            return True
        return False

    def win_detection(self):
        """
        We use this function to determine whether some player won. If a win is
        detected it returns score in form of a dictionary with keys "x" and "o"
        """
        game = self.squares()
        winning_list = []
        """
        Loops below serve a purpose of checking whether we have a winning
        combination on diagonals, colums or rows.
        """
        for i in [1, 2, 3]:
            if game[i][0] and game[i+3][0] and game[i+6][0]:
                """
                When all squares in a column are collapsed we check whether
                all collapsed marks are either "x" or "o".
                """
                if self.same_collapsed_marks([i, i+3, i+6]):
                    winning_list += [[i, i+3, i+6]]
        for i in [1, 4, 7]:
            if game[i][0] and game[i+1][0] and game[i+2][0]:
                """
                When all squares in a row are collapsed we check whether
                all collapsed marks are either "x" or "o".
                """
                if self.same_collapsed_marks([i, i+1, i+2]):
                    winning_list += [[i, i+1, i+2]]
        for i in [0, 2]:
            if game[1+i][0] and game[5][0] and game[9-i][0]:
                """
                When all squares in a diagonal are collapsed we check whether
                all collapsed marks are either "x" or "o".
                """
                if self.same_collapsed_marks([1+i, 5, 9-i]):
                    winning_list += [[1+i, 5, 9-i]]
        if bool(winning_list):
            """
            If there is a winning combination we need to determine score
            so we check which combination has lowest last move number.
            """
            list_of_last_moves = []
            for list_of_squares in winning_list:
                last_move = max(game[square][1].move_number() for square in
                                list_of_squares)
                list_of_last_moves += [last_move]
            winning_move = min(list_of_last_moves)
            for move in list_of_last_moves:
                if (winning_move - move) % 2:
                    return {player_detection(winning_move): 1,
                            player_detection(move): 0.5
                            }
            return {player_detection(winning_move): 1,
                    player_detection(winning_move-1): 0
                    }
        """
        If win wasn't detected earlier now we check whether it's a tie
        or the game isn't finished.
        """
        free_squares = self.available_squares()
        if len(free_squares) == 1 or len(free_squares) == 0:
            return {'x': 0.5, 'o': 0.5}
        return False

    def visual_square_interior(self, square_number):
        """
        Visual representation of interior of one of game's squares.
        square_number is number of a square which we want to visualize.
        """
        square = self.squares()[square_number]
        visual_square = f'{square_number}'+' '*10+'\n'
        list_of_symbols = []
        if not square[0]:
            """
            If square is not collapsed we need to represent all spooky marks in
            that square.
            """
            for mark in square[1:]:
                list_of_symbols += [str(mark)]
            for i in range(10 - len(square)):
                list_of_symbols += ['']
            for i in [0, 3, 6]:
                a = list_of_symbols[i] + " " + list_of_symbols[i+1] + " " + \
                    list_of_symbols[i+2]
                visual_square += f'{a: <11}' + '\n'
                visual_square += ' '*11 + '\n'
        else:
            """
            When we encounter collapsed square we represent it by bigger marks.
            """
            if square[1].mark() == 'x':
                visual_square += ' '*11 + '\n'
                visual_square += r'   \  /    '+'\n'
                visual_square += r'    \/     '+'\n'
                visual_square += r'    /\     '+'\n'
                visual_square += r'   /  \ '+f'{square[1].move_number()}  \n'
                visual_square += ' '*11 + '\n'
            else:
                visual_square += r'    __     '+'\n'
                visual_square += r'   /  \    '+'\n'
                visual_square += r'  /    \   '+'\n'
                visual_square += r'  \    /   '+'\n'
                visual_square += r'   \__/ '+f'{square[1].move_number()}  \n'
                visual_square += ' '*11 + '\n'
        return visual_square

    def __str__(self):
        """
        Visual representation of current state of the game.
        """
        upper_third = ''
        for i in [1, 2, 3]:
            upper_third += self.visual_square_interior(i)
        middle_third = ''
        for i in [4, 5, 6]:
            middle_third += self.visual_square_interior(i)
        lower_third = ''
        for i in [7, 8, 9]:
            lower_third += self.visual_square_interior(i)
        upper_third = upper_third.splitlines()
        middle_third = middle_third.splitlines()
        lower_third = lower_third.splitlines()
        visual_table = ''
        horizontal_line = '_'*11+'|'+'_'*11+'|'+'_'*11+'\n'
        """
        Below we take every seventh element from table which was created
        when we used splitlines() on our thirds of game table. It works because
        visual_square_interior() produced 7 lines for each square since we want
        to add horizontal line we resign from last line from each square
        produced with visual_square interior().
        """
        for i in range(6):
            visual_table += upper_third[i]+'|'+upper_third[i+7]+'|' + \
                            upper_third[i+14]+'\n'
        visual_table += horizontal_line
        for i in range(6):
            visual_table += middle_third[i]+'|'+middle_third[i+7]+'|' + \
                            middle_third[i+14]+'\n'
        visual_table += horizontal_line
        for i in range(6):
            visual_table += lower_third[i]+'|'+lower_third[i+7]+'|' + \
                            lower_third[i+14]+'\n'
        return visual_table

    def move(self, move_number, player, opponent):
        """
        We use this function to go through one placement of mark during
        Quantum Tic Tac Toe game.
        First variable is current move number.
        Second is player who is moving.
        Third is opponent of the player who is moving.
        """
        mark = player.mark()
        entanglement = player.mark_choice(self)
        mark = Mark(mark, entanglement, move_number)
        self.add_entangled_mark(mark)
        new_path, cycle = self.paths_update(entanglement)
        if cycle:
            choice = player.collapse_choice(self, mark)
            self.collapse_squares(mark, choice)
        win = self.win_detection()
        if not win:
            return False
        return win

    def available_squares(self):
        """
        We return a set of squares which aren't collapsed.
        """
        free_squares = set()
        game = self.squares()
        for square in game:
            if not game[square][0]:
                free_squares = free_squares.union({square})
        return free_squares

    def both_options(self, mark):
        """
        This function returns two possible states of game after choice of
        square in which we want collapse some mark starting a cycle.
        It doesn't alter original game.
        """
        copied_game_1 = deepcopy(self)
        copied_mark_1 = deepcopy(mark)
        copied_game_2 = deepcopy(self)
        copied_mark_2 = deepcopy(mark)
        copied_game_1.add_entangled_mark(copied_mark_1)
        copied_game_2.add_entangled_mark(copied_mark_2)
        entanglement = mark.entanglement()
        path, cycle = copied_game_1.paths_update(entanglement)
        copied_game_2.paths_update(entanglement)
        if cycle:
            copied_game_1.collapse_squares(copied_mark_1, entanglement[0])
            copied_game_2.collapse_squares(copied_mark_2, entanglement[1])
        else:
            raise(ValueError)
        return copied_game_1, copied_game_2

    def available_pairs_of_squares(self):
        """
        This function returns list of pairs of squares in which we can
        place spooky marks. Since middle square is most strategically
        important if it isn't already collapsed we put pairs with it
        on the start of this list.
        """
        free_squares = list(self.available_squares())
        if 5 in free_squares:
            i_5 = free_squares.index(5)
            free_squares[i_5], free_squares[0] = free_squares[0],\
                free_squares[i_5]
        current_index = 0
        list_of_pairs = []
        for i in free_squares:
            current_index += 1
            for j in free_squares[current_index:]:
                list_of_pairs += [i, j]
        return list_of_pairs


def player_detection(move_number):
    """
    Since x's move numbers are odd and o's move numbers are even we
    can use this function to determine what player's mark is when all
    we have is move number.
    """
    if move_number % 2:
        return 'x'
    return 'o'
