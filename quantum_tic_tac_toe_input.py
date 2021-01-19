def number_of_rounds_input():
    number_of_rounds = None
    while not (type(number_of_rounds) == int):
        number_of_rounds = input('Choose number of rounds you wish to play: ')
        number_of_rounds = remove_spaces_from_one_item_str(number_of_rounds)
        if number_of_rounds.isdigit():
            number_of_rounds = int(number_of_rounds)
            if number_of_rounds < 1:
                print('\nNumber of rounds must at least be equal to 1.\n')
                number_of_rounds = False
        else:
            print('\nNumber of rounds must be an integer grater than or equal'
                  + ' to 1.\n')
    return number_of_rounds


def player_mode_input(player_number):
    player_mode = None
    while player_mode not in [0, 1, 2]:
        player_mode = input(f'Choose player {player_number} mode: ')
        player_mode = remove_spaces_from_one_item_str(player_mode)
        if player_mode.isdigit():
            player_mode = int(player_mode)
            if player_mode not in [0, 1, 2]:
                print('Player mode must be 0, 1 or 2')
        else:
            print('Player mode must be 0, 1 or 2')
    return player_mode


def remove_spaces_from_one_item_str(string):
    split_str = string.split()
    if len(split_str) == 1:
        return split_str[0]
    return ''


def collapse_input(entanglement):
    chosen_square = None
    while not (chosen_square in entanglement):
        print(f'\nYou must choose between square {entanglement[0]}'
              + f' and {entanglement[1]}.')
        chosen_square = input('\nChoose square in which you want to'
                              + ' collapse previous move: ')
        chosen_square = remove_spaces_from_one_item_str(chosen_square)
        if chosen_square.isdigit():
            chosen_square = int(chosen_square)
    print('\n')
    return chosen_square


def entanglement_input(free_squares, game):
    chosen_squares = [0, 0]
    while not (chosen_squares[0] in free_squares and chosen_squares[1]
               in free_squares and len(chosen_squares) == 2):
        chosen_squares = input("\n\nChoose squares to place "
                               + "entanglement to: ").split()
        print('\n')
        if len(chosen_squares) == 1 or len(chosen_squares) == 0:
            print('Input is incorrect. Correct input format is:'
                  + '*square number* *square number*')
            chosen_squares = [0, 0]
        else:
            if chosen_squares[0].isdigit() and\
               chosen_squares[1].isdigit() and\
               len(chosen_squares) == 2:
                chosen_squares[0] = int(chosen_squares[0])
                chosen_squares[1] = int(chosen_squares[1])
                if not(chosen_squares[0] in range(1, 10) and
                        chosen_squares[1] in range(1, 10)):
                    print('You need to choose numbers from 1 to 9')
                elif chosen_squares[0] == chosen_squares[1]:
                    chosen_squares = [0, 0]
                    print('You need to choose two different squares.')
                elif game.squares()[chosen_squares[0]][0] or\
                        game.squares()[chosen_squares[1]][0]:
                    print('You need to choose square which is not '
                          + 'collapsed.')
            else:
                print('Input is incorrect. Correct input format is:'
                      + '*square number* *square number*')
    return chosen_squares
