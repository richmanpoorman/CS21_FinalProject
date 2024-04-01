from GameObject import GameObject

class Player(GameObject):
    UP, DOWN, LEFT, RIGHT = (0, 1), (0, -1), (-1, 0), (1, 0)
    INVINCIBLE_DURATION   = 10

    def __init__(self, position : tuple, surface : tuple):
        super().__init__(position, surface)
        self.invincibleTimer = 0

    def movePlayer(self, dir : tuple, boardSize : tuple) -> None:
        w , h  = boardSize 
        dx, dy = dir 
        x , y  = self.getPosition()
        newX, newY = x + dx, y + dy 
        
        # Wrap if going off of the board
        if newX < 0:
            newX = w - 1 
        elif newX >= w:
            newX = 0 
        elif newY < 0:
            newY = h - 1 
        elif newY >= h:
            newY = 0

        # Set the position, assuming it is checked that it can move there
        self.setPosition((newX, newY))

    
    def isInvincible(self) -> bool:
        return self.invincibleTimer > 0

    def setInvincible(self) -> None:
        self.invincibleTimer = Player.INVINCIBLE_DURATION

    def decrementInvincibleTimer(self) -> bool:
        self.invincibleTimer -= 1
        return self.isInvincible()