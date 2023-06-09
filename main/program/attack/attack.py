import pygame as pg

from program.universals import*
from program.game_sys import* 

class Hitbox:
    def __init__( self, size: vector2 ):
        self.size = size

        self.image = pg.Surface( (self.size.get(0), self.size.get(1)) )
        self.image.fill( GREEN )
        self.rect = self.image.get_rect()
    
    def update(self, parent:pg.sprite.Sprite):
        self.rect = parent.rect

    def render(self, surface:pg.Surface):
        surface.blit( self.image, self.rect )
        
class Attack_Frame:
    def __init__(self, hitbox:Hitbox, duration:int):
        self.hitbox = hitbox
        self.duration = duration

class Attack:
    def __init__(self, parent:pg.sprite.Sprite, sequeunce:list[Attack_Frame]):
        self.sequence: list[Attack_Frame] = sequeunce
        self.active_frame: int = 0
        self.active = False

        self.parent:pg.sprite.Sprite = parent
    
    def initiate(self):
        self.active = True
        self.active_frame = -1
        self.progress()
    
    def update(self):
        if self.active:
            self.sequence[self.active_frame].hitbox.update(self.parent)

    def render(self, surface: pg.Surface):
        if self.active:
            self.sequence[self.active_frame].hitbox.render(surface)

    def progress(self):
        self.active_frame += 1
        if self.active_frame < len(self.sequence):
            Timer( self.sequence[self.active_frame].duration, self.progress )
        else: 
            self.active = False