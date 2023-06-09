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

        self.x:float = pos[0]
        self.y:float = pos[1]

        # physics
        self.mass: float = 50
        self.forces = vector4(0, 0, 0, 0) #+x, -x, +y, -y
        self.velocity = vector2(0, 0)

        # Collision
        self.elasticity: float = 0.5
        self.in_collision = False

        # Properties
        self.feels_gravity = feels_gravity
        self.test = 0


    def update(self):
        if self.feels_gravity:
            self.forces.add( PY, GRAVITY )

        self.check_collisions()
        self.calculate_pos()
        
    def move(self, event:Notification_Event):
        move_speed = ( event.value / max(abs(event.value), 1) ) * 5
        self.velocity.set(X, move_speed) 
    
    def jump(self, event:Notification_Event):
        self.forces.add( NY, -500 )

    def check_collisions(self):
        copy_sprites = sprite_manager.sprites.copy()
        copy_sprites.remove(self)

        for sprite in copy_sprites:

            if self.check_collision( sprite ):
                if isinstance(sprite, Ground):
                    self.collide_elastically(sprite)

    # for individual object - object collisions
    def check_collision(self, object2:'Rigid_Body') -> bool:
        if (self.rect.bottom >= object2.rect.top and self.rect.top <= object2.rect.top) or ( self.rect.top <= object2.rect.bottom and self.rect.bottom >= object2.rect.bottom):
            return True
        
        # if (self.rect.left < object2.rect.right and self.rect.right > object2.rect.right) or ( self.rect.right > object2.rect.left and self.rect.left < object2.rect.left):
        #     return Collision_Info( vector2( self.rect.left, self.rect.y ), 0 )
    
    def determine_velocity_dir(self, axis:int) -> int:
        net = self.velocity.get(axis)
        if net == 0: 
            return 0
        return net / abs(net)

    def determine_force_dir(self, axis:int) -> int:
        net = self.forces.get( (2 * axis) ) + self.forces.get( (2 * axis) + 1 )
        if net == 0:
            return 0
        return net / abs(net)

    def apply_normal_force(self, axis:int):
        # use this function to create a counter amont of force in the direction opposing the motion
        # ie. if a block is accelerating into a fixed object, this will generate an equal amount of force in the direction opposing the motion
        direction = self.determine_velocity_dir(axis)

        # receiving index is the index of the positive/negative component of the force which the normal force will be added tp
        # value index is the index of the component of the force the normal force will be computed from
        # These are formulas that take the axis (-1 or 1) and translate them into the correct index in a vec4 accessor
        receiving_index = max( direction, 0 ) + (2 * axis)
        value_index = max( -direction, 0 ) + (2 * axis)

        self.forces.add( receiving_index, -self.forces.get( value_index ) )

    # for a moving object against a fixed one 
    def collide_elastically(self, sprite:pg.sprite.Sprite):

        def apply_velocity():
            # handles putting the box against the wall that it is colliding with depending on dir
            # this should happen regardless of if it is accelerating or moving into the wall
            # so the boxs only collide once when bouncing, and collid indefinitley when they come to rest
            force_dir_y = self.determine_force_dir(Y)
            velocity_dir_y = self.determine_velocity_dir(Y)

            if force_dir_y > 0 or velocity_dir_y > 0:
                self.y = sprite.rect.top - (self.rect.height / 2)
            if force_dir_y < 0 or velocity_dir_y < 0:
                self.y = sprite.rect.bottom + (self.rect.height / 2)
            
            force_dir_x = self.determine_force_dir(X)
            velocity_dir_x = self.determine_velocity_dir(X)

            if force_dir_x > 0 or velocity_dir_x > 0:
                self.y = sprite.rect.left - (self.rect.width / 2)
            if force_dir_x < 0 or velocity_dir_x < 0:
                self.y = sprite.rect.right + (self.rect.width / 2)
        

        # self.apply_normal_force( X )
        self.apply_normal_force( Y )
                   
        apply_velocity()

        self.velocity.set(Y, float(-self.velocity.get(Y) * self.elasticity))
        if abs(self.velocity.get(Y)) < 1:
            self.velocity.set(Y, 0)


    def calculate_pos(self):

        net_y = self.forces.get(PY) + self.forces.get(NY)
        self.velocity.add(Y, net_y / self.mass )
        
        self.x += (self.velocity.get(X)) * Game_sys.dt
        self.y += (self.velocity.get(Y)) * Game_sys.dt
        self.rect.center = ( self.x, self.y )

        # print(self.y)

        self.forces.clear()

    def render(self, surface: pg.Surface):
        self.test += 0.5 * Game_sys.dt
        # surface.blit( self.image, (self.test, 100) )
        # print(self.x, self.y)
        surface.blit( self.image, self.rect )

# //MARK: GROUND

class Ground(Rigid_Body):
    pass
    def __init__( self, size: vector2, pos: vector2=(0, 0) ):
        super().__init__(size, pos, feels_gravity=False)
    
