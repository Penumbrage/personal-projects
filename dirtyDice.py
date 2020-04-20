# Name: William Wang
# ID: 108980353
# Course: CSCI 1320
# Section: 112
# Assignment 9
# Description: This program is a game called Dirty Dice that has one user/player play
# against a computer in a dice game. This game prompts to user for an objective score between
# 100 (noninclusive) and 200, and then has them play the game to obtain that score.
# The user or computer will roll a die until a three is rolled or the player chooses to
# hold their current die total, which will then be subtracted from the opposing player's score.
# The program will display the winner at the end of the game

"""
In C++, the general outline for how this program ran:
1) The main function ran all of the other functions in a step by step fashion
2) Ask the user for inputs on their desired point value to play to (verify that the score is viable for the rules above)
3) Runs a loopGame() function that loops through the game rules and returns a boolean value with the winner of the game (prints the winner to the screen)
    Much of the meat on how the game actually functions is withinthe loopGame() function and the functions that loopGame() uses
4) The primary functions that operate witin the original C++ code were loopGame() (maintains the game), oneTurn()
(which I think simulates one turn for a player or the computer and returns the results to the game), and roll()
(which simulates rolling a die)
5) I think the main classes I can make to sort of simulate what this game would be like in real life:
    A class for the game itself (this class would include the loopGame and the oneTurn() functions maybe)
    A class for the players (to keep track who's playing and their point values)
    A class for the die to simulate the random numbers that you would get if you were actually rolling a die
"""

from random import seed
from random import randint
import time

# Let's start with making the dice class 
class Dice(object):

    # Initializer / Instance Attributes
    def __init__(self):
        seed(time.time())

    # roll the dice function
    def roll(self):
        self.rolledNum = randint(1,6)
        return self.rolledNum



# Now, let's make classes that define the user and the computer that the user is playing against

# Player (parent class)
class Players(object):

    # Initializer / Instance Attributes the player will have
    def __init__(self):
        self.pointTotal = 100   # point total initially held by the players

    # Gives the user a die
    def getDie(self, die):
        self.die = die



# Child class for the user
class User(Players):

    # Method where the player with play his/her turn for the game (will return the point value at the end)
    def playerTurn(self):
        self.myTurn = True
        self.turnTotal = 0

        while self.myTurn == True:
            self.dec = int(input("Would you like to roll the die or hold your hand (Enter 1 for roll and 2 for hold): "))

            # Check if the roll is correct or not
            self.correctRoll = False
            while self.correctRoll == False:
                if (self.dec != 1) and (self.dec != 2):
                    self.dec = int(input("Please enter a valid response: "))
                else:
                    self.correctRoll = True
            
            # this is the scenario if the player has chosen to roll
            if self.dec == 1:
                self.currentRoll = self.die.roll() # we have rolled the die

                # if we roll a three, our turn total is automatically over and we only get three points this turn
                if self.currentRoll == 3:
                    self.turnTotal = 3
                    print("\nYou have rolled a three this turn/round, and this is your round total.\n")
                    self.myTurn = False

                # update the turn total with what we rolled and let the user know their current standings
                else:
                    self.turnTotal += self.currentRoll
                    print("\nCurrent roll: {}".format(self.currentRoll))
                    print("Current running total for this turn: {} \n".format(self.turnTotal))
                
            # the player has chosen to end their turn    
            else:
                print("\nYou have chosen to end your turn this round. This is your round-ending total: {}\n".format(self.turnTotal))
                self.myTurn = False
        
        # updates player current point standing
        self.pointTotal += self.turnTotal

        return self.turnTotal



# Child class for the computer
class Computer(Players):
    
    # Initializer to seed the random function used for the die
    def __init__(self):
        seed(time.time())
        super().__init__()

    # Method where the computer will play its turn this game (the computer will default play 3 turns, then will make "random" decisions using a randomizer)
    def computerTurn(self):
        self.noThree = True
        self.threeTurns = 0
        self.turnTotal = 0
        self.compTurn = True

        # Computer plays three turns automatically, as long as it does not roll a three
        while (self.noThree == True) and (self.threeTurns < 3):
            print("The computer has chosen to roll.")
            self.currentRoll = self.die.roll()

            # Checks if the computer plays a three in the initial three turns
            if (self.currentRoll == 3):
                self.turnTotal = 3
                print("The computer has rolled a three, and that is its score this turn.\n")
                # print(self.turnTotal)
                self.noThree = False # stops this while loop
                self.compTurn = False # prevents the random decision making that's coming up
            else:
                self.turnTotal += self.currentRoll
                print("The computer has rolled a: {}".format(self.currentRoll))
                print("The computer's running total this turn is: {} \n".format(self.turnTotal))
                self.threeTurns += 1
                # print(self.currentRoll, self.turnTotal)

        # This code demonstrates the "random" decisions the computer will make w.r.t. to rolling the die
        while self.compTurn == True:

            # Computer will "choose" to roll using this random function
            if (randint(0, 9) % 2) == 0:
                print("The computer has chosen to roll.")
                self.currentRoll = self.die.roll()
            
            # Checks if the computer has rolled a three, if not, add the current roll to the total sum
                if (self.currentRoll == 3):
                    self.turnTotal = 3
                    print("The computer has rolled a three, and that is its score this turn.\n")
                    self.compTurn = False # stops the computer's turn
                else:
                    self.turnTotal += self.currentRoll
                    print("The computer has rolled a: {}".format(self.currentRoll))
                    print("The computer's running total this turn is: {} \n".format(self.turnTotal))

            # Computer has "chosen" to end its turn
            else:
                print("The computer has decided to end its turn with a round-ending total of: {}\n".format(self.turnTotal))
                self.compTurn = False

        # Updates the computer's points
        self.pointTotal += self.turnTotal

        return self.turnTotal



# Let us make the game (where the two players interact and play the game according to some additional rules) class
class GameArena(object):
    
    # Initializer to obtain both players when this object is created
    def __init__(self, user, computer):
        seed(time.time())
        self.user = user
        self.computer = computer

    # Instance method that obtains the game objective score / verifies the score is within the correct range
    def desiredScore(self):
        self.viableScore = False

        #  Asks the user for a score to play to 
        self.desScore = int(input("Please enter an integer score greater than 100 and less than or equal to 200 to play to: "))

        # Checks the score
        while self.viableScore == False:
            if self.desScore <= 100 or self.desScore > 200:
                self.desScore = int(input("\nThe score you entered is not within the correct range. Please enter a number that is greater than 100 and less than or equal to 200: "))
            else:
                self.viableScore = True

    # Instance method that will actually conduct the game between the user and the computer
    def playGame(self):
        self.noWinner = True
        self.playerTurn = False

        # Determines who starts first in this game
        if (randint(0, 9) % 2) == 0:
            self.playerTurn = True
            print("\nYou have been randomly chosen to start first!\n")
        else:
            self.playerTurn = False
            print("\nThe computer has been randomly chosen to start first ...\n")

        # While loop to keep the game running until a winner is determined
        while self.noWinner == True:
            
            # This is the user's turn
            if self.playerTurn == True:
                self.turnPoints = self.user.playerTurn() # the User class will have automatically updated the user's score
                self.computer.pointTotal -= self.turnPoints # update computer score
                print("You have stolen {} points from the computer.".format(self.turnPoints))
                print("Your current score: {} \nThe computer's current score: {}\n\n".format(self.user.pointTotal, self.computer.pointTotal))
                self.playerTurn = False # switches player to computer

            # This is the computer's turn
            else:
                self.turnPoints = self.computer.computerTurn() # Computer class also updates computer's points
                self.user.pointTotal -= self.turnPoints # update user score
                print("The computer has stolen {} points from you.".format(self.turnPoints))
                print("Your current score: {} \nThe computer's current score: {}\n\n".format(self.user.pointTotal, self.computer.pointTotal))
                self.playerTurn = True # swtiches player to user

            # Checks after each player's turn to see if we reached the threshold score
            if self.user.pointTotal >= self.desScore:
                print("You are the winner and have defeated the computer!\n\n")
                self.noWinner = False
            elif self.computer.pointTotal >= self.desScore:
                print("The computer has defeated you... Try again.\n\n")
                self.noWinner = False
            else:
                pass

        
# Create the die object
myBeautifulDie = Dice()

# Create the user object and give the user a die
me = User()
me.getDie(myBeautifulDie)

# Create the computer object and give the computer a die
compJoe = Computer()
compJoe.getDie(myBeautifulDie)

# Create the game object and insert the computer and the user into the game
battle = GameArena(me, compJoe)

# Prompt the user for an objective score
battle.desiredScore()

# Play the game
battle.playGame()