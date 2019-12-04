# -*- coding: utf-8 -*-
from cisc106 import *
import time
from tkinter import *

# Project group is Aidan, Dylan, and Denise

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

class Grid:
    """
    Has attributes numRows, numCols, and squares (a 2D list containing True/False).
    """
    def __init__(self, rows, cols, squares):
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
        testing = find_max_score_location(self, shape)
        location = testing[2]
        fits = testing[0]
        numRotations = testing[1]
        while numRotations:
            shape.rotate90()
            numRotations -= 1
        for row in range(len(shape.squares)):
            for col in range(len(shape.squares[0])):
                if shape.squares[row][col] == True:
                    self.squares[location[0] + row][location[1] + col] = True
        self.print()
        return fits
        
    def print(self):
        """
        Print the grid, using an asterisk for each true square, underscore for false.
        Use a newline after each row, and no spaces in rows.
        """
        for element1 in range(self.numRows):
            alist = self.squares[element1]
            for element2 in range(self.numCols):
                if alist[element2]:
                    print('*', end = '\f')
                else:
                    print('_', end = '\f')
            print('\t')
    
class Shape:
    """
    A "shape" is a nested tuple
    For example, an "L" shape could be represented as:
    ((False, False, True), (True, True, True))
    Has attributes x, y, letter, squares (a nested list of type boolean),
    color, num_rotations
    """
    def __init__(self, letter, squares, color):
        self.y = 0
        self.x = 0
        self.letter = letter
        self.squares = squares
        self.color = color
        self.num_rotations = 0
        
    def rotate90(self):
        """
        Rotates this shape 90 degrees clockwise
        Mutates squares and num_rotations
        Returns None
        """
        self.num_rotations = self.num_rotations + 1
        if self.num_rotations == 4:
            self.num_rotations = 0
        column = []
        for x in range(len(self.squares[0])):
            row = []
            for y in range(len(self.squares) - 1, -1, -1):
                row += [self.squares[y][x]]
            column += [row] 
        self.squares = column
    
def generate_all_locations(grid, shape):
    """
    Takes a single shape in one position and finds all the places it could fit on the
    grid, given its dimensions.
    Returns: a list of row, col tuples
    """
    location_list = []
    for x in range(grid.numRows):
        if x + len(shape.squares) <= grid.numRows:
            for y in range(grid.numCols):
                if y + len(shape.squares[0]) <= grid.numCols:
                    location_list = location_list + [(x, y)]
    return location_list
    
def get_valid_locations(location_list, grid, shape):
    """
    Returns list of locations where shape does not overlap shapes
    already on grid. Assumes that all locations in parameter list are
    potential fits for this shape.
    Calls: fits
    """
    validLocations = []
    for location in location_list:
        if fits(location, grid, shape):
            validLocations = validLocations + [location]
    return validLocations

def fits(location, grid, shape):
    """
    Returns True if shape placed at location does not overlap shapes
    already on grid.
    location: row, col tuple
    """
    temporary = []
    for element in range(location[0], location[0] + len(shape.squares)):
        if location[0] + len(shape.squares) > len(grid.squares):
            return False
        elif location[1] + len(shape.squares[0]) > len(grid.squares[element]):
            return False
        temporary += [grid.squares[element][location[1]:location[1] + len(shape.squares[0])]]
    for cols in range(len(temporary[0])):
        for rows in range(len(temporary)):
            if temporary[rows][cols] and shape.squares[rows][cols]:
                return False
    return True
            
def get_max_score(location_list, grid, shape):
    """
    Finds highest scoring location from list, given shape.
    When scores are equal, the lowest row (highest row number), right end (highest
    column) should be preferred.
    Return: nested tuple of (location_tuple, number)
    Calls: get_score
    """
    max_score = 0
    max_score_location = location_list[0]
    for location in location_list:
        if get_score(location, grid, shape) > get_score(max_score_location, grid, shape):
            max_score = get_score(location, grid, shape)
            max_score_location = location
        elif get_score(location, grid, shape) == get_score(max_score_location, grid, shape):
            if location[1] > max_score_location[1]:
                max_score_location = location
                max_score = get_score(location, grid, shape)
            elif location[0] > max_score_location[0]:
                max_score_location = location
                max_score = get_score(location, grid, shape)
    return (max_score_location, max_score)
                                             
def get_score(location, grid, shape):
    """
    Computes the score for a shape placed at a single location on grid.
    Scores are positive, higher is better. For now, code the heuristic discussed in class.
    location: row, col tuple
    Returns: number
    """
    score = 0
    for row in range(len(shape.squares)):
        for col in range(len(shape.squares[0])):
            if (not shape.squares[row][col]) and grid.squares[location[0] + row][location[1] + col]:
                score += 1
    return score
    
def find_max_score_location(grid, shape):
    """
    Takes a single shape, finds best position on grid. Tries original
    and three possible 90 degree rotations. Mutates shape for each rotation.
    When scores are equal, the lowest row (highest row number), right end (highest
    column) should be preferred.
    Returns tuple: (fits, numberRotations, location)
    fits: bool
    maxScoreRow, maxScoreCol: upper left coordinates of best position for shape on grid
    numberRotations: 0-3 rotations required for best fit.
    Calls: rotate90, generate_all_locations, get_valid_locations, get_max_score
    """
    maxScoreLocation = ((0, 0), -1)
    currentScore = ()
    rotations = 0
    while shape.num_rotations < 3:
        currentScore = get_max_score(get_valid_locations(generate_all_locations(grid, shape), grid, shape), grid, shape)
        if maxScoreLocation[1] < currentScore[1]:
            maxScoreLocation = currentScore
            shape.x = maxScoreLocation[0][1]
            shape.y = maxScoreLocation[0][0]
            rotations = shape.num_rotations
            fitting = fits(maxScoreLocation[0], grid, shape)
        elif maxScoreLocation[1] == currentScore[1] and currentScore[0] > maxScoreLocation[0]:
            maxScoreLocation = currentScore
            shape.x = maxScoreLocation[0][1]
            shape.y = maxScoreLocation[0][0]
            rotations = shape.num_rotations
            fitting = fits(maxScoreLocation[0], grid, shape)
        shape.rotate90()
    shape.rotate90()
    return (fitting, rotations, maxScoreLocation[0])
    
def get_shape(letter):
    """
    Returns the Shape corresponding to the letter parameter: I for a line; 
    T for a T; L for an L on its back, foot to right; Z for a Z. More may be added.
    """
    if letter == 'L':
        return Shape('L', ((False, False, True), (True, True, True)), 'Red')
    elif letter == 'T':
        return Shape('T', ((True, True, True), (False, True, False)), 'Blue')
    elif letter == 'Z':
        return Shape('Z', ((True, True, False), (False, True, True)), 'Green')
    elif letter == 'I':
        return Shape('I', ((True, True, True, True),), 'Orange')
    
# Tests for get_shape
assertEqual(get_shape('L').squares, ((False, False, True), (True, True, True)))
assertEqual(get_shape('T').squares, ((True, True, True), (False, True, False)))
assertEqual(get_shape('Z').squares, ((True, True, False), (False, True, True)))
assertEqual(get_shape('I').squares, ((True, True, True, True),))

# Tests for fits
assertEqual(fits((0, 0), Grid(2, 3, [[True, True, False], [False, False, False]]), get_shape('L')), True)
assertEqual(fits((0, 0), Grid(2, 3, [[True, True, True], [True, True, True]]), get_shape('L')), False)
assertEqual(fits((0, 0), Grid(2, 4, []), get_shape('I')), True)
assertEqual(fits((0, 0), Grid(1, 4, []), get_shape('I')), True)
assertEqual(fits((0, 0), Grid(2, 4, [[False, False, False, False], [True, True, True, True]]), get_shape('I')), True)

# Tests for generate_all_locations
assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])
assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('Z')), [(0, 0), (0, 1)])
assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('T')), [(0, 0), (0, 1)])
assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('I')), [(0, 0), (1, 0)])
assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])
assertEqual(generate_all_locations(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), [(0, 0), (0, 1), (1, 0), (1, 1)])
assertEqual(generate_all_locations(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('Z')), [(0, 0), (0, 1), (1, 0), (1, 1)])
assertEqual(generate_all_locations(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('T')), [(0, 0), (0, 1), (1, 0), (1, 1)])
assertEqual(generate_all_locations(Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('I')), [(0, 0), (1, 0), (2, 0)])
assertEqual(generate_all_locations(Grid(2, 6, []), get_shape('L')), [(0, 0), (0, 1), (0, 2), (0, 3)])
assertEqual(generate_all_locations(Grid(2, 6, []), get_shape('Z')), [(0, 0), (0, 1), (0, 2), (0, 3)])
assertEqual(generate_all_locations(Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])

# Tests for get_valid_locations
assertEqual(get_valid_locations([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('Z')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('T')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0), (1, 0)], Grid(2, 4, []), get_shape('I')), [(0, 0), (1, 0)])
assertEqual(get_valid_locations([(0, 0), (0, 1), (1, 0), (1, 1)], Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0), (0, 1), (1, 0), (1, 1)], Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('Z')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0), (0, 1), (1, 0), (1, 1)], Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('T')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0), (1, 0), (2, 0)], Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('I')), [(0, 0), (1, 0)])
assertEqual(get_valid_locations([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)], Grid(4, 6, []), get_shape('L')), [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)])
assertEqual(get_valid_locations([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)], Grid(4, 6, []), get_shape('Z')), [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)])
assertEqual(get_valid_locations([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), [(0, 0), (0, 1)])
assertEqual(get_valid_locations([(0, 0)], Grid(2, 3, [[1, 0, 0], [0, 0, 0]]), get_shape('L')), [(0, 0)])

# Tests for get_max_score
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('Z')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('T')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (1, 0)], Grid(2, 4, []), get_shape('I')), ((1, 0), 0))
assertEqual(get_max_score([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)], Grid(4, 6, []), get_shape('L')), ((2, 3), 0))
assertEqual(get_max_score([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)], Grid(4, 6, []), get_shape('Z')), ((2, 3), 0))
assertEqual(get_max_score([(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (2, 0), (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3)], Grid(4, 6, []), get_shape('T')), ((2, 3), 0))
assertEqual(get_max_score([(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2), (3, 0), (3, 1), (3, 2)], Grid(4, 6, []), get_shape('I')), ((3, 2), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(3, 8, []), get_shape('L')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(3, 8, []), get_shape('Z')), ((0, 1), 0))
assertEqual(get_max_score([(0, 0), (0, 1)], Grid(2, 4, []), get_shape('L')), ((0, 1), 0))

# Tests for find_max_score_location
assertEqual(find_max_score_location(Grid(3, 4, []), get_shape('L')), (True, 0, (1, 1)))
assertEqual(find_max_score_location(Grid(3, 4, []), get_shape('T')), (True, 0, (1, 1)))
assertEqual(find_max_score_location(Grid(3, 4, []), get_shape('Z')), (True, 0, (1, 1)))
assertEqual(find_max_score_location(Grid(4, 4, []), get_shape('I')), (True, 0, (3, 3)))
assertEqual(find_max_score_location(Grid(4, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), (True, 2, (2, 0)))
assertEqual(find_max_score_location(Grid(4, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('T')), (True, 3, (1, 0)))
assertEqual(find_max_score_location(Grid(4, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('Z')), (True, 1, (1, 0)))
assertEqual(find_max_score_location(Grid(4, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('I')), (True, 1, (2, 0)))
assertEqual(find_max_score_location(Grid(4, 6, []), get_shape('L')), (True, 0, (2, 3)))
assertEqual(find_max_score_location(Grid(4, 6, []), get_shape('T')), (True, 0, (2, 3)))
assertEqual(find_max_score_location(Grid(3, 4, [[True, False, False, False], [False, False, False, False], [False, False, False, False]]), get_shape('L')), (True, 0, (0, 1))) 
assertEqual(find_max_score_location(Grid(3, 4, []), get_shape('L')), (True, 0, (0, 1)))

# Tests for get_score
assertEqual(get_score((0, 0), Grid(2, 4, []), get_shape('L')), 0)
assertEqual(get_score((0, 0), Grid(2, 4, []), get_shape('Z')), 0)
assertEqual(get_score((0, 0), Grid(2, 4, []), get_shape('T')), 0)
assertEqual(get_score((0, 0), Grid(2, 4, []), get_shape('I')), 0)
assertEqual(get_score((0, 1), Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), 0)
assertEqual(get_score((0, 1), Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('Z')), 0)
assertEqual(get_score((0, 1), Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('T')), 0)
assertEqual(get_score((0, 1), Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('I')), 0)
assertEqual(get_score((0, 0), Grid(2, 6, []), get_shape('L')), 0)
assertEqual(get_score((0, 0), Grid(2, 6, []), get_shape('Z')), 0)
assertEqual(get_score((0, 0), Grid(2, 3, [[True, True, False], [False, False, False]]), get_shape('L')), 2)
assertEqual(get_score((0, 0), Grid(2, 3, [[True, True, False], [False, False, False]]), get_shape('L')), 2)

# Tests for rotate90
a_Shape = Shape('L',[[False, False, True], [True, True, True]], 0)
a_Shape.rotate90()
assertEqual(a_Shape.squares, [[True, False], [True, False], [True, True]])
a_Shape.rotate90()
assertEqual(a_Shape.squares, [[True, True, True], [True, False, False]])
a_Shape.rotate90()
assertEqual(a_Shape.squares, [[True, True], [False, True], [False, True]])

b_Shape = Shape('I', [[True, True, True, True],], 0)
b_Shape.rotate90()
assertEqual(b_Shape.squares, [[True], [True], [True], [True]])
b_Shape.rotate90()
assertEqual(b_Shape.squares, [[True, True, True, True],])

c_Shape = Shape('Z', [[True, True, False], [False, True, True]], 0)
c_Shape.rotate90()
assertEqual(c_Shape.squares, [[False, True], [True, True], [True, False]])
c_Shape.rotate90()
assertEqual(c_Shape.squares, [[True, True, False], [False, True, True]])

d_Shape = Shape('T', [[True, True, True], [False, True, False]], 0)
d_Shape.rotate90()
assertEqual(d_Shape.squares, [[False, True], [True, True], [False, True]])
d_Shape.rotate90()
assertEqual(d_Shape.squares, [[False, True, False], [True, True, True]])
d_Shape.rotate90()
assertEqual(d_Shape.squares, [[True, False], [True, True], [True, False]])

# Tests for updateGrid
#a_Grid = Grid(2, 4, [])
#a_Grid.updateGrid([[False, False, True], [True, True, True]])
#assertEqual(a_Grid.squares,[[False, False, True, False], [True, True, True, False]])
#assertEqual(a_Grid.updateGrid([[False, False, True], [True, True, True]]), True)

#b_Grid = Grid(2, 4, [[False, False, False, False], [True, True, True, True]])
#b_Grid.updateGrid([[True, True, True, True]])
#assertEqual(b_Grid.squares, [[True, True, True, True], [True, True, True, True]])
#assertEqual(b_Grid.updateGrid([[True, True, True, True]]), True)

#c_Grid = Grid(2, 4, [[True, True, True, True], [True, True, True, True]])
#c_Grid.updateGrid([[True, True, False], [False, True, True]])
#assertEqual(c_Grid.squares, [[True, True, True, True], [True, True, True, True]])
#assertEqual(c_Grid.updateGrid([[True, True, False], [False, True, True]]), False)

#d_Grid = Grid(2, 4, [[True, True, False, True], [False, False, True, True]])
#d_Grid.updateGrid([[True, True, True], [False, True, False]])
#assertEqual(d_Grid.squares, [[True, True, False, True], [False, False, True, True]])
#assertEqual(d_Grid.updateGrid([[True, True, True], [False, True, False]]), False)
