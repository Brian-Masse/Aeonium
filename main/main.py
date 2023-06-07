import pygame as pg
import math
import random

pg.init()

# //MARK: GLOBALS
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
SCREEN_NAME = "Aeonium"

screen_flags = pg.RESIZABLE
Global_screen: pg.Surface = pg.display.set_mode( ( SCREEN_WIDTH, SCREEN_HEIGHT ), screen_flags )
pg.display.set_caption( SCREEN_NAME )

Global_running = True

# //MARK: GLOBAL  FUNCTIONS

def translate_y( position ) -> float:
    return SCREEN_HEIGHT - position

class Text:



    default_font: pg.Font = pg.font.Font('Monoid', 32)

    def __init__( self, text: str, font: pg.Font = default_font ):
        self.text = text

        font_dir = '/Users/brianmasse/Developer/Python/Aeonium/resources/fonts/Kelsi-fill.otf'

        self.font = font
        # pg.font.Font( font_dir, 32 )
        self.text_obj = self.font.render(self.text, True, ( 0, 0, 0 ) )
        self.rect = self.text_obj.get_rect()

    def render(self, surface: pg.Surface):
        surface.blit( self.text_obj, self.rect )
            

test_text = Text("Hello Aeonium!")

# //MARK: MAIN LOOP
while Global_running:
    for event in pg.event.get():
        if (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE) or (event.type == pg.QUIT):
                Global_running = False

    Global_screen.fill( ( 255, 0, 0 ) )

    test_text.render(Global_screen)

    pg.display.flip()

pg.quit()
