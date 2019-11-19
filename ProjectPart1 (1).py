# -*- coding: utf-8 -*-
from cisc106 import *
import time
from tkinter import *

#Working with Denise and Dylan, my name is Aidan

DEBUG = True

# A grid is a 2D list containing ones or zeros. A "shape" is an
# object containing a nested tuple, where the real world shape is
# represented as True values. For example, an "L" shape could be represented as

# ((False, False, True),(True, True, True))

# Read a sequence of letters from a string (later from a text
# file). Each letter represents a shape: T, L, or Z (all 2x3), or I
# (1x4). Use functions to find a place on the grid where
# the next shape in the sequence doesn’t overlap any ones. Rotate the
# shape to find the "best" fit. Then modify the grid to show the
# shape in place, and repeat with the next shape in the sequence.
# We will add the graphics and high level functions in the next part.

# 2 low level
# 4 high level
# 3 constructors

class Grid:
    """
    Has attributes numRows, numCols, and squares (a 2D list containing True/False).
    """
    def __init__(self,rows,cols,squares):
        self.numRows = rows
        self.numCols = cols
        self.squares = squares if squares else [cols * [False] for r in range(rows)]
        
    def updateGrid(self, shape):
        """
        Top-level def for placing a single shape on grid. Finds best
        position and rotation for shape, update grid squares (mutates).
        Calls: find_max_score_location
        Returns boolean: fits or not
        """
        
    def print(self):
        """
        Print the grid, using an asterisk for each true square, underscore for false.
        Use a newline after each row, and no spaces in rows.
        """
        print(self.squares)
    
def transpose(shape):
    result = [len(shape.squares) * [False] for r in range(len(shape.squares[0]))]
    for i in range(len(shape.squares)):
        for j in range(len(shape.squares[0])):
            result[j][i] = shape.squares[i][j]
    return result
    
class Shape:
    """
    A "shape" is a nested tuple, where the real world shape is
    represented as ones. For example, an "L" shape could be represented as
    ((False, False, True),(True, True, True))
    Has attributes x, y, letter, squares (a nested list of type boolean),
    color, num_rotations
    """
    
    def __init__(self, letter, squares, color):
        self.x = 0 # will be modified later to indicate position
        self.y = 0 # will be modified later to indicate position
        self.letter = letter
        self.squares = squares
        self.color = color
        self.num_rotations = 0
        
    def rotate90(self):
        """
        Rotates this shape 90 degrees clockwise (direction
        matters). Mutates squares and num_rotations
        Returns None
        """
        initial = transpose(self)
        for i in range(len(initial)):
            initial[i] = initial[i][::-1]
        self.squares = initial
        self.num_rotations += 1
        return None
    
def generate_all_locations(grid, shape):
    """
    Takes a single shape in one position and finds all the places it could fit on the
    grid, given its dimensions.
    Returns: a list of row,col tuples
    """
    location_list = []
    rows = grid.numRows
    cols = grid.numCols
    for rows1 in range(grid.numRows):
        for cols1 in range(grid.numCols):
            if len(shape.squares[0]) <= (cols- cols1):
                if len(shape.squares) <= (rows - rows1):
                    location_list += [(rows1, cols1)]           
    return location_list
    
def get_valid_locations(location_list, grid, shape):
    """
    Returns list of locations where shape does not overlap shapes
    already on grid. Assumes that all locations in parameter list are
    potential fits for this shape.
    Calls: fits
    """
    valid = []
    for element in range(len(location_list)):
        if fits(location_list[0], grid, shape):
            valid += [(location_list[0])]
        location_list = location_list[1:]
    return valid
    
def fits(location, grid, shape):
    """
    Returns True if shape placed at location does not overlap shapes
    already on grid.
    location: row,col tuple
    """
    temp = []
    testing = True
    for element1 in range(len(shape.squares) - 1):
        for element2 in range(len(shape.squares[0]) - 1):
            if shape.squares[element1][element2] != grid.squares[location[0] + element1][location[1] + element2]:
                temp += [True]
            else:
                temp += [False]
    for element in temp:
        if False:
            return False
            testing = False
    if testing:
        return True
            
def get_max_score(location_list, grid, shape):
    """
    Finds highest scoring location from list, given shape.
    When scores are equal, the lowest row (highest row number), right end (highest
    column) should be preferred.
    Return: nested tuple of (location_tuple,number)
    Calls: get_score
    """
    max_score = 0
    max_score_location = location_list[0]
    for location in location_list:
        if get_score(location, grid, shape) > get_score(max_score_location, grid, shape):
            max_score = get_score(location, grid, shape)
            max_score_location = (location)
        if get_score(location, grid, shape) == get_score(max_score_location, grid, shape):
            if location[1] > max_score_location[1]:
                max_score_location = location
            if location[0] > max_score_location[0]:
                max_score_location = location
                max_score = get_score(location, grid, shape)
    return ((max_score_location), max_score)
                                             
def get_score(location, grid, shape):
    """
    Computes the score for a shape placed at a single location on grid.
    Scores are positive, higher is better. For now, code the heuristic discussed in class.
    location: row,col tuple
    Returns: number
    """
    score = 0
    for rowIndex in range(len(shape.squares) - 1):
        row = rowIndex + location[0]
        for colIndex in range(len(shape.squares[0]) - 1):
            col = colIndex + location[1]
            if bool(shape.squares[rowIndex][colIndex]) == False:
                if bool(grid.squares[row][col]) == True:
                    score += 1
    return score
    
def find_max_score_location(grid, shape):
    """
    Takes a single shape, finds best position on grid. Tries original
    and three possible 90 degree rotations. Mutates shape for each rotation.
    When scores are equal, the lowest row (highest row number), right end (highest
    column) should be preferred.
    Returns tuple: (fits numberRotations location)
    fits: bool
    maxScoreRow, maxScoreCol: upper left coordinates of best position for shape on grid
    numberRotations: 0-3 rotations required for best fit.
    Calls: rotate90, generate_all_locations, get_valid_locations, get_max_score
    """
    location_list = generate_all_locations(grid, shape)
    get_valid_locations(location_list, grid, shape)
    if not location_list:
        return False
    else:
        fitting = True
        savedScore = 0
        currentRotated = 0
        bestLocation = (0,0)
        bestRotated = 0
        for element in range(4):
            currentScore = get_max_score(location_list, grid, shape)[1]
            currentLocation = get_max_score(location_list, grid, shape)[0]
            maxScoreRow = get_max_score(location_list, grid, shape)[0][0]
            maxScoreCol = get_max_score(location_list, grid, shape)[0][1]
            if currentScore > savedScore:
                bestRotated = currentRotated
                bestLocation = currentLocation
                savedScore = currentScore
                shape.x = maxScoreCol
                shape.y = maxScoreRow
            elif currentScore == savedScore:
                if currentRotated < bestRotated:
                    bestRotated = currentRotated
                    bestLocation = currentLocation
                    shape.x = maxScoreCol
                    shape.y = maxScoreRow
                elif currentRotated == bestRotated:
                    bestLocation = currentLocation
                    shape.x = maxScoreCol
                    shape.y = maxScoreRow
            shape.rotate90()
            currentRotated += 1
        return (fitting, bestRotated, bestLocation)

    
def get_shape(letter):
    """
    Returns the Shape corresponding to the letter parameter: I for a line; 
    T for a T; L for an L on its back, foot to right; Z for a Z. More may be added.
    """
    if letter == 'L':
        return Shape('L', ((False, False, True), (True, True, True)), 0)
    elif letter == 'T':
        return Shape('T', ((True, True, True), (False, True, False)), 0)
    elif letter == 'Z':
        return Shape('Z', ((True, True, False), (False, True, True)), 0)
    elif letter == 'I':
        return Shape('I', ((False, False, False, False), (True, True, True, True)), 0)
"""
assertEqual(get_shape('L'),((False, False, True), (True, True, True)))
assertEqual(get_shape('T'),((True, True, True), (False, True, False)))
assertEqual(get_shape('Z'),('Z',((True, True, False), (False, True, True)), 0))
assertEqual(get_shape('I'), ((True, True, True, True)))
"""
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('Z')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('T')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('I')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(4, 6, []), get_shape('L')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(4, 6, []), get_shape('Z')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(4, 6, []), get_shape('T')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(4, 6, []), get_shape('I')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(3, 8, []), get_shape('L')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(3, 8, []), get_shape('Z')), ((0, 1), 0))
  
assertEqual(find_max_score_location(Grid(2, 4, []), get_shape('L')), (True, 0, (0, 1)))
assertEqual(find_max_score_location(Grid(2, 4, []), get_shape('T')), (True, 0, (0, 1)))
assertEqual(find_max_score_location(Grid(2, 4, []), get_shape('Z')), (True, 0, (0, 1)))
assertEqual(find_max_score_location(Grid(2, 4, []), get_shape('I')), (True, 0, (0, 1)))
assertEqual(find_max_score_location(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), (True, 3, (1, 1)))
assertEqual(find_max_score_location(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('T')), (True, 0, (1, 1)))
assertEqual(find_max_score_location(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('Z')), (True, 0, (1, 1)))
assertEqual(find_max_score_location(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('I')), (True, 2, (1, 0)))

g = Grid(2, 4, [[True, False, False, False], [False, False, False, False]])
assertEqual(find_max_score_location( g, get_shape('L')), (True, 0, (0, 0))) 

if DEBUG:
    assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])
    assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), ((0, 1), 0))
    assertEqual(get_valid_locations([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])
    b = [[1, 0, 0],[0, 0, 0]]
    assertEqual(get_valid_locations([(0, 0)], Grid(2, 3, b), get_shape('L')), [(0, 0)])
    assertEqual(find_max_score_location(Grid(2, 4, []), get_shape('L')), (True, 0, (0, 1)))
    assertEqual(find_max_score_location(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), (True, 2, (1, 0)))
    g = Grid(2, 4, [[True, False, False, False], [False, False, False, False]])
    assertEqual(find_max_score_location( g, get_shape('L')), (True, 0, (0, 0)))
    g.print()
