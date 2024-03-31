from GameObject import GameObject

class Player(GameObject):
    UP, DOWN, LEFT, RIGHT = 0, 1, 2, 3

    def __init__(self, position : tuple, surface : tuple):
        super().__init__(position, surface)
        pass 

    def movePlayer(self, dir : int, boardSize : tuple) -> None:
        pass 
    
    def isInvincible(self) -> bool:
        pass

    def setInvincible(self) -> None:
        pass 

    def decrementInvincibleTimer(self) -> bool:
        pass 