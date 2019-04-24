"""
Write a module docstring here
"""

__author__ = "Eric Gu"

import sys
import os
from collections import defaultdict

def pacman(input_file):
    """ Use this function to format your input/output arguments. Be sure not to change the order of the output arguments.
    Remember that code organization is very important to us, so we encourage the use of helper fuctions and classes as you see fit.

    Input:
        1. input_file (String) = contains the name of a text file you need to read that is in the same directory, includes the ".txt" extension
           (ie. "input.txt")
    Outputs:
        1. final_pos_x (int) = final x location of Pacman
        2. final_pos_y (int) = final y location of Pacman
        3. coins_collected (int) = the number of coins that have been collected by Pacman across all movements
    """

    if not os.path.isfile(input_file):
        print("File path {} does not exist. Exiting...".format(input_file))
        sys.exit()

    with open(input_file, "r") as fp:
        # dictionaries for O(1) lookup time
        walls = defaultdict(int)
        visited = defaultdict(int)
        coinsCollected = 0

        # read input
        # assume input will always follow given template
        for index, line in enumerate(fp):
            if index == 0:
                row = line.split()
                dimensions = (int(row[0]), int(row[1]))
            if index == 1:
                row = line.split()
                currPosX, currPosY = int(row[0]), int(row[1])
            if index == 2:
                movements = line.strip('\n')
            if index >= 3:
                row = line.split()
                wall = (int(row[0]), int(row[1]))
                walls[wall] = 1

        # sanity check inputs
        if (dimensions[0] < 1 or dimensions [1] < 1 or 
            currPosX < 0 or currPosX >= dimensions[0] or
            currPosY < 0 or currPosY >= dimensions[1]):
            return (-1, -1, 0)

        # no coin at Pacman's starting location
        visited[(currPosX, currPosY)] = 1

        # calculate movements
        for move in movements:
            newX, newY = currPosX, currPosY
            if move == 'N':
                newY += 1
            elif move == 'E':
                newX += 1
            elif move == 'S':
                newY -= 1
            elif move == 'W':
                newX -= 1

            newLocation = (newX, newY)

            # check if Pacman moves
            if checkMovement(dimensions, walls, newLocation):
                # update position
                currPosX, currPosY = newX, newY

            # update coins if visiting new square
            currPosition = (currPosX, currPosY)
            if visited[currPosition] == 0:
                coinsCollected += 1
            visited[currPosition] += 1

        return currPosX, currPosY, coinsCollected

def checkMovement(dimensions, walls, newLocation):
    """ Pass in dimensions of the Pacman board, a list of impassable walls, and the proposed new location Pacman wants to move to.
    Returns true if Pacman can move there, false otherwise.

    Input:
        1. dimensions (tuple) = (X, Y) dimensions of the board
        2. walls {(tuple): (int)} = dict of walls within the board
        3. newLocation (tuple) = (x, y) location that Pacman is trying to move to
    Output:
        1. canMove (boolean) = returns true if Pacman can move to new location, false otherwise.
    """

    newX, newY = newLocation[0], newLocation[1]

    if newX < 0 or newX >= dimensions[0] or newY < 0 or newY >= dimensions[1]:
        return False

    if walls[newLocation] != 0:
        return False

    return True