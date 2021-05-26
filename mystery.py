from mastermind import *
from scsa import *
#from player import *
from player import Player
import time
#Box 2
class Ram5(Player): #b1
    """B3 finds the number of occurences of each letter, then relies on randomization to guess
    different combinations of those letters
    """
    def __init__(self):

        self.player_name = "Ram5"
    #Global Variables
    guessnum = 0            #to find 1st color
    guessecondnum = 0       #to find 2nd color based on the 1st color
    guesses = []            #to store all guesses
    prevGuesses = []        #Holds all guesses attempted
    responses = []          #Holds all responses corresponding to previous guesses  
    positions = {}          #Holds position data in dictionary {position: character}
    colorsUsed = []         #Holds all correct colors in a given code
    num_bs = 0
    def make_guess(self, board_length, colors, scsa, last_response): 
            if last_response[2] == 0:                       #reset all global vars that were used 
                self.prevGuesses = []
                self.colorsUsed = []
                self.guessnum = 0
                self.guessecondnum = 0 
            if not self.prevGuesses:                              #if no prevGuesses guess firstColor * b_l
                guess = (colors[0] * board_length)                #i.e AAAAA
                guess = list_to_str(guess)                        #convert guess to a string
                self.prevGuesses.append(list_to_str(guess))       #add guess to prev guesses
                return guess                                      #return guess
            if (last_response[1] == 0 and last_response[0] == 0): #if no color and pegs match thus guess = nextcol*b_l
                if self.guessnum < len(colors) - 1:               #if guessnum is not exceeding colors highest index
                    self.guessnum = self.guessnum + 1             #increment guessnum
                guess = (colors[self.guessnum]*board_length)      #guess next color x b_l
            if (last_response[0] > 0 and len(self.colorsUsed) < 2):      #if guess had no pegs matched and colorsUsed < 2
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):     #if the color has not already been added
                    #print(self.prevGuesses[-1][-1])
                    self.colorsUsed.append(self.prevGuesses[-1][-1])     #add color to colorsUsed  
                if (self.guessnum < len(colors) - 1 and len(self.colorsUsed) < board_length): #if guessnum > col elements 
                    self.guessnum = self.guessnum + 1                          #and not all cols have been found increment 
                guess = (colors[self.guessnum] * board_length)                 #guessnum and guess next color x b_l
            if (len(self.colorsUsed) == 2):                       #if all colors have been found in code
                guess = ""
                if (self.guessecondnum == 0):                     #guess 1 c1c2c1c2...
                    for i in range(board_length):                 #alternate color1 and color2 board_len times
                        if (i % 2 == 0):                
                            guess = guess + self.colorsUsed[0]
                        if (i % 2 == 1):
                            guess = guess + self.colorsUsed[1]
                if (self.guessecondnum == 1):                     #guess 2 c2c1c2c1...
                    for i in range(board_length):                 #alternate color2 and color1 board_len times
                        if (i % 2 == 0):
                            guess = guess + self.colorsUsed[1]
                        if (i % 2 == 1):
                            guess = guess + self.colorsUsed[0]
                self.guessecondnum = self.guessecondnum + 1       #increment guesscondnum

            guess = list_to_str(guess)                   #convert guess to a string
            if(len(guess) != board_length):
                guess = list_to_str(colors[0]*board_length)
                
            self.prevGuesses.append(list_to_str(guess))  #add guess to previous guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            
            return guess 
       

#Boxes for mysteries
board_length = 5 # Number of pegs
num_colors = 7 # Number of colors
colors = [chr(i) for i in range(65,91)][:num_colors] # Retrieves first num_colors from list of all colors 
player = Ram5()
scsa = InsertColors()
code_file = "Mystery5_5_7.txt"

mastermind = Mastermind(board_length, colors)

mastermind.practice_tournament(player, scsa, code_file)