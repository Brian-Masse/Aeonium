import pygame as pg

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

FPS = 60

# //MARK: FLAGS
# can be an enum
MOVE = 1
REFRESH_SEARCH = 2 # the action to trigger a refresh search for joysticks

# //MARK: GLOBAL CLASSES

class vector2:
    def __init__( self, x:float, y:float ):
        self.x = x
        self.y = y

    def get(self, index:int) -> float:
        if index == 0: return self.x
        if index == 1: return self.y
        return 0
    
    def set(self, index:int, value:float):
        if index == 0: self.x = value
        if index == 1: self.y = value
        return 0
    
# //MARK: GLOBAL FUNCTIONS

