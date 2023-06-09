import pygame as pg

from program.player.rigid_body import*

class Player( Rigid_Body ):
    def __init__(self, id:int, size: vector2, pos:vector2=(0, 0), color:tuple[int, int, int]=BLACK):
        super().__init__( size, vector2(100, 100), color )

        self.id = id

        self.MOVEMENT_THRESHOLD: float = 0.1

        self.on_ground = False
        
        self.setup()

    def setup(self):
        notification_manager.register_observer( self.id, [ MOVE ], self.move )
        notification_manager.register_observer( self.id, [ JUMP ], self.jump )
    
    # //MARK: ACTIONS
    def move(self, event:Notification_Event):
    
        value = 0
        if abs(event.value) > self.MOVEMENT_THRESHOLD:
            value = event.value

        move_speed = ( value / max(abs(value), 1) ) * 5
        self.velocity.set(X, move_speed) 
    
    def jump(self, event:Notification_Event):
        self.forces.add( NY, -200 )
        

