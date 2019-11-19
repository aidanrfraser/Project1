"""
CISC106 Testing Module that includes some basic helper functions
such as assertEqual
"""
import sys, traceback, types

success = 0
fail = 0

def assertEqual(testValue, expectedValue, *args):
    """
    This is for comparing a test value to an expected value.
    Uses the isEqual function.
    Prints a message if the test case passed or failed.
    """    
    trace = traceback.extract_stack()
    frame = trace[len(trace)-2]
    global success, fail
    
    if not isEqual(testValue, expectedValue, *args):
        fail += 1
        print( "[%d tests: %d failed] line %d: failure for %s, received %s expected %s" \
            % (success + fail, fail, frame[1], frame[3], testValue, expectedValue) )
    else:
        success += 1
        print( "[%d tests: %d failed] line %d: success" \
            % (success + fail, fail, frame[1]) )
    
def isEqual(x, y, *args):
    """
    isEqual : thing thing -> boolean
    isEqual : number number number -> boolean
    Determines whether the two arguments are equal, or in the case of
    floating point numbers, within a specified number of decimal points
    precision (by default, checks to with 4 decimal points for floating
    point numbers).
    
    Examples:
    >>> isEqual('ab', 'a'+'b')
     True
     
    >>> isEqual(12.34, 12.35)
     False
     
    >>> isEqual(12.3456, 12.34568, 4)
     True
         
    >>> isEqual(12.3456, 12.34568, 5)
     False
    """
    if x == y:
        return True
    elif x is None or y is None:
        return False
    elif type(x) == int and type(y) == int:
        return x == y
    elif type(x) == float or type(y) == float:
        if len(args) == 1:
            error = 10 ** (- args[0])
        else:
            error = 0.0001
        return abs(x - y) < error
    elif isseqtype(x) and isseqtype(y) and len(x)==len(y):
        for (x1,y1) in zip(x, y):
            if not isEqual(x1, y1, *args):
                return False
        return True
    elif type(x) == dict == type(y):
        if len(x) == len(y):
            for k, v in x.items():
                if not isEqual(v, y[k], *args):
                    return False
            return True
    else:
        return False

def isseqtype(x):
    return type(x) == list or type(x) == tuple

def print_verbose(obj):
    for f in dir(obj):
        print( f, "=", getattr(obj, f) )


## SIMPLE IMAGING AND ANIMATION ##
        
#import Tkinter
#from PIL import Image, ImageTk
#
#class TKGUI:
#    image = None
#    label = None
#    geo = None
#    root = None
#    
#    def _init(self):
#        if self.root is None:
#            self.root = Tkinter.Tk()
#            self.root.title("") #set title blank
#            self.root.protocol('WM_DELETE_WINDOW',self.quit)   #close button
#            self.root.resizable(0,0) #do not allow resizing
#            self.root.wm_attributes("-topmost", 1) #move window to top
#            self.root.focus()
#            
#    def quit(self):
#        self.root.destroy()
#    def wait(self):
#        self.root.wait_window(self.root)
#        self.root = None
#    def on_tick(self, tickfunction, ticktime=1000, tick=0):
#        self._init()
#        
#        self.image = tickfunction(tick)
#        if self.image is None:
#            print( "Error: tickfunction did not return an Image" )
#        else:
#            self.tkImage = ImageTk.PhotoImage(self.image)
#            oldLabel = self.label
#            self.label = Tkinter.Label(self.root, image=self.tkImage) 
#            self.label.place(width=self.image.size[0], \
#                             height=self.image.size[1])
#            geo = '%dx%d' % self.image.size
#            if not geo == self.geo:
#              self.geo = geo
#              self.root.geometry(geo)
#            self.label.pack()
#            if oldLabel is not None:
#                oldLabel.destroy()
#
#        self.root.after(ticktime, self.on_tick, \
#                        tickfunction, ticktime, tick+1)
#
## global gui helper
#gui = TKGUI()
#
#def display(image):
#    gui.on_tick(lambda x: image, 99999999)
#    gui.wait()
#
#def animate(on_tick_function, tick_length_ms=1000):
#    gui.on_tick(on_tick_function, tick_length_ms)
#    gui.wait()
#
#def bind(event, on_event_function):
#    gui._init()
#    gui.root.bind(event, on_event_function)
#
