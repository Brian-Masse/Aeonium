import pygame as pg
from enum import Enum

from program.universals import*

class Controller_Event:
    # a flag is related to a specific, in game action, not a specific button press. Multiple button presses (from keyboards / controllers) will link to the same flag 
    # from a notification perspective, the value is generic data that is being passed through the notification
    # the id is the sender (can be the hardware id of a device, or a UUID of a class)
    def __init__(self, id:str, flag:int, value:float=0 ):
        self.id = id
        self.flag = flag
        self.value = value

# mainly just for storing these properties together
class Observer:
    def __init__(self, flags:list[int], action):
        self.flags = flags
        self.action = action

# This class is only focused on the input events, for other event handling, see the Event_Handler
class Controller_Manager:
    def __init__(self):

        self.events: list[Controller_Event] = []
        
        self.joysticks: list[pg.joystick.Joystick] = []

        self.observers:list[Observer] = []

        # when REFRESH_SEARCH IS POSTED, TRIGGER THE ADD_JOYSTICKS FUNCTION
        self.register_observer( [ REFRESH_SEARCH ], self.add_joysticks )

    # All of the flags in this list will cause the action to trigger
    # the action will receive the notification event object
    def register_observer( self, flags:list[int], action ):
        self.observers.append( Observer( flags, action ) )
    
    def post(self, event:Controller_Event):
        self.events.append( event )
        
        [observer.action(event) for observer in self.observers if observer.flags.count( event.flag ) != 0]
    

    def translate_event( self, event:pg.event.Event ):
        
        self.define_key_action( event, pg.K_r, REFRESH_SEARCH  )

        # move
        self.define_key_action( event, pg.K_d, MOVE, start_value=1, end_value=0 )
        self.define_key_action( event, pg.K_a, MOVE, start_value=-1, end_value=0 )

        for joystick in self.joysticks:
            horizontal_left_axis = joystick.get_axis(0)
            self.post(Controller_Event(joystick.get_guid(), MOVE, value=horizontal_left_axis)) 
    
    # for keyboard events, pygame doesn't have a built in identifier system, so I'll need to find it in other python packages. For now its fine, since I'm only using one controller
    # this function makes associating key actions with post messages quicker to define in translate_event
    # start value is the value that will be passed when the key is pressed, end_value is the value that will be passed when the key is released
    def define_key_action(self, event:pg.event.Event, key:int, flag:int, start_value:float=0, end_value:float=0, id:str=""):
        if event.type == pg.KEYDOWN and event.key == key:
            self.post( Controller_Event( id=id, flag=flag, value=start_value ) )
        if event.type == pg.KEYUP and event.key == key:
            self.post( Controller_Event( id=id, flag=flag, value=end_value ) )
    
    def update(self):
        self.events.clear()

    # triggered by a Controller_Event
    def add_joysticks( self, event:Controller_Event ):
        for i in range(0, pg.joystick.get_count()):
            joystick = pg.joystick.Joystick(i)

            if sum( joy.get_id() == joystick.get_id() for joy in self.joysticks ) == 0:
                self.joysticks.append(joystick)
    

controller_manager = Controller_Manager()