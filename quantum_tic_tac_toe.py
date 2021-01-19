from classes_quantum_tic_tac_toe import Quantum_Tic_Tac_Toe
from quantum_tic_tac_toe_input import (
    number_of_rounds_input,
    player_mode_input
)
from os import system


def one_round(player_1, player_2):
    q = Quantum_Tic_Tac_Toe()
    move_number = 0
    winner = False
    while not winner:
        move_number += 1
        winner = q.move(move_number, player_1, player_2)
        player_1, player_2 = player_2, player_1
    x_score = winner['x']
    o_score = winner['o']
    print(str(q))
    if x_score == 1:
        print('!!! X won !!!')
    elif o_score == 1:
        print('!!! O won !!!')
    else:
        print('Tie')
    return x_score, o_score


def main():
    system('clear')
    number_of_rounds = number_of_rounds_input()
    print('\nPlayer modes:\n0 - human player\n1 - computer player (easy)')
    print('2 - computer player (hard)\n')
    player_1 = player_mode_input(1)
    player_2 = player_mode_input(2)
    p1_score = 0
    p2_score = 0
    for i in range(number_of_rounds):
        round_score = one_round(player_1, player_2)
        p1_score += round_score[i % 2]
        p2_score += round_score[(i+1) % 2]
        player_1, player_2 = player_2, player_1
        print(f'\nThe score is:\nPlayer 1:{p1_score}\nPlayer 2:{p2_score}'
              + '\n\n')
        print(f'End of round {i+1}. Press enter to continue.\n\n')
        input()
    if p1_score > p2_score:
        print('!!!!!!! Player 1 won the match !!!!!!!')
    elif p1_score == p2_score:
        print('Match was tied.')
    else:
        print('!!!!!!! Player 2 won the match !!!!!!!')


if __name__ == "__main__":
    main()
