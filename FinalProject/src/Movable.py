from GameObject import GameObject 

from typing import Any

class Movable(GameObject):
    UP, DOWN, LEFT, RIGHT, NEUTRAL = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)

    def __init__(self):
        '''
            Params  : (None)
            Purpose : Creates an game object that can move on the board
        '''
        self.facing = Movable.RIGHT 

    def setGoingTo(self, direction : tuple):
        '''
            Params  : ([int, int]) direction := The direction to try to go to
            Purpose : Sets the directio the object is trying to move to 
            Return  : (None)
        '''
        self.setFacing(direction)
        
    def setFacing(self, direction : tuple): 
        '''
            Params  : ([int, int]) direction := The direction the object is facing
            Purpose : Sets the direction the object is facing
            Return  : (None)
        '''
        self.facing = direction
    
    def getFacing(self) -> tuple: 
        '''
            Params  : (None)
            Purpose : Gets the direction the object is facing
            Return  : ([int, int]) The direction the object is facing
        '''
        return self.facing
    
    def pack(self) -> tuple[str, dict[str, Any]]:
        '''
            Params  : (None)
            Purpose : Packs the information required to be a movable object
            Return  : (Message) The packed object for movable
        '''
        info = {
            "facing" : self.getFacing()
        }
        return ("movable", info)
    
    def unpack(self, info):
        '''
            Params  : (dict) info := The information for how to unpack a movable
            Purpose : Unpack a movable object
            Return  : (self) The unpacked object
        '''
        self.setFacing(info["facing"])
        return self