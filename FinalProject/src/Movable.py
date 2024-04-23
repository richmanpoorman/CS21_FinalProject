from GameObject import GameObject 

class Movable(GameObject):
    
    UP, DOWN, LEFT, RIGHT, NEUTRAL = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
    
    def __init__(self):
        self.facing    = Movable.RIGHT
        self.direction = Movable.NEUTRAL
    
    def setFacing(self, direction : tuple):
        self.facing = direction 

    def setDirection(self, direction : tuple) -> None:
        self.direction = direction

    def setGoingTo(self, direction : tuple):
        self.setFacing(direction)
        self.setDirection(direction)
    
    def noMovement(self) -> None:
        self.direction = self.NEUTRAL

    def goingTo(self) -> tuple:
        return self.direction 
    
    def getFacing(self) -> tuple: 
        return self.facing