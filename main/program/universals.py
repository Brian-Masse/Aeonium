import pygame as pg

# //MARK: Vars
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# //MARK: Game
FPS = 60
GRAVITY = 9.8

# //MARK: FLAGS
# can be an enum
MOVE = 1
REFRESH_SEARCH = 2 # the action to trigger a refresh search for joysticks
JUMP = 3
JAB = 4

# //MARK: GLOBAL CLASSES

# Accessors
X = 0
Y = 1

PX = 0
NX = 1
PY = 2
NY = 3

class vector2:
    def __init__( self, x:float, y:float ):
        self.x = x
        self.y = y

        self.vals = [ self.x, self.y]

    def get(self, index:int) -> float:
        return self.vals[index]
    
    def set(self, index:int, value:float):
        self.vals[index] = value
    
    def add(self, index:int, value:float):
        self.vals[index] += value
    
class vector4:
    def __init__( self, x:float, y:float, z:float, w:float ):
        self.vals = [ x, y, z, w ]

    def get(self, index:int) -> float:
        return self.vals[int(index)]
    
    def set(self, index:int, value:float):
        self.vals[int(index)] = value
    
    def add(self, index:int, value:float):
        self.vals[int(index)] += value
    
    # axis is 0 for x and 1 for 1
    def net(self, axis:int) -> float:
        return self.vals[ int(2 * axis) ] + self.vals[ int(2 * axis) + 1 ]

    def clear(self):
        for i in range( 0, 4 ):
            self.vals[i] = 0
