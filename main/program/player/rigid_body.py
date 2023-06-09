import pygame as pg
import math
import uuid

from program.universals import*
from program.game_sys import*
from program.controller_manager import*


# //MARK: CONSTANTS
# The direction of the object colliding with the constant object
COLLISION_RIGHT = 0
COLLISION_LEFT = 1
COLLISION_DOWN = 2
COLLISION_UP = 3

# //MARK: RIGID BODY

class Rigid_Body(pg.sprite.Sprite):

    def __init__(self, size: vector2, pos:vector2, color:tuple[int, int, int]=BLACK, feels_gravity=True):
        pg.sprite.Sprite.__init__(self)

        self.id = uuid.uuid1()

        # basic attributes
        self.image = pg.Surface( size )
        self.image.fill( color )

        self.x:float = pos.get(X)
        self.y:float = pos.get(Y)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # physics
        self.mass: float = 50
        self.forces = vector4(0, 0, 0, 0) #+x, -x, +y, -y
        self.velocity = vector2(0, 0)

        # Collision
        self.elasticity: float = 0.5
        self.in_collision = False

        # Properties
        self.feels_gravity = feels_gravity
        self.on_ground = False

    # //MARK: UPDATE LOOP
    def update(self):

        self.reset_vars()
        if self.feels_gravity:
            self.forces.add( PY, GRAVITY )

        self.calculate_pos()
        self.check_collisions()
        self.finalize_pos()

    # done at the start of the loop instead of the end, because all actions run before the first call of this loop 
    def reset_vars(self):
        self.on_ground = False

    # simulate the next move for positon
    # check_collision will validate this
    def calculate_pos(self):

        net_y = self.forces.get(PY) + self.forces.get(NY)
        self.velocity.add(Y, net_y / self.mass )
        
        self.x += (self.velocity.get(X)) * Game_sys.dt
        self.y += (self.velocity.get(Y)) * Game_sys.dt
        self.rect.center = ( self.x, self.y )
    
    # this applies any corrective action
    def finalize_pos(self):
        self.rect.center = (self.x, self.y)
        self.forces.clear()
    
    # //MARK: COLLISIONS
    def check_collisions(self):
        copy_sprites = sprite_manager.sprites.copy()
        copy_sprites.remove(self)

        for sprite in copy_sprites:

            if isinstance(sprite, Ground) and not isinstance(self, Ground):
                collision_dir = self.check_collision( sprite )
                if collision_dir != -1:
                    if collision_dir == COLLISION_DOWN: 
                        self.on_ground = True
                    self.collide_elastically(collision_dir, sprite)
                

    # for individual object - object collisions
    def check_collision(self, object2:'Rigid_Body') -> int:

        y_dir = -1
        x_dir = -1

        # if colliding they should be positive
        # if they are colliding in both directions, whichever one is closer to their edge (represented by dx, dy) shoul take priority
        dy = 0
        dx = 0

        if (self.rect.bottom >= object2.rect.top and self.rect.top <= object2.rect.top) and ( self.rect.right > object2.rect.left and self.rect.left < object2.rect.right ):
            y_dir = COLLISION_DOWN
            dy = self.rect.bottom - object2.rect.top
        elif (self.rect.top <= object2.rect.bottom and self.rect.bottom >= object2.rect.bottom) and ( self.rect.right > object2.rect.left and self.rect.left < object2.rect.right ):
            y_dir = COLLISION_UP
            dy = object2.rect.bottom - self.rect.top
        if (self.rect.right >= object2.rect.left and self.rect.left <= object2.rect.left) and ( self.rect.bottom > object2.rect.top and self.rect.top < object2.rect.bottom ):
            x_dir = COLLISION_RIGHT
            dx = self.rect.right - object2.rect.left 
        elif (self.rect.left <= object2.rect.right and self.rect.right >= object2.rect.right) and ( self.rect.bottom > object2.rect.top and self.rect.top < object2.rect.bottom ):
            x_dir = COLLISION_LEFT
            dx = object2.rect.right - self.rect.left

        if x_dir != -1 and y_dir != -1:
            if dx < dy: return x_dir
            return y_dir
    
        return max(x_dir, y_dir)

    # for a moving object against a fixed one 
    def collide_elastically(self, collision_dir:int, sprite:pg.sprite.Sprite):

        # convers the 4 dimensional up/down left/right representation of dir into an x/y representation
        axis = math.floor( float(collision_dir) / 2 ) 
                   
        if collision_dir == COLLISION_DOWN:
            self.y = sprite.rect.top - (self.rect.height / 2)
        if collision_dir == COLLISION_UP:
            self.y = sprite.rect.bottom + (self.rect.height / 2)
        if collision_dir == COLLISION_RIGHT:
            self.x = sprite.rect.left - (self.rect.width / 2)
        if collision_dir == COLLISION_LEFT:
            self.x = sprite.rect.right + (self.rect.width / 2)

        # if you are accelerating into the wall, do a bounc back, otherwise, simply stop
        if self.forces.net(axis) != 0:
            self.velocity.set(axis, float(-self.velocity.get(axis) * self.elasticity))
            if abs(self.velocity.get(axis)) < 1:
                self.velocity.set(axis, 0)
        else:
            self.velocity.set(axis, 0)

    # //MARK: RENDER
    def render(self, surface: pg.Surface):
        surface.blit( self.image, self.rect )

# //MARK: GROUND

class Ground(Rigid_Body):
    pass
    def __init__( self, size: vector2, pos: vector2=(0, 0) ):
        super().__init__(size, pos, feels_gravity=False)
    
