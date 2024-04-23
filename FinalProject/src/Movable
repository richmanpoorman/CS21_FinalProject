from GameObject import GameObject 

from typing import Any

class Movable(GameObject):
    UP, DOWN, LEFT, RIGHT, NEUTRAL = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)

    def __init__(self):
        self.facing = Movable.RIGHT 
        
    def setFacing(self, direction : tuple): 
        self.facing = direction
    
    def getFacing(self) -> tuple: 
        return self.facing
    
    def pack(self) -> tuple[str, dict[str, Any]]:
        info = {
            "facing" : self.getFacing()
        }
        return ("movable", info)
    
    def unpack(self, info):
        self.setFacing(info["facing"])
        return self