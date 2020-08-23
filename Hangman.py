# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 14:32:49 2020

@author: Ayush Mittal
"""
 # Import files to modules used in project
import random
import time
import os

# Global Variables
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
     
# Class for player properties  
class Player:
    
    # Player Constructor
    def __init__(self, inputName):
        self.name = inputName
        self.strikes = 0
    
    # Increment Strike by 1
    def incrementStrike(self):
        self.strikes += 1
    
    # Print of Player object
    def __str__(self):
        return "{0} ({1} Strike)\n".format(self.name, self.strikes) + self.printTextArt()
    
    # Print of Text Art based on number of strikes
    def printTextArt(self):
        if self.strikes == 0:
            img = '''
            +---+
            |    
            |    
            |    
            |
            ===
            '''
        elif self.strikes == 1:
            img = '''
            +---+
            |   o
            |    
            |    
            |
            ===
            '''
        elif self.strikes == 2:
            img = '''
            +---+
            |   o
            |   |
            |    
            |
            ===
            '''
        elif self.strikes == 3:
            img = '''
            +---+
            |   o
            |  /|
            |    
            |
            ===
            '''
        elif self.strikes == 4:
            img = '''
            +---+
            |   o
            |  /|\\
            |  
            |
            ===
            '''
        elif self.strikes == 5:
            img = '''
            +---+
            |   o
            |  /|\\
            |  /
            |
            ===
            '''
        elif self.strikes == 6:
            img = '''
            +---+
            |   o
            |  /|\\
            |  / \\
            |
            ===
            You ran out of Lives
            '''
        else:
            img = "HUSTON WE HAVE A PROBLEM"
        
        return img
    
    # Get next move from Player
    def getMove(self , obscuredWord, guessed):
        print(self)
        print("Word:        {}".format(obscuredWord))
        print("Word Length: {}".format(len(obscuredWord)))
        print("Guessed:     {}".format(guessed))
        print("")
        return input("Guess a letter, word, or type 'exit':\t")

# Obtain a New Word from file based on difficulty level sellected by user
def GetWord(difficulty):
    if difficulty == "E":
        file = "wordList/google-10000-english-usa-no-swears-short.txt"
    elif difficulty == "M":
        file = "wordList/google-10000-english-usa-no-swears-medium.txt"
    else:
        file = "wordList/google-10000-english-usa-no-swears-long.txt"
        
    with open(file, 'r') as f:
        lines = f.readlines()
        word = random.choice(lines)
        return word.strip().upper()

# Get the obscured version of Word based on letters already guessed
def obscureWord(word, guessed):
    rv = ''
    for s in word:
        if (s in LETTERS) and (s not in guessed):
            rv = rv+'_'
        else:
            rv = rv+s
    return rv

# Initial Heading of game
def header():
    os.system('cls')
    print('='*30)
    print(' HANGMAN GAME By AYUSH MITTAL')
    print('='*30)
    print('')

# Get a move from player and validate it
def requestPlayerMove(player, guessed):
    while True: # we're going to keep asking the player for a move until they give a valid one
        time.sleep(0.1) # added so that any feedback is printed out before the next prompt
        
        header()
        move = player.getMove(obscureWord(word, guessed), guessed)
        move = move.upper() # convert whatever the player entered to UPPERCASE
        if move == 'EXIT':
            return move
        elif len(move) == 1: # they guessed a character
            if move not in LETTERS: # the user entered an invalid letter (such as @, #, or $)
                print('Guesses should be letters. Try again.')
                time.sleep(2)
                continue
            elif move in guessed: # this letter has already been guessed
                print('{} has already been guessed. Try again.'.format(move))
                time.sleep(2)
                continue
            else:
                return move
        else: # they guessed the phrase
            return move


# *START of GAME LOGIC*
# Start of game setup
header()
inputName = input("PLAYER, Enter your name\n\n").upper()
player = Player(inputName)

#External loop to prompt for difficulty and start game with a word from file 
while True:
    header() # Header of Game
    player = Player(inputName)
    print("Hello {}".format(player.name))
    message = """    
Enter the difficulty you want to play 

[E]asy   1-4 letters
[M]edium 5-8 Letters
[H]ard   9+ Letters

""".format(player.name)
    difficulty = input(message).upper() # Get Difficulty
    
    # Validate Difficulty input
    while difficulty not in ['E','M','H']: 
        header()
        print('Invalid Input')
        difficulty = input(message).upper()
    
    print("\nGetting your word")
    word = GetWord(difficulty) # Get a word from relevent File
    time.sleep(3) # Pause for suspense
    
    # set/reset variables to initial values
    guessed = []
    winner = False
    
    # Start of game level
    header()
    # Entrance message for player
    print("Prisoner {}, time to go".format(player.name))
    time.sleep(2) # for suspense
    print(
"""
You have been sentenced to death by the Galactic Republic of Scrabble

To save yourself from execution you must guess a word for me  

PRESS ANY CLUE TO CONTINUE""")
    input() # Start button for Player
    
    while True:
        header()
        
        move = requestPlayerMove(player, guessed) # Request for a new move
        header()
        if move == 'EXIT': # leave the game
            print('Until next time!')
            break
        elif len(move) == 1: # they guessed a letter
            guessed.append(move)
            guessed.sort()

            print('{} guesses "{}"\n'.format(player.name, move))

            count = word.count(move) # returns an integer with how many times this letter appears
            if count > 0: # Guessed a letter right
                if count == 1:
                    print("There is one {}".format(move))
                else:
                    print("There are {} {}'s".format(count, move))
                
                print(obscureWord(word, guessed))

                # all of the letters have been guessed
                if obscureWord(word, guessed) == word:
                    winner = player
                    break

            elif count == 0: # Guessed the letter wrong
                print("There is no {}".format(move))
                player.incrementStrike()
                # Show the player their current status
                print(player.printTextArt())
                
                if player.strikes == 6: # check if the player has lost all their lives
                    break
                
        else: # they guessed the whole phrase
            if move == word: # they guessed the full phrase correctly
                winner = player
                break
            else:
                print('{} was not the word'.format(move))
                player.incrementStrike() # Wrong guess of word treated at par with wrong letter
                # Show the player their current status
                print(player.printTextArt())
                
                if player.strikes == 6: ## check if the player has lost all their lives
                    break
    
        time.sleep(2) # Suspense after a move and also reading time
    
    if winner:
        # In your head, you should hear this as being announced by a game show host
        print('{} you saved your life! The word was indeed {}'.format(winner.name, word))
    else:
        print('YOU WERE HANGED TO DEATH. The word was {}'.format(word))
    time.sleep(3) # Let player comprehend their loss
    
    header()
    if move == "EXIT":
        break
    choice = input("Do you want to play again (Y/N)\t").upper() # Prompt to play again
    while choice not in ['Y','N']: # choice validation
        print('Invalid Input\n')
        choice = input("Do you want to play again (Y/N)\t").upper()
    if choice == 'N': # Exit if they do not wish to play more
        print("Until next time!")
        break
        
    
        
    
        