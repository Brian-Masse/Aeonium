import pygame as pg
from ..universals import*

# //MARK: Globals
FONTS_PATH = 'resources/fonts/'
MONOID = FONTS_PATH + 'Monoid-Regular.ttf'

default_font: pg.font.Font = pg.font.Font(MONOID, 16)


class Text:

    def __init__( self, text: str, position: tuple[float, float]=(0, 0), color: tuple[int, int, int]=BLACK, font: pg.font.Font = default_font ):
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
        pass
        # surface.blit( self.text_obj, self.rect )
    
