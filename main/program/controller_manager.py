import pygame as pg
from enum import Enum

from program.universals import*
from program.notification_manager import*

# This class is only focused on the input events, for other event handling, see the Event_Handler
class Controller_Manager:
    def __init__(self):
        
        self.joysticks: list[pg.joystick.Joystick] = []
        self.add_joysticks()

        # when REFRESH_SEARCH IS POSTED, TRIGGER THE ADD_JOYSTICKS FUNCTION
        notification_manager.register_observer( 0, [ REFRESH_SEARCH ], self.add_joysticks )

    def translate_event( self, event:pg.event.Event ):
        
        self.define_key_action( event, pg.K_r, REFRESH_SEARCH  )

        # move
        self.define_key_action( event, pg.K_d, MOVE, start_value=1, end_value=0 )
        self.define_key_action( event, pg.K_a, MOVE, start_value=-1, end_value=0 )
        self.define_key_action( event, pg.K_SPACE, JUMP)
        
        self.define_button_action( event, pg.CONTROLLER_BUTTON_A, JUMP)

        for joystick in self.joysticks:
            horizontal_left_axis = joystick.get_axis(0)
            notification_manager.post(Notification_Event(joystick.get_instance_id(), MOVE, value=horizontal_left_axis)) 
    
    # for keyboard events, pygame doesn't have a built in identifier system, so I'll need to find it in other python packages. For now its fine, since I'm only using one controller
    # this function makes associating key actions with post messages quicker to define in translate_event
    # start value is the value that will be passed when the key is pressed, end_value is the value that will be passed when the key is released
    def define_key_action(self, event:pg.event.Event, key:int, flag:int, start_value:float=0, end_value:float=0, id:int=0):
        if event.type == pg.KEYDOWN and event.key == key:
            notification_manager.post( Notification_Event( id=id, flag=flag, value=start_value ) )
        if event.type == pg.KEYUP and event.key == key:
            notification_manager.post( Notification_Event( id=id, flag=flag, value=end_value ) )
        
    def define_button_action(self, event:pg.event.Event, button:int, flag:int, start_value:float=1, end_value:float=0):
        if event.type == pg.JOYBUTTONDOWN and event.button == button:
            notification_manager.post( Notification_Event( id=event.joy, flag=flag, value=start_value ) )
        if event.type == pg.JOYBUTTONUP and event.button == button:
            notification_manager.post( Notification_Event( id=event.joy, flag=flag, value=end_value ) )


    # triggered by a Controller_Event
    def add_joysticks( self, event:Notification_Event=None ):
        for i in range(0, pg.joystick.get_count()):
            joystick = pg.joystick.Joystick(i)

            if sum( joy.get_id() == joystick.get_id() for joy in self.joysticks ) == 0:
                self.joysticks.append(joystick)
    

controller_manager = Controller_Manager()