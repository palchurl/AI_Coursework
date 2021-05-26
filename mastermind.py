# File contains implementation of a representation for Mastermind and Rounds of Mastermind
# See main.py or examples.ipynb for example usages

import random
import time
from operator import sub
from scsa import *
from player import *

def letter_to_num(letter):
    """Converts letter to number based on position its in alphabet

    Args:
        letter (chr): Letter to convert to number. 

    Returns:
        int: Position of letter in alphabet.
    """

    return ord(letter) - 64

def old_score(results):
    """Computes score using old score function for a tournament

    Args:
        results (dict): Dictionary containing number of wins, losses, and failures for a tournament.

    Returns:
        num: Returns score for a tournament based on the results.
    """

    return 5*results["win"] - 2*results["failure"]


class Round:
    """Representation for round of the game of Mastermind
    """

    def __init__(self, board_length, colors, answer, scsa_name, guess_cutoff = 100, time_cutoff = 5):
        """Constuctor for Round

        Args:
            board_length (int): Number of pegs.
            colors (list of strs): All possible colors that can be used to generate a code.
            answer (string): Answer for the round that the player is trying to guess.
            scsa_name (str): Name of SCSA used to generate secret code.
            guess_cutoff (int, optional): Number of guesses allowed per round. Defaults to 100.
            time_cutoff (int, optional): Amount of time in seconds allowed for the round. Defaults to 5.
        """

        self.board_length = board_length
        self.colors = colors
        self.answer = answer
        self.scsa_name = scsa_name
        self.guesses = 0
        self.guess_cutoff = guess_cutoff
        self.time_cutoff = time_cutoff
        self.time_buffer = 0.1 # Seconds
        self.time_used = 0

    def valid_guess(self, guess):
        """Checks whether a guess is valid

        Args:
            guess (str): Guess of secret code.

        Returns:
            bool: Returns True if guess is valid (correct length and uses only possible colors) and False otherwise.
        """

        if len(guess) != self.board_length:

            return False

        for peg in guess:

            if peg not in self.colors:

                return False 

        return True

    def count_colors(self, guess):
        """Counts number of occurences for each color 

        Args:
            guess (str): Guess of secret code.

        Returns:
            list of ints: Returns list of number of occurences for each color in color.
        """

        counts = [0]*len(self.colors)

        for peg in guess:

            idx = letter_to_num(peg) - 1

            counts[idx] += 1

        return counts

    def process_guess(self, guess):
        """Determines number of exactly correct pegs and partially correct pegs for a guess 

        Args:
            guess (str): Guess of secret code.

        Returns:
            exact (int): Number of pegs that match exactly with the answer.
            other (int): Number of pegs that are the right color, but in the wrong location.
        """

        guess_color_count = self.count_colors(guess)
        answer_color_count = self.count_colors(self.answer)

        exact = 0
        other = 0

        for i in range(self.board_length):

            if guess[i] == self.answer[i]:

                exact += 1

                # Decrease color counts
                guess_color_count[letter_to_num(guess[i])-1] -= 1
                answer_color_count[letter_to_num(self.answer[i])-1] -= 1

        for i in range(len(self.colors)):

            if answer_color_count[i] <= guess_color_count[i]:

                other += answer_color_count[i]

            elif guess_color_count[i] < answer_color_count[i] and guess_color_count[i] > 0:

                other += guess_color_count[i]

        return exact, other


    def respond_to_guess(self, guess):
        """Responds with correctness of player's guess

        Args:
            guess (str): Guess of secret code

        Returns:
            string or tuple of ints: Returns "win" if guess is answer, returns "invalid" if guess is not valid, and 
                                     returns number of correct pegs, number of correct colors in wrong position, 
                                     and number of guesses so far otherwise.
        """

        if guess == self.answer:

            response = "win"

        elif self.valid_guess(guess):
            
            exact, other = self.process_guess(guess)

            response = (exact, other, self.guesses)

        else:

            response = "invalid"

        return response

    def play_round(self, player):
        """Plays out a round of Mastermind

        Args:
            player (Player): Player to guess secret code.

        Returns:
            str: Result of round (win, loss, or failure).
            int: Number of rounds until that result was achieved.
        """

        response = (0,0,0)

        while self.guesses < self.guess_cutoff:

            start = time.time()
            guess = player.make_guess(self.board_length, self.colors, self.scsa_name, response)
            end = time.time()

            self.guesses += 1

            duration = end - start

            self.time_used += duration

            if self.time_used > self.time_cutoff + self.time_buffer:

                return ("loss", self.guesses)

            response = self.respond_to_guess(guess)

            #print("Response:", response, "Time:", self.time_used)

            if response == "win":

                return ("win", self.guesses)

            elif response == "invalid":

                return ("failure", self.guesses)

        return ("loss", self.guesses)


class Mastermind:
    """Representation to play the game of Mastermind
    """

    def __init__(self, board_length = 4, colors = [chr(i) for i in range(65,91)], guess_cutoff = 100, round_time_cutoff = 5, tournament_time_cutoff = 300):
        """Constructor for Mastermind

        Args:
            board_length (int, optional): Number of pegs. Defaults to 4.
            colors (list, optional): List of colors that can be used to generate a secret code. Defaults to [chr(i) for i in range(65,91)].
            guess_cutoff (int, optional): Number of guesses allowed per round. Defaults to 100.
            round_time_cutoff (int, optional):  Amount of time in seconds allowed for the round. Defaults to 5.
            tournament_time_cutoff (int, optional): Amount of time in seconds allowed for the round. Defaults to 300.
        """

        self.board_length = board_length
        self.colors = colors
        self.num_colors = len(colors)
        self.guess_cutoff = guess_cutoff
        self.round_time_cutoff = round_time_cutoff
        self.tournament_time_cutoff = tournament_time_cutoff
        self.time_used = 0

    def print_results(self, player, scsa_name, results, score, num_rounds):
        """Prints results for a tournament

        Args:
            player (Player): Player who played in the tournament.
            scsa_name (str): Name of SCSA used to generate codes in tournament.
            results (dict): Dictionary containing number of wins, losses, and failures for a tournament.
            score (float): Score for tournament computed based on function in project description.
            num_rounds (int): Number of rounds in the tournament.
        """

        print("Player:", player.player_name)
        print("SCSA Name:", scsa_name)
        print("Game:", self.board_length, "Pegs", self.num_colors, "Colors")
        print("Rounds:", sum(results.values()), "out of", num_rounds)
        print("Results:", results)
        print("Score:", score)

        return 

    def play_tournament(self, player, scsa, num_rounds):
        """Plays a tournament of Mastermind

        Args:
            player (Player): Player who plays in tournament, making guesses.
            scsa (SCSA): SCSA used to generate secret codes for player to guess.
            num_rounds (int): Number of rounds to play Mastermind.
        """
        
        results = {"win": 0, "loss": 0, "failure": 0}

        score = 0

        for i in range(1,num_rounds+1):

            code = scsa.generate_codes(self.board_length, self.colors, 1)

            round = Round(self.board_length, self.colors, code, scsa.name, self.guess_cutoff, self.round_time_cutoff)

            start = time.time()
            result, guesses = round.play_round(player)
            end = time.time()

            duration = end - start
            
            self.time_used += duration

            if self.time_used > self.tournament_time_cutoff:

                break
            
            #print("Round:", i, "Result:", result, "Guesses:", guesses)

            results[result] += 1

            if result == "win":

                score += self.board_length*len(self.colors)*(5*guesses**(-0.5))

            elif result == "failure":

                score -= 2*self.board_length*len(self.colors)

                break

        self.print_results(player, scsa.name, results, score, num_rounds)

        return 


    def practice_tournament(self, player, scsa_name, code_file):
        """Plays a tournament of Mastermind using pregenerated codes from file

        Args:
            player (Player): Player who plays in tournament, making guesses.
            scsa_name (str): Name of SCSA used to generate codes in tournament.
            code_file (str): Name of file to read secret codes from.
        """

        codes = read_from_file(code_file)

        num_rounds = len(codes)

        results = {"win": 0, "loss": 0, "failure": 0}

        score = 0

        cur_round = 0

        for code in codes:

            cur_round += 1

            round = Round(self.board_length, self.colors, code, scsa_name, self.guess_cutoff, self.round_time_cutoff)

            start = time.time()
            result, guesses = round.play_round(player)
            end = time.time()

            duration = end - start
            
            self.time_used += duration

            if self.time_used > self.tournament_time_cutoff:

                break

            #print("Round:", cur_round, "Result:", result, "Guesses:", guesses)

            results[result] += 1

            if result == "win":

                score += self.board_length*len(self.colors)*(5*guesses**(-0.5))

            elif result == "failure":

                score -= 2*self.board_length*len(self.colors)

                break

        self.print_results(player, scsa_name, results, score, num_rounds)

        return
