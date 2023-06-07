import pygame as pg
import math
import random

pg.init()

# //MARK: GLOBALS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN_NAME = "Aeonium"

screen_flags = pg.RESIZABLE
pg.display.set_caption( SCREEN_NAME )
pg.display.set_mode()
Global_screen: pg.Surface = pg.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ), screen_flags )

# //MARK: GLOBAL  FUNCTIONS

def translate_y( position ) -> float:
    return SCREEN_HEIGHT - position

# //MARK: FONTS

FONTS_PATH = 'resources/fonts/'
MONOID = FONTS_PATH + 'Monoid-Regular.ttf'

default_font: pg.font.Font = pg.font.Font(MONOID, 32)


class Text:

    def __init__( self, text: str, position: tuple[float, float]=(0, 0), color: tuple[int, int, int]=(0, 0, 0), font: pg.font.Font = default_font ):
        self.text = text
        self.font = font
        self.color = color
        self.position = position

        self.define_text_obj()
        
    def define_text_obj(self):
        self.text_obj = self.font.render(self.text, True, self.color)
        self.rect = self.text_obj.get_rect()
        self.rect.topleft = self.position

    def update(self, text ):
        self.text = text
        self.define_text_obj()

    def render(self, surface: pg.Surface):
        surface.blit( self.text_obj, self.rect )
    


class Sys(): 
     
    def __init__(self):
        self.running = True
        self.clock = pg.time.Clock()
        self.fps: int

        self.test_text = Text("fps: ")

    def update(self):
        self.update_clock()

    def render(self):
        self.test_text.render(Global_screen)

    def update_clock(self):
        self.clock.tick()
        self.fps = self.clock.get_fps()

        if (pg.time.get_ticks() % 2000 <= 25):
            self.test_text.update("fps: " + str( math.floor(self.fps)))
     

Game_sys = Sys()

# //MARK: MAIN LOOP
while Game_sys.running:
    for event in pg.event.get():
        if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (event.type == pg.QUIT):
                Game_sys.running = False

    Game_sys.update()

    Global_screen.fill( ( 255, 0, 0 ) )

    Game_sys.render()

    pg.display.update()

pg.quit()
