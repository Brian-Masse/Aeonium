

class Notification_Event:
    # a flag is related to a specific, in game action, not a specific button press. Multiple button presses (from keyboards / controllers) will link to the same flag 
    # from a notification perspective, the value is generic data that is being passed through the notification
    # the id is the sender (can be the hardware id of a device, or a UUID of a class)
    def __init__(self, id:int, flag:int, value:float=0 ):
        self.id = id
        self.flag = flag
        self.value = value

# mainly just for storing these properties together
class Observer:
    def __init__(self, id:int, flags:list[int], action):
        self.id = id
        self.flags = flags
        self.action = action


class Notification_Manager:
    def __init__(self):

        self.events: list[Notification_Event] = []

        self.observers:list[Observer] = []
    
    def update(self):
        self.events.clear()

    # All of the flags in this list will cause the action to trigger
    # the action will receive the notification event object
    def register_observer( self, id:int, flags:list[int], action ):
        self.observers.append( Observer( id, flags, action ) )
    
    def post(self, event:Notification_Event):
        self.events.append( event )
        
        [observer.action(event) for observer in self.observers if (observer.id == event.id and observer.flags.count( event.flag ) != 0)]
    

notification_manager = Notification_Manager()