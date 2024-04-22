from GameObject import GameObject

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
import pygame as py

from pygame.transform import rotate

from typing import Any

from TestTools import outputLn

class Player(GameObject):
    UP, DOWN, LEFT, RIGHT, NEUTRAL= (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
    INVINCIBLE_DURATION   = 10
    path = "./images/pac_man_frame2.png"
    playerImage = py.image.load(path)
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)
        self.invincibleTimer = 0
        self.facing = Player.RIGHT
        self.direction = Player.NEUTRAL

    
    def isInvincible(self) -> bool:
        return self.invincibleTimer > 0

    def setInvincible(self) -> None:
        self.invincibleTimer = Player.INVINCIBLE_DURATION

    def removeInvincible(self) -> None:
        self.invincibleTimer = 0

    def decrementInvincibleTimer(self) -> bool:
        self.invincibleTimer -= 1
        return self.isInvincible()
    
    def getSurface(self) -> Surface:
        surface = self.playerImage.copy() 
        outputLn(str(self.getFacing()))
        match self.getFacing():
            case Player.UP:
                surface = rotate(surface, 90)
            case Player.DOWN:
                surface = rotate(surface, -90)
            case Player.LEFT:
                surface = rotate(surface, 180)
            case Player.RIGHT:
                outputLn("I am facing right")
            case _:
                raise RuntimeError("No direction found")
        return surface
    
    def setDirection(self, direction : tuple) -> None:
        self.facing    = direction 
        self.direction = direction
    
    def setStuck(self) -> None:
        self.direction = self.NEUTRAL

    def getGoingTo(self) -> tuple:
        return self.direction 
    
    def getFacing(self) -> tuple: 
        return self.facing

    def pack(self) -> tuple[str, dict[str, Any]]: 
        info = {
            "invincible" : self.isInvincible(),
            "facing"     : self.facing,
            "direction"  : self.direction
        }
        return ("player", info)
    
    def unpack(self, info):
        if info["invincible"]:
            self.setInvincible() 
        else:
            self.removeInvincible()

        self.facing    = info["facing"]
        self.direction = info["direction"]
        
        return self