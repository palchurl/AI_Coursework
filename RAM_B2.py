import random
from scsa import *
from player import Player

class RAMB2(Player): #b2
    
    """
    B2 player that relies on similar lexicographic strategy as B1, but skips over some guesses. 
    Please refer to the B1 documentation to understand the for loops; they are used again to change 
    the color at an index after a certain number of guesses has passed. B2 has code that allows it to 
    skip over colors that have been ruled out. After making the first guess, there last_response 
    is checked to see if the previous guess produced '0 0 (guess number).' If such is the case, 
    then no colors were correct in that guess and should not appear in subsequent guesses. The while 
    loop continues producing guesses until it produces one that has no colors that were determined 
    to be invalid. If the previous guess did not have '0 0 (guess number)' then a different while 
    loop cycles through the guesses in a similar manner until an acceptable one is produced. Honestly, 
    the code could have been written using a single while loop, since they esentially do the same 
    thing, but because of errors during testing this longer version was opted for.
    """

    def __init__(self):

        self.player_name = "RAMB2"
    guesses = [] #for all guesses made
    guessnum = 0 
    #esentially the same function as last_response[2], i.e. the guess number; 
    #a separate variable with the same functionality had to be used because 
    #last_response[2]'s value cannot be changed when cycling through guesses
    invalid_letters = set() 
    #to hold invalid colors, which each guess produced is checked against
    def make_guess(self, board_length, colors, scsa, last_response):
        if (last_response[2] == 0): #if the first guess
            guess = list_to_str('A'*board_length) #guess all As
            self.guessnum = 0 #reset globals
            self.invalid_letters = set()
        else:
            color = list(self.guesses[-1]) 
            #retrieve the previous guess for lexicographic enumeration
            if (last_response[0] == 0 and last_response[1] == 0): 
                #check if last guess had colors that were totally ruled out 
                #and should not appear in future guesses
                self.invalid_letters.update(self.guesses[-1]) 
                #if it did then put those colors into the set
                                        
                while (set(color).isdisjoint(self.invalid_letters) != True): 
                    #check if the guess at the beginning/guesses produced have 
                    #any invalid colors; if so, then produce a new guess that comes after the current one

                    for i in range(1,board_length+1): 
                        #i takes on the values from 1 to the board_length, here with 1 
                        #added to account for range's exclusivisity; the i values will be 
                        #used as exponents
                        if (self.guessnum%(len(colors)**i)) == 0: 
                            #this checks wether a certain number of guesses has passed; the number 
                            #of guesses at which a letter in one of the guess indices must change is
                            #always divisible by the number of colors
                            color[(board_length-1)-i] = colors[int((self.guessnum/(len(colors)**i))%(len(colors)))] 
                            #this determines what color in colors to change the index to (starting from 
                            #the right); the expression produces a modulo value that is the index of 
                            #some color in colors 
                    color[-1]= colors[self.guessnum%len(colors)] 
                    #since the last index changes with every guess, it is simply 
                    #a modulo value based on the guess number
                    self.guessnum = self.guessnum + 1 
                    #mimic the incrementing of last_response[2] by incrementing guessnum
            
            else: 
                #this code here does basically the same thing as the code above, 
                #just in do-while format instead of while so that a new guess is first produced 
                while True: 
                    #as an example, consider BBB in a 3-4 game, which has no As 
                    #and would thus be disjoint to invalid_letters at the time it 
                    #is produced. When it is retrieved as the previous guess, it 
                    #should be changed to BBC before BBC is checked for disjunction
                    self.guessnum = self.guessnum + 1
                    for i in range(1,board_length+1):
                        if (self.guessnum%(len(colors)**i)) == 0: 
                            #4th 16th or 64th guess, i is 1 2 or 3
                            color[(board_length-1)-i] = colors[int((self.guessnum/(len(colors)**i))%(len(colors)))]

                    color[-1]= colors[self.guessnum%len(colors)]
                    if (set(color).isdisjoint(self.invalid_letters) == True): 
                        #once the guess has no invalid letters, break out of the while loop
                        break               
            guess = list_to_str(color)  
            #turn the final list into a string guess
             
        self.guesses.append(guess) 
        #save the guess that will be made
        return guess #make the guess



