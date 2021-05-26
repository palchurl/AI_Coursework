# Main file to run game of Mastermind based on command-line arguments
# See example.ipynb for other ways to use the Mastermind representation

import sys
from scsa import *
from player import *
from mastermind import *
from RAM import *

if len(sys.argv) != 6:
     
    print("Usage: python3 main.py <board length> <num colors> <player name> <scsa name> <num rounds>")
     
    sys.exit(1)

board_length = int(sys.argv[1])
num_colors = int(sys.argv[2])
player_name = sys.argv[3]
scsa_name = sys.argv[4]
num_rounds = int(sys.argv[5])


if player_name == "RandomFolks":

    player = RandomFolks()

elif player_name == "Boring":

    player = Boring()

elif player_name == "RAM":
    
    player = RAM()
    
else:

    print("Unrecognized player.")
    sys.exit(1)


if scsa_name == "InsertColors":

    scsa = InsertColors()

elif scsa_name == "TwoColor":

    scsa = TwoColor()

elif scsa_name == "ABColor":

    scsa = ABColor()

elif scsa_name == "TwoColorAlternating":

    scsa = TwoColorAlternating()

elif scsa_name == "OnlyOnce":

    scsa = OnlyOnce()

elif scsa_name == "FirstLast":

    scsa = FirstLast()

elif scsa_name == "UsuallyFewer":

    scsa = UsuallyFewer()

elif scsa_name == "PreferFewer":

    scsa = PreferFewer()

else:

    print("Unrecognized SCSA.")
    sys.exit(1)

colors = [chr(i) for i in range(65,91)][:num_colors]

mastermind = Mastermind(board_length, colors)

mastermind.play_tournament(player, scsa, num_rounds)