import random
from scsa import *
from player import Player

class RAMB1(Player): #b1
    """
    B1 player that makes use of the current guess number, the number of color in colors, 
    and the numbers ranging from 1 board_length in order to proceed lexicographically without 
    the use of excessive globals. The first guess is always all As. After this, a for loop
    checks whether a certain number of guesses has passed. Some letter change in the indices other 
    than the last index occurs for every guess number divisible by the number of colors. For 
    example, consider 4 colors and a board. A letter change will occur at every 4^1 = 4, 4^2 = 16, 
    and 4^3 = 64 guess, where each exponent corresponds to the value of i in the for loop. If the 
    guess number is divisible by, say, 64, then the color at some index must be changed. This index 
    is given by color[(board_length-1)-i], since the letters change from right to left. The letter to 
    change to (or the color) is given by colors[int((last_response[2]/(len(colors)**i))%(len(colors)))], 
    which produces a modulo correpsonding to an index in colors. Outside the for loop, the last 
    index changes with every guess.
    """
    def __init__(self):

        self.player_name = "RAMB1"
    guesses = [] #store all guesses
    
    def make_guess(self, board_length, colors, scsa, last_response):
        if (last_response[2] == 0): #guess all As on the first guess
            guess = list_to_str('A'*board_length) 
            self.guesses = [] #reset global at the start of every round
        else:
            color = list(self.guesses[-1]) #retrieve the previous guess made, since the 
                                           #next guess will just follow lexicographically after the previous one
            for i in range(1,board_length+1): 
                #i takes on the values from 1 to the board_length, here with 1 added to account for 
                #range's exclusivisity; the i values will be used as exponents
                if (last_response[2]%(len(colors)**i)) == 0: 
                    #this checks wether a certain number of guesses has passed; the number of guesses 
                    #at which a letter in one of the guess indices must change is always divisible by the number of colors 
                    color[(board_length-1)-i] = colors[int((last_response[2]/(len(colors)**i))%(len(colors)))] 
                    #this determines what color in colors to change the index to (starting from the right); 
                    #the expression produces a modulo value that is the index of some color in colors 
                    
            color[-1]= colors[last_response[2]%len(colors)] 
            #since the last index changes with every guess, it is simply a modulo 
            #value based on the guess number
            guess = list_to_str(color) #turn the final list into a string guess
    
        #print(last_response[2], ' ', 'guess ', guess)
        self.guesses.append(guess) #save the guess that will be made
        return guess #make the guess