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
        testing=find_max_score_location(self,shape)
        location=testing[2]
        fits=testing[0]
        numRotations=testing[1]
        for rotations in range(numRotations):
            shape.rotate90
        for row in range(len(shape.squares)):
            for col in range(len(shape.squares[0])):
                if shape.squares[row][col]==True:
                    self.squres[location[0]+row][location[1]+col]
        self.print()
        return fits
        
    def print(self):
        """
        Print the grid, using an asterisk for each true square, underscore for false.
        Use a newline after each row, and no spaces in rows.
        """
        for elt1 in range(self.numRows):
            alist=self.squares[elt1]
            for elt2 in range(self.numCols):
                if alist[elt2]:
                    print('*',end='\f')
                else:
                    print('_',end='\f')
            print('\t')
    
def transpose(shape):
    result = [len(shape.squares) * [False] for r in range(len(shape.squares[0]))]
    for i in range(len(shape.squares)):
        for j in range(len(shape.squares[0])):
            result[j][i] = shape.squares[i][j]
    return result
    
class Shape:
    """
    A "shape" is a nested tuple
    For example, an "L" shape could be represented as:
    ((False, False, True),(True, True, True))
    Has attributes x, y, letter, squares (a nested list of type boolean),
    color, num_rotations
    """
    
    def __init__(self, letter, squares, color):
        self.x = 0
        self.y = 0
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
        self.num_rotations = 0
        initial = transpose(self)
        for i in range(len(initial)):
            initial[i] = initial[i][::-1]
        self.squares = initial
        self.num_rotations += 1
        self.num_rotations = self.num_rotations % 4
        return None
    
def generate_all_locations(grid, shape):
    """
    Takes a single shape in one position and finds all the places it could fit on the
    grid, given its dimensions.
    Returns: a list of row,col tuples
    """
    location_list = []
    for rows in range(grid.numRows):
        for cols in range(grid.numCols):
            if rows + len(shape.squares) <= grid.numRows:
                if cols + len(shape.squares[0]) <= grid.numCols:
                    location_list += [(rows, cols)]
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
        else:
            location_list = location_list[1:]
    return valid
    
def fits(location, grid, shape):
    """
    Returns True if shape placed at location does not overlap shapes
    already on grid.
    location: row,col tuple
    """
    tempSpace = []
    for element in range(location[0], location[0] + len(shape.squares)):
        if location[0] + len(shape.squares) > len(grid.squares):
            return False
        elif location[1] + len(shape.squares[0]) > len(grid.squares[element]):
            return False
        tempSpace += [grid.squares[element][location[1]:location[1] + len(shape.squares[0])]]
    for cols in range(len(tempSpace[0])):
        for rows in range(len(tempSpace)):
            if tempSpace[rows][cols] and shape.squares[rows][cols]:
                return False
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
    for row in range(len(shape.squares)):
        for col in range(len(shape.squares[0])):
            if shape.squares[row][col] == False:
                if grid.squares[location[0] + row][location[1] + col] == True:
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
    if not location_list:
        return False
    else:
        fitting = True
        savedScore = 0
        currentRotated = 0
        bestLocation = (0,0)
        bestRotated = 0
        for element in [1, 2, 3, 4]:
            location_list = get_valid_locations(location_list, grid, shape)
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
                elif currentRotated > bestRotated:
                    bestRotated = bestRotated
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
        return Shape('I', ((True, True, True, True),), 0)

# Tests for get_shape
assertEqual(get_shape('L'), Shape('L', ((False, False, True), (True, True, True)), 0))
assertEqual(get_shape('T'), Shape('T', ((True, True, True), (False, True, False)), 0))
assertEqual(get_shape('Z'), Shape('Z', ((True, True, False), (False, True, True)), 0))
assertEqual(get_shape('I'), Shape('I', ((False, False, False, False), (True, True, True, True)), 0))

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
assertEqual(get_score((0,0),Grid(2, 4, []), get_shape('L')), 0)
assertEqual(get_score((0,0),Grid(2, 4, []), get_shape('Z')), 0)
assertEqual(get_score((0,0),Grid(2, 4, []), get_shape('T')), 0)
assertEqual(get_score((0,0),Grid(2, 4, []), get_shape('I')), 0)
assertEqual(get_score((0,1),Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('L')), 0)
assertEqual(get_score((0,1),Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('Z')), 0)
assertEqual(get_score((0,1),Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('T')), 0)
assertEqual(get_score((0,1),Grid(3, 4, [[0, 0, 0, 0], [0, 0, 0, 0], [0, 1, 1, 1]]), get_shape('I')), 0)
assertEqual(get_score((0,0),Grid(2, 6, []), get_shape('L')), 0)
assertEqual(get_score((0,0),Grid(2, 6, []), get_shape('Z')), 0)
assertEqual(get_score((0, 0), Grid(2, 3, [[True, True, False], [False, False, False]]), get_shape('L')), 2)
assertEqual(get_score((0, 0), Grid(2, 3, [[True, True, False], [False, False, False]]), get_shape('L')), 2)

#Tests for rotate90
a_Shape=Shape('L',[[False,False,True],[True,True,True]],0)
a_Shape.rotate90()
assertEqual(a_Shape.squares,[[True,False],[True,False],[True,True]])
a_Shape.rotate90()
assertEqual(a_Shape.squares,[[True,True,True],[True,False,False]])
a_Shape.rotate90()
assertEqual(a_Shape.squares,[[True,True],[False,True],[False,True]])

b_Shape=Shape('I',[[True,True,True,True]],0)
b_Shape.rotate90()
assertEqual(b_Shape.squares,[[True],[True],[True],[True]])
b_Shape.rotate90()
assertEqual(b_Shape.squares,[[True,True,True,True]])

c_Shape=Shape('Z',[[True,True,False],[False,True,True]],0)
c_Shape.rotate90()
assertEqual(c_Shape.squares,[[False,True],[True,True],[True,False]])
c_Shape.rotate90()
assertEqual(c_Shape.squares,[[True,True,False],[False,True,True]])

d_Shape=Shape('T',[[True,True,True],[False,True,False]],0)
d_Shape.rotate90()
assertEqual(d_Shape.squares,[[False,True],[True,True],[False,True]])
d_Shape.rotate90()
assertEqual(d_Shape.squares,[[False,True,False],[True,True,True]])
d_Shape.rotate90()
assertEqual(d_Shape.squares,[[True,False],[True,True],[True,False]])