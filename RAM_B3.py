import random
from scsa import *
from player import Player

class RAMB3(Player): #b3
    """**Note:Professor granted our group an extension for B3 because of our group's situation. This is why B3 is
    sumbitted late.
    B3 finds the number of occurences of each letter, then relies on randomization to guess
    different combinations of those letters
    """
    def __init__(self):

        self.player_name = "RAMB3"
    guesses = [] #all guesses made
    num_colors = [] #store occurence of each letter
    def make_guess(self, board_length, colors, scsa, last_response): 
        if (last_response[2] == 0): #if the first guess of a round
            self.guesses = [] #reset globals
            self.num_colors = []
        if (last_response[2] < (len(colors)-1)): #guess monochromatic combos of all c-1 colors; e.g. 3 colors, len = 3, want colors[0] and colors[1]
            guess = list_to_str(colors[last_response[2]]*board_length) 
        if (last_response[2] < (len(colors))): #colors ranging up to c
            if (last_response[0] !=0): #check if the last guess had any correct colors
                self.num_colors.extend(colors[last_response[2]-1]*last_response[0]) #if so, store that color the number of times it appears into the list
            if (last_response[2] == len(colors)-1): #if at the cth color
                if (len(self.num_colors) < board_length): #any positions not filled by the c-1 colors must be filled by the cth color
                    self.num_colors.extend(colors[last_response[2]]*(board_length - len(self.num_colors))) #if this is the case then store the cth color the number of times it appears into the list
        if (last_response[2] >= (len(colors)-1)): #after making c-1 monochromatic guesses, a list with every color and its occurence has been obtained; combos of the list will be guessed for the rest of the guesses
            while True: 
                random.shuffle(self.num_colors) #shuffle the list
                guess = list_to_str(self.num_colors) #generate a guess
                if not (guess in self.guesses): #if the guess has not already been made
                    break #stop looping so the guess can be made
        self.guesses.append(guess) #save all guesses made
        return guess #make the guess
