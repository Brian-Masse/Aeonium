import pygame as pg

from program.player.rigid_body import*

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

        self.attacks: list[Attack] = [jab]

    def setup(self):
        notification_manager.register_observer( self.id, [ MOVE ], self.move )
        notification_manager.register_observer( self.id, [ JUMP ], self.receive_jump )
        notification_manager.register_observer( self.id, [ JAB ], self.jab )

    # //MARK: UPDATE + RENDER LOOP

    def update(self):
        super().update()
        self.update_actions()
    
    def render(self, surface: pg.Surface):
        super().render(surface)
        for attack in self.attacks:
            if attack.active:
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
        jab.initiate()

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


class Hitbox:
    def __init__( self, size: vector2 ):
        self.size = size

        self.image = pg.Surface( (self.size.get(0), self.size.get(1)) )
        self.image.fill( GREEN )
        self.rect = self.image.get_rect()
    
    def render(self, surface:pg.Surface):
        surface.blit( self.image, (300, 300) )
        
class Attack_Frame:
    def __init__(self, hitbox:Hitbox, duration:int):
        self.hitbox = hitbox
        self.duration = duration

class Attack:
    def __init__(self, sequeunce:list[Attack_Frame] = []):
        self.sequence: list[Attack_Frame] = sequeunce
        self.active_frame: int = 0
        self.active = False
    
    def initiate(self):
        self.active = True
        self.active_frame = -1
        self.progress()
    
    def render(self, surface: pg.Surface):
        self.sequence[self.active_frame].hitbox.render(surface)

    def progress(self):
        self.active_frame += 1
        if self.active_frame < len(self.sequence):
            Timer( self.sequence[self.active_frame].duration, self.progress )
        else: 
            self.active = False


frame1 = Attack_Frame(Hitbox( vector2( 10, 10 ) ), duration=60 )
frame2 = Attack_Frame(Hitbox( vector2( 100, 100 ) ), duration=10 )
frame3 = Attack_Frame(Hitbox( vector2( 50, 50 ) ), duration=35 )

jab = Attack( [ frame1, frame2, frame3 ] )

# # //MARK: Hitbox:

