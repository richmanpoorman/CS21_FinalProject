from GameObject import GameObject

class Player(GameObject):
    UP, DOWN, LEFT, RIGHT = (0, 1), (0, -1), (-1, 0), (1, 0)
    INVINCIBLE_DURATION   = 10

    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)
        self.invincibleTimer = 0

    
    def isInvincible(self) -> bool:
        return self.invincibleTimer > 0

    def setInvincible(self) -> None:
        self.invincibleTimer = Player.INVINCIBLE_DURATION

    def removeInvincible(self) -> None:
        self.invincibleTimer = 0

    def decrementInvincibleTimer(self) -> bool:
        self.invincibleTimer -= 1
        return self.isInvincible()