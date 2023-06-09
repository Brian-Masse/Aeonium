import pygame as pg

from program.player.rigid_body import*
from program.attack.attacks import*

class Action:
    def __init__(self, duration:int, flag:int, action):
        self.duration = duration
        self.action = action
        self.flag = flag
        self.timer: float = 0
    
    def update(self) -> bool:
        self.timer += Game_sys.dt
        if self.timer >= self.duration or self.action():
            return True
        return False
        

class Player( Rigid_Body ):
    def __init__(self, id:int, size: vector2, pos:vector2=(0, 0), color:tuple[int, int, int]=BLACK):
        super().__init__( size, pos, color )

        self.id = id

        self.MOVEMENT_THRESHOLD: float = 0.1
        self.MOVEMENT_SPEED: float = 75
        self.JUMP_FORCE: float = 1000
        
        self.setup()

        self.action_queue:list[Action]= []

        self.attacks: list[Attack] = [Jab( self ) ]
        

    def setup(self):
        notification_manager.register_observer( self.id, [ MOVE ], self.move )
        notification_manager.register_observer( self.id, [ JUMP ], self.receive_jump )
        notification_manager.register_observer( self.id, [ JAB ], self.jab )

    # //MARK: UPDATE + RENDER LOOP

    def update(self):
        super().update()
        self.update_actions()
        self.update_attacks()
    
    def render(self, surface: pg.Surface):
        super().render(surface)
        self.render_attacks(surface)
       

    def update_attacks(self):
         for attack in self.attacks:    
            attack.update()
        
    def render_attacks(self, surface: pg.Surface):
        for attack in self.attacks:    
            attack.render(surface)

    # //MARK: ACTIONS
    # if an action should be valid for a few frames after the input is received, store it in the action queue as an action. 
    # This will attempt to run the action every frame until it expires or is successful 
    def update_actions(self):
        for action in self.action_queue:
            if action.update():        
                self.action_queue.remove( action )


    def move(self, event:Notification_Event):
        value = 0
        if abs(event.value) > self.MOVEMENT_THRESHOLD:
            value = event.value

        move_speed = ( value / max(abs(value), 1) ) * self.MOVEMENT_SPEED
        self.velocity.set(X, move_speed) 

    def jab(self, event:Notification_Event):
        self.attacks[0].initiate()

    def jump(self) -> bool:
        if self.on_ground:

            self.forces.add( NY, -self.JUMP_FORCE )
            return True
        return False

    # returns a bool so the action manager know that this action has completed
    def receive_jump(self, event:Notification_Event):
        action = Action( 2, event.flag, self.jump )
        if len([ action for action in self.action_queue if action.flag == event.flag ]) == 0:
            if event.value == 1:
                self.action_queue.append( action )
