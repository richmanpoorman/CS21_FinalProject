from GameObject import GameObject

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
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
    
    def getSurface(self) -> Surface | None:
        surface = Surface((200, 200))
        surface.fill((0, 200, 100))
        return surface
    
    def pack(self) -> tuple[str, dict[str, str]]: 
        return ("player", {"invincible" : "True" if self.isInvincible() else "False"})
    
    def unpack(self, info):
        invincibleState = info["invincible"]
        match invincibleState:
            case "True":
               self.setInvincible()
            case "False":
                self.removeInvincible()
            case _:
                pass 
        return self