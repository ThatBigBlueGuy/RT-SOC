# usage: RT-SOC.py [-h] p d mp s sp

# Real Time Catan, CMD Line Version

# positional arguments:
#   p           The period of time, in seconds, a turn will last at the beginning of the game
#   d           The amount the period of time, in seconds, a turn decreases by per turn
#   mp          The minimum amount of time a turn can last
#   s           Seasons are enabled
#   sp          The number of turns a season lasts

# optional arguments:
#   -h, --help  show this help message and exit

import dice
import argparse
import time
import os
import pprint as pp

# Global Variables
SEASONS_NAMES = ['Summer, +1 Wheat', 'Fall, +1 Timber', 'Winter, +1 Rock', 'Spring, +1 Sheep']
NUMBER_OF_SEASONS = len(SEASONS_NAMES)

# Main Game Loop
def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Real Time Catan, CMD Line Version')
    parser.add_argument('turnPeriod', metavar='p', type=float, nargs=1, 
        help='The period of time, in seconds, a turn will last at the beginning of the game')
    parser.add_argument('turnPerDecay', metavar='d', type=float, nargs=1,
        help='The amount the period of time, in seconds, a turn decreases by per turn')
    parser.add_argument('minTurnPeriod', metavar='mp', type=float, nargs=1,
        help='The minimum amount of time a turn can last')
    parser.add_argument('seasonsOn', metavar='s', type=bool, nargs=1,
        help='Seasons are enabled')
    parser.add_argument('seasonPeriod', metavar='sp', type=int, nargs=1,
        help='The number of turns a season lasts')

    args = parser.parse_args()

    # Initialize the state machine and the display object
    sm = state()
    disp = cmdDisplay()

    sm.turnPeriod = args.turnPeriod[0]
    sm.turnPerDecay = args.turnPerDecay[0]
    sm.minTurnPeriod = args.minTurnPeriod[0]
    sm.seasonsOn = args.seasonsOn[0]
    sm.seasonPeriod = args.seasonPeriod[0]

    sm.start()

    # Update the state machine, and display on a loop
    while(True):
        sm.update()
        disp.update(sm)

class state:
    def __init__(self):
        self.turnNumber = 0
        self.turnPeriod = 100.0
        self.turnPerDecay = 1.0
        self.minTurnPeriod = 10

        self.seasonsOn = True
        self.seasonPeriod = 10

        self.diceRoll = self._rollDice()
        self.turnBegan = 0.0
        self.turnEnds = 0.0
        self.season = 0 # Summer, Fall, Winter, Spring
    
    # start(self)
    # Starts the game
    def start(self):
        self.turnNumber = 0
        self.turnEnds = time.time()
        self.turnPeriod = self.turnPeriod + self.turnPerDecay
        self._nextTurn()

    # update(self)
    # Checks if the state machine needs to be updated, then updates it
    def update(self):
        currTime = time.time()
        if (currTime - self.turnBegan) > self.turnPeriod:
            self._nextTurn()

    def getTimeLeftInTurn(self):
        return self.turnEnds - time.time()

    # _nextTurn(self)
    # Updates the state machine to reflect the values of the next turn
    def _nextTurn(self):
        self.turnNumber = self.turnNumber + 1
        self.season = int(self.turnNumber / self.seasonPeriod) % NUMBER_OF_SEASONS

        self.turnPeriod = self.turnPeriod - self.turnPerDecay
        if (self.turnPeriod < self.minTurnPeriod):
            self.turnPeriod = self.minTurnPeriod

        self.turnBegan = self.turnEnds
        self.turnEnds = self.turnBegan + self.turnPeriod
        
        self.diceRoll = self._rollDice()

    def _rollDice(self):
        return dice.roll('2d6')


class cmdDisplay:
    def __init__(self):
        pass

    def update(self, sm):
        os.system('cls')
        print("Dice Roll is " + str(sm.diceRoll) + " = " + str(sum(sm.diceRoll)))
        print("Turn #: " + str(sm.turnNumber))
        print("Turn Period: " + str(sm.turnPeriod))
        if sm.seasonsOn:
            print("Season: " + SEASONS_NAMES[sm.season])

        print("")
        print("Time Left: " + str(sm.getTimeLeftInTurn()))

        time.sleep(0.005)
    
if __name__ == '__main__':
    #start_time = time.time()
    main()
    #print("%s seconds" % (time.time() - start_time))
