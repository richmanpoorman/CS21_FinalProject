from GameObject import GameObject 

class Movable(GameObject):
    
    UP, DOWN, LEFT, RIGHT, NEUTRAL = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
    
    def __init__(self):
        self.facing    = Movable.RIGHT
        self.wentTo  = Movable.NEUTRAL
    
    def wentToReset(self):
        self.wentTo = Movable.NEUTRAL 

    def setWentTo(self, direction : tuple):
        self.wentTo = direction
    
    def getWentTo(self):
        return self.wentTo

    def setFacing(self, direction : tuple):
        self.facing = direction 

    def setGoingTo(self, direction : tuple):
        self.setFacing(direction)
        self.setWentTo(direction)
    
    def getFacing(self) -> tuple: 
        return self.facing