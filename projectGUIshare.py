from project_1 import *

import tkinter as tk

# Group is Aidan, Dylan, and Denise

class PackingSimulation():
    """
    Is a visible frame on which to display shapes. Has attributes scale
    (number of pixels per square side), rows, cols, and shapes (a list
    of shape letters that need to be placed).
    """
    def __init__(self, rows, cols, shapes_list, master):
        self.master = master
        self.rows = rows
        self.cols = cols
        self.shapes = shapes_list
        self.scale = 20
        self.canvas = Canvas(master, width= cols * self.scale, height= rows * self.scale)
        self.canvas.pack()

    def draw_square(self, x, y, color):
        """
        Draws one square onto the existing game figure. Be careful mapping
        row and col onto x and y. Calls canvas.create_rectangle
        """
        return self.canvas.create_rectangle(x*self.scale, y*self.scale, \
                                     (x + 1) * self.scale, (y + 1) * self.scale, fill = color)
        
        
    def draw_shape(self, shape):
        """
        Draws the shape parameter onto the existing canvas. 
        Calls: draw_square
        """
        for row in self.shapes:
            for col in self.shapes:
                if shape.squares[row][col] == True:
                    self.draw_square(row, col, fill = shape.color)
                    
    def run(self, grid):
        print("run************************************")
        global delay
        run_flag = False

        if self.shapes:
            next_shape = get_shape(self.shapes.pop(0))
            print("run", next_shape)
            run_flag = grid.updateGrid(next_shape)

        if not run_flag: #stop if full or out of shapes
            filled = sum([ sum(row) for row in grid.squares])
            size = self.rows * self.cols
            print('size: ', size, 'squares filled: ', filled, '  percent: ', str(100* filled/size))
        else:
            print("run ", next_shape.num_rotations, next_shape.squares)
            grid.print()
            
            self.draw_shape(next_shape)
            self.master.after(delay, self.run, grid) #the request to run this function again

def start(rows,cols):
    """
    Make a blank Board, size rows x cols. Make a Game of the same size
    on which to draw shapes. Read the shape number sequence from a
    string or data file. Try to fit the shape onto the board; if the
    shape doesn't fit, game is over and def displays number of filled
    and blank spaces on the board, and the percentage filled. Starts
    the event loop.
    
    Calls: get_shape,  
    Returns: None
    """
    global delay
    delay = 10 #msec
    global letterIndex
    letterIndex = 0
    
    shapes = list('LTIZ') * 300

    root_window = Tk()
    pack_sim = PackingSimulation(rows, cols, shapes, root_window)

    pack_sim.draw_square(0,0,'blue') #comment these out after you test
    pack_sim.draw_square(2,2,'blue')

    #example test draw_shape; comment out before testing run
    pack_sim.draw_shape(Shape('L', ((False, False, True),(True, True, True)), 'orange'))

    #test run
    grid = Grid(rows, cols, [])
    pack_sim.master.after(100, pack_sim.run, grid) 
    root_window.mainloop()

start(20,10)
