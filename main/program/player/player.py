import pygame as pg

from program.player.rigid_body import*

class Player( Rigid_Body ):
    def __init__(self, id:int, size: vector2, pos: vector2=(0, 0), color:tuple[int, int, int]=BLACK):
        super().__init__( size, pos, color )

        self.id = id
        
        self.setup()

    def setup(self):
        notification_manager.register_observer( self.id, [ MOVE ], self.move )
        notification_manager.register_observer( self.id, [ JUMP ], self.jump )
        

