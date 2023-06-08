import pygame as pg
import math
import uuid

from program.universals import*
from program.game_sys import*
from program.controller_manager import*

# //MARK: RIGID BODY

class Rigid_Body(pg.sprite.Sprite):

    def __init__(self, size: vector2, pos: vector2=(0, 0), color:tuple[int, int, int]=BLACK, feels_gravity=True):
        pg.sprite.Sprite.__init__(self)

        self.id = uuid.uuid1()

        # basic attributes
        self.image = pg.Surface( size )
        self.image.fill( color )
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

        # physics
        self.mass: float = 50
        self.forces = vector2(0, 0)
        self.velocity = vector2(0, 0)

        # Collision
        self.elasticity: float = 0.2
        self.in_collision = False

        # Properties
        self.feels_gravity = feels_gravity

        # self.setup()

    def setup(self):
        notification_manager.register_observer( [ MOVE ], self.move )
        notification_manager.register_observer( [ JUMP ], self.jump )

    def update(self):
        self.check_collisions()
        self.calculate_pos()
        
    def move(self, event:Notification_Event):
        self.velocity.x = ( event.value / max(abs(event.value), 1) ) * 5
    
    def jump(self, event:Notification_Event):
        self.forces.y += -500

    def check_collisions(self):
        copy_sprites = sprite_manager.sprites.copy()
        copy_sprites.remove(self)

        for sprite in copy_sprites:
            if pg.sprite.collide_rect( self, sprite ):
                if isinstance(sprite, Ground):
                    if not self.in_collision:
                        # if you're touching the ground and not already in collision 
                        self.collide_elastically(dir=1)
            else:
                self.in_collision = False

    # for a moving object against a fixed one 
    def collide_elastically(self, dir:int ):
        self.in_collision = True
        new_velocity = self.elasticity * -self.velocity.get(dir)
        self.velocity.set(dir, new_velocity)

        # when the bounces become small enough, stop treating it like a collision and simply resist the force of the block
        if abs(new_velocity) <= 20:
            self.in_collision = False
            self.forces.set(dir, -self.forces.get(dir))
        

    def calculate_pos(self):
        if self.feels_gravity:
            self.forces.y += GRAVITY

        self.velocity.y += ( self.forces.y / self.mass ) * float(Game_sys.dt)
        
        self.rect.x += (self.velocity.x)
        self.rect.y += (self.velocity.y / 20)

        self.forces.x = 0
        self.forces.y = 0

    def render(self, surface: pg.Surface):
        surface.blit( self.image, self.rect )



# //MARK: GROUND

class Ground(Rigid_Body):
    pass
    def __init__( self, size: vector2, pos: vector2=(0, 0) ):
        super().__init__(size, pos, feels_gravity=False)
    
