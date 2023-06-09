import pygame as pg

from program.universals import*
from program.attack.attack import*

class Jab(Attack):
    def __init__(self, parent: pg.sprite.Sprite):

        frame1 = Attack_Frame(Hitbox( vector2( 10, 10 ) ), duration=60 )
        frame2 = Attack_Frame(Hitbox( vector2( 100, 100 ) ), duration=10 )
        frame3 = Attack_Frame(Hitbox( vector2( 50, 50 ) ), duration=35 )
        sequence = [frame1, frame2, frame3]
    
        super().__init__( parent, sequence )