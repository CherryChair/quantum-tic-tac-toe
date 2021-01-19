from quantum_tic_tac_toe_class import Quantum_Tic_Tac_Toe
from player_class import Player, Computer_Easy, Computer_Hard


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
    if x_score == 1:
        pass
    elif o_score == 1:
        pass
    else:
        pass
    return x_score, o_score


def main():
    player_1 = Computer_Hard("x")
    player_2 = Computer_Easy("o")
    x, o = one_round(player_1, player_2)
    pass


if __name__ == "__main__":
    main()
