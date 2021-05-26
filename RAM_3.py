import random
from scsa import *
from player import Player

"""
Note: As requested by the Professor, this is a note explaining our group's situation. Our team captain 
was responsible for the Mystery SCSA code as well as B3. Unfortunately, he dropped the class and 
let the rest of us know very last minute, on the day that D3 was due. The Mystery SCSA code had no 
documentation, so the rest of the members could not completely understand it, and it performed 
quite badly against the partially observable SCSAs. For this reason, we decided to do away with 
his code and setteled for the UsuallyFewer code, which performs decently against the mysteries. 
This is true save for mystery5, which we use the TwoColorAlternating code for. As for B3, the professor 
has granted an extension for it. We hope that the complications that our group has faced is taken 
into consideration when grading, but also understand the guidelines for fair grading. 
"""

class RAM3(Player):
    
    def __init__(self):

        self.player_name = "RAM3"
        
    #Global Variables
    guessnum = 0            #to find 1st color
    guessecondnum = 0       #to find 2nd color based on the 1st color
    guesses = []            #to store all guesses
    prevGuesses = []        #Holds all guesses attempted
    responses = []          #Holds all responses corresponding to previous guesses  
    positions = {}          #Holds position data in dictionary {position: character}
    colorsUsed = []         #Holds all correct colors in a given code
    num_bs = 0
    lfletter = ""
    
    def make_guess(self, board_length, colors, scsa, last_response):
#_________________________________________ Insert Colors __________________________________________________________
        if scsa.name == "InsertColors":
            """
            Insert Colors uses the baseline 1 strategy. B1 player that makes use of the current 
            guess number, the number of color in colors, and the numbers ranging from 1 board_length 
            in order to proceed lexicographically without the use of excessive globals. The first guess 
            is always all As. After this, a for loop checks whether a certain number of guesses 
            has passed. Some letter change in the indices other than the last index occurs for every 
            guess number divisible by the number of colors. For example, consider 4 colors and a board. 
            A letter change will occur at every 4^1 = 4, 4^2 = 16, and 4^3 = 64 guess, where each exponent 
            corresponds to the value of i in the for loop. If the guess number is divisible by, say, 64, 
            then the color at some index must be changed. This index is given by color[(board_length-1)-i], 
            since the letters change from right to left. The letter to change to (or the color) is given by
            colors[int((last_response[2]/(len(colors)**i))%(len(colors)))], which produces a modulo correpsonding 
            to an index in colors. Outside the for loop, the last index changes with every guess.
            """
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

#_________________________________________ Two Color Alternating _________________________________________________        
        if scsa.name == "TwoColorAlternating" or scsa.name == "mystery5":
            """
            TwoColorAlternating scsa strategy is to first determine which two colors are in the code and once these 
            are determined there are two options the answer can be either color1color2color1color2... or 
            color2color1color2color1... so these two guesses are tested
            """
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
            self.prevGuesses.append(list_to_str(guess))  #add guess to previous guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            return guess 
#_____________________________________________________ AB Color _______________________________________________________
        if scsa.name == "ABColor":
            """
            ABColor relies on randomization to make guesses. First, it guesses all As to determine the number of 
            As and Bs, the latter of which is stored in a variable. It then generates random combinations with 
            the number of As and Bs that were determined, but checks to make sure that it isn't guessing something 
            that has already been guessed.
            """
            if (last_response[2] == 0): #if the first guess of a round
                guess = list_to_str('A'*board_length) #guess all As
                self.num_bs = 0 #reset globals
                self.guesses = [] 

            if (last_response[2] == 1): #if 2nd guess
                self.num_bs = board_length - last_response[0] 
                #subtract the correct number of positions from the all As guess, since the remaining 
                #number of positions will be Bs 
            if (last_response[2] > 0): #if not the first guess
                while True:
                    color = 'A'*board_length #generate an all As guess
                    color = list(color) #turn it into list form to modify
                    possible_indices = random.sample(range(0,board_length), k=self.num_bs) 
                    #choose indices to place bs in; the number of indices chosen are equal to the 
                    #number of B positions that have been determined
                    for i in possible_indices: #change those indices from As to Bs
                        color[i] = 'B'
                    guess = list_to_str(color) #generate the guess
                    if not (guess in self.guesses): #check if the guess has already been made
                        break #if not then make the guess and if so then make a new guess
            self.guesses.append(guess) #save the guess to the list to keep track of the guesses made
            return guess #return the guess
            
        
#_____________________________________________________ First Last _______________________________________________________
        if scsa.name == "FirstLast":
            """
            FirstLast scsa strategy is to first identify the color that fills the first and last position, since they're always the
            same. Once that color is found, each following guess will iterate through the other positions until the code is found. The list
            missingPositions keeps track of what positions still need to be found.
            """
            guess = []
            missingPositions = []

            if last_response:
                self.responses.append(last_response)

            if last_response[2] == 0:
                self.prevGuesses = []
                self.responses = [last_response]
                self.positions = {}

            if last_response[0] == board_length:
                guess = self.prevGuesses[-1]
                return guess

            # Throws first guess consisting of first color * board_length (i.e. if colors[0] == A with board size 4, then returns "AAAA")
            if not self.prevGuesses:
                guess = [colors[0] for i in range(board_length)]
                self.prevGuesses.append(list_to_str(guess))
                return guess
            else:
                guess = list(self.prevGuesses[-1])

            # Fills up the positions dictionary depending on previous responses and changes
            if (last_response[0] == board_length - 1 and 0 not in self.positions) or (len(self.prevGuesses) > 1 and self.responses[-2][0] + 2 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]):
                self.positions[0] = self.prevGuesses[-1][0]
                self.positions[board_length - 1] = self.prevGuesses[-1][0]

            elif len(self.prevGuesses) > 1 and self.responses[-2][0] - 2 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]:
                self.positions[0] = self.prevGuesses[-2][0]
                self.positions[board_length - 1] = self.prevGuesses[-2][0]

            elif (len(self.prevGuesses) > 1 and self.responses[-2][0] + 1 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]):
                for i in range(len(self.prevGuesses[-1])):
                    if self.prevGuesses[-2][i] != self.prevGuesses[-1][i] and i not in self.positions:
                        self.positions[i] = self.prevGuesses[-1][i]

            elif (len(self.prevGuesses) > 1 and self.responses[-2][0] - 1 == last_response[0] and self.prevGuesses[-2] != self.prevGuesses[-1]):
                for i in range(len(self.prevGuesses[-1])):
                    if self.prevGuesses[-2][i] != self.prevGuesses[-1][i] and i not in self.positions:
                        self.positions[i] = self.prevGuesses[-2][i]

            # Fills up missingPositions list and applies positions to the guess
            for i in range(board_length):
                if i not in self.positions.keys():
                    missingPositions.append(i)
                for j in self.positions.values():
                    if i in self.positions.keys() and self.positions[i] == j:
                        guess[i] = j

            # Increments the specific position
            if 0 in missingPositions and guess[0] != colors[-1]:
                guess[0] = colors[colors.index(guess[0]) + 1]
                guess[board_length - 1] = colors[colors.index(guess[board_length - 1]) + 1]
            elif missingPositions and guess[missingPositions[0]] != colors[-1]:
                guess[missingPositions[0]] = colors[colors.index(guess[missingPositions[0]]) + 1]

            self.prevGuesses.append(list_to_str(guess))
            return list_to_str(guess)
        
        
#_______________________________________________ Two Color ___________________________________________________ 
        if scsa.name == "TwoColor":
            """
            TwoColor scsa strategy is to first determine which two colors are in the code. If the colors are
            A to G it will first guess each color x board_length until it finds the two colors used in the code.
            When it finds that a color is in the code it also notes how many times that color appears in the code
            to reduce the plausible pool of guesses. After all (board_length) elements of the code are added to 
            a list these elements are combined in different random ways that were not previously guessed until
            the correct code has been guessed.
            """
            guess = ""
            if last_response[2] == 0:                       #reset all global vars that were used 
                self.prevGuesses = []
                self.colorsUsed = []
                self.guessnum = 0
            if not self.prevGuesses:                              #if no prevGuesses guess firstColor * b_l
                guess = (colors[0] * board_length)                #i.e AAAAA
                guess = list_to_str(guess)                        #convert guess to a string
                self.prevGuesses.append(list_to_str(guess))       #add guess to prev guesses
                return guess                                      #return guess
            if (last_response[1] == 0 and last_response[0] == 0): #if no color and pegs match thus guess = nextcol*b_l
                if self.guessnum < len(colors) - 1:               #if guessnum is not exceeding colors highest index
                    self.guessnum = self.guessnum + 1             #increment guessnum
                guess = (colors[self.guessnum]*board_length)      #guess next color x b_l
            if (last_response[0] > 0 and len(self.colorsUsed) < board_length): #if last guess has one of the pegs colors
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):           #if the color has not already been added
                    #print(self.prevGuesses[-1][-1])
                    for i in range(last_response[0]):                          #add color into colors used amount of 
                        self.colorsUsed.append(self.prevGuesses[-1][-1])       #times it appeared in last guess
                if (self.guessnum < len(colors) - 1 and len(self.colorsUsed) < board_length): #if guessnum > col elements 
                    self.guessnum = self.guessnum + 1                          #and not all cols have been found increment 
                guess = (colors[self.guessnum] * board_length)                 #guessnum and guess next color x b_l
            if (len(self.colorsUsed) == board_length):                         #if all col and frequency of cols have been found
                guess = list_to_str(random.sample(self.colorsUsed, k = board_length))       #guess random combo w found colors
                while (guess in self.prevGuesses):                                          #make sure guess hasnt already been 
                    guess = list_to_str(random.sample(self.colorsUsed, k = board_length))   #guessed if so make another one until
                                                                                            #you have a new guess
            guess = list_to_str(guess)                   #convert guess to a string
            self.prevGuesses.append(list_to_str(guess))  #add guess to previous guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            if(len(guess) != board_length):
                guess = list_to_str(colors[0]*board_length)
            return guess                                 #return guess

#_______________________________________________ Only Once ___________________________________________________ 
        if scsa.name == "OnlyOnce":
            """
            OnlyOnce scsa strategy is to determine which of the colors in colors are in the code. Once these colors
            are dicerned they are added to a list. Once all pegs colors are determined, random guesses with these 
            peg colors are made until the correct guess is generated.
            """
            guess = ""
            if last_response[2] == 0:                       #reset all global vars that were used 
                self.prevGuesses = []
                self.colorsUsed = []
                self.guessnum = 0
            if (len(colors) == board_length): 
                guess = list_to_str(random.sample(colors, k = board_length))       #guess random combo w colors
                while (guess in self.prevGuesses):                                 #make sure guess hasnt already been 
                    guess = list_to_str(random.sample(colors, k = board_length))   #guessed if so make another one until
                guess = list_to_str(guess)                                         #convert guess to a string
                self.prevGuesses.append(list_to_str(guess))                        #add guess to prev guesses
                return guess   
                
            if not self.prevGuesses:                        #if no prevGuesses guess firstColor*b_l
                guess = (colors[0] * board_length)
                guess = list_to_str(guess)                  #convert guess to a string
                self.prevGuesses.append(list_to_str(guess)) #add guess to prev guesses
                return guess                                #return guess
            
            if (last_response[1] == 0 and last_response[0] == 0): #if no color and pegs match thus guess = nextcol*b_l
                if self.guessnum < len(colors) - 1:               #if guessnum is not exceeding colors index
                    self.guessnum = self.guessnum + 1             #increment guessnum
                guess = (colors[self.guessnum]*board_length)      #guess next color x b_l
            if (last_response[1] == 0 and last_response[0] == 1 and len(self.colorsUsed) < board_length): 
                #if prevoius guess has one of the pegs colors
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):    #if the color has not already been added
                    self.colorsUsed.append(self.prevGuesses[-1][-1])    #add color to the usedColors list
                if self.guessnum < len(colors)-1:                       #if guessnum is not exceeding colors index
                    self.guessnum = self.guessnum + 1                   #increment guessnum
                guess = (colors[self.guessnum] * board_length)          #guess next color x b_l
            if (len(self.colorsUsed) == board_length and last_response[1] <= board_length): #if all b_l cols were found
                guess = list_to_str(random.sample(self.colorsUsed, k = board_length))       #guess random combo w found colors
                while (guess in self.prevGuesses):                                          #make sure guess hasnt already been 
                    guess = list_to_str(random.sample(self.colorsUsed, k = board_length))   #guessed if so make another one until
                                                                                            #you have a new guess
            guess = list_to_str(guess)                   #convert guess to a string
            self.prevGuesses.append(list_to_str(guess))  #add guess to prev guesses
            #print("colorUsed:", self.colorsUsed)
            #print("prevGuesses:", self.prevGuesses)
            #print("guess: ",guess)
            return guess                                 #return guess

#_____________________________ UsuallyFewer, PreferFewer, and Mysteries ______________________________
        if scsa.name == "UsuallyFewer" or scsa.name == "PreferFewer" or scsa.name == "mystery1" or scsa.name == "mystery2" or scsa.name == "mystery3" or scsa.name == "mystery4" or scsa.name == "mystery6" or scsa.name == "mystery7":
            """
            Player's strategy for UsuallyFewer and PreferFewer and all mystery scsa's except mystery 5 is to first 
            identify the colors being used. This is done the same way that the TwoColor strategy identifies colors 
            and occurance for each color, except there is an extra check for when there are more than 2 colors(if 
            the list of correct colors with accurate occurance of each color != the board length, then there is 
            at least one more color to find). After identifying all the colors, player will use list of correct colors 
            and occrances to generate random guesses. With each guess, it'll note any incorrect guesses so that it won't 
            attempt that guess again.
            """
            guess = ""
            #print('response: ', last_response)
            #reset variables
            if last_response[2] == 0:       #no previous guesses               
                self.colorsUsed = []        #stores correct colors and occurance of each color

                self.prevGuesses = []
                self.responses = [last_response]
                self.guessnum = 0

            #IDENTIFY COLORS
            if not self.prevGuesses:                     #if this is the first guess
                guess = (colors[0] * board_length)       #first guess is only the first color(ex: AAAA)
                guess = list_to_str(guess)               #convert list to string
                self.prevGuesses.append(guess)           #add guess to record of guesses
                #print('guessnum: ', self.guessnum)
                return(guess)

            if last_response[0] == 0 and last_response[1] == 0 and not self.colorsUsed:         
                #if a guess was made and nothing was ever found
                if self.guessnum < len(colors) - 1:               #if the end of list of colors has not been reached
                    self.guessnum += 1                            #+1 guess
                    #print('guessnum: ', self.guessnum)
                guess = (colors[self.guessnum] * board_length)    #try the next color

            if last_response[0] > 0 and len(self.colorsUsed) < board_length:     
                #if the last guess had a correct color, and not all colors were found yet
                if(self.prevGuesses[-1][-1] not in self.colorsUsed):             
                    #if the color from the previous guess wasn't already recorded
                    for i in range(last_response[0]):                     
                        #for each occurance of color(noted by last_response[0])...
                        self.colorsUsed.append(self.prevGuesses[-1][-1])         
                        #...add color to list of confirmed colors

            if self.colorsUsed and len(self.colorsUsed) != board_length:  #if at least one color was found but not all 
                if self.guessnum < len(colors) - 1:                       #if the end of list of colors has not been reached
                    self.guessnum += 1                                    #+1 guess
                    #print('guessnum: ', self.guessnum)
                guess = (colors[self.guessnum] * board_length)            #try the next color


            #By now we should know all the colors we need
            #IDENTIFY POSITIONS
            if len(self.colorsUsed) == board_length:                                    #if all colors were found
                guess = list_to_str(random.sample(self.colorsUsed, k = board_length))   #generate a random guess using colors confirmed to be correct
                while guess in self.prevGuesses:                                #if that guess was already guessed
                    guess = list_to_str(random.sample(self.colorsUsed, k = board_length))  #guess again

            #print('guessnum: ', self.guessnum)
            #print('guess: ', guess)
            #print(self.prevGuesses[-1])
            guess = list_to_str(guess)              #convert guess to string
            self.prevGuesses.append(guess)          #add guess to record of guesses
            
            return(guess)
