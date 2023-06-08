import pygame as pg
import math

from program.universals import*
from program.UI.text import* 
from program.controller_manager import*

# //MARK: GLOBALS
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_NAME = "Aeonium"

screen_flags = pg.RESIZABLE
pg.display.set_caption( SCREEN_NAME )
pg.display.set_mode()
Global_screen: pg.Surface = pg.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ), screen_flags )

class Sprite_Manager:
    def __init__(self):
        self.sprites: list[pg.sprite.Sprite] = []

    def add(self, sprites:list[pg.sprite.Sprite]):
        for sprite in sprites:
            self.sprites.append(sprite)

sprite_manager = Sprite_Manager()

# //MARK: Game System
class Sys(): 
     
    def __init__(self):
        self.running = True
        self.clock = pg.time.Clock()

        self.dt: int = 1 # delta time
        self.fps: int = 1

        self.test_text = Text("fps: ")

    def update(self):
        for sprite in sprite_manager.sprites:
            sprite.update()

        self.update_clock()
        controller_manager.update()
        

    def render(self):
        Global_screen.fill( WHITE )

        for sprite in sprite_manager.sprites:
            sprite.render( Global_screen )

        self.test_text.render(Global_screen)

    def update_clock(self):
        pass
        # this is now happening after the render loop in main.py
        
        # self.dt = self.clock.tick(FPS)
        # self.fps = self.clock.get_fps()
        # self.test_text.update("fps: " + str( math.floor(self.fps)))
            


Game_sys = Sys()

