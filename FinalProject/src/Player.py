from Movable import Movable

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
import pygame as py

from pygame.transform import rotate

from typing import Any

from TestTools import outputLn

class Player(Movable):
    
    INVINCIBLE_DURATION   = 10
    path = "./images/pac_man_frame2.png"
    invinciblePath = "./images/halo.png"
    playerImage = py.image.load(path)
    invincibleEffect = py.image.load(invinciblePath)
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__()
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
    

    def getSurface(self) -> Surface:
        surface = self.playerImage.copy() 
        if self.isInvincible():
            surface.blit(self.invincibleEffect, (0, 0))
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

    def pack(self) -> tuple[str, dict[str, Any]]: 
        info = {
            "invincible" : self.isInvincible(),
            "facing"     : self.getFacing(),
            "direction"  : self.goingTo()
        }
        return ("player", info)
    
    def unpack(self, info):
        if info["invincible"]:
            self.setInvincible() 
        else:
            self.removeInvincible()

        self.setFacing(info["facing"])
        self.setDirection(info["direction"])
        
        return self