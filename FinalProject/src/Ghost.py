from GameObject import GameObject
from Player import Player
import pygame as py
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
from random import randrange
from typing import Any
from TestTools import outputLn

class Ghost(GameObject):
    UP, DOWN, LEFT, RIGHT, NEUTRAL= (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)

    pathUp    = "./images/ghost/ghostUp.png"
    pathDown  = "./images/ghost/ghostDown.png"
    pathLeft  = "./images/ghost/ghostLeft.png"
    pathRight = "./images/ghost/ghostRight.png"
    ghostUp    = py.image.load(pathUp)
    ghostDown  = py.image.load(pathDown)
    ghostLeft  = py.image.load(pathLeft)
    ghostRight = py.image.load(pathRight)
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)
        self.facing = Ghost.RIGHT
        self.direction = Ghost.NEUTRAL

    def setDirection(self, direction : tuple) -> None:
        self.facing    = direction 
        self.direction = direction
    
    def setStuck(self) -> None:
        self.direction = self.NEUTRAL

    def goingTo(self) -> tuple:
        return self.direction 
    
    def getFacing(self) -> tuple: 
        return self.facing

    def getSurface(self) -> Surface:
        match self.getFacing():
            case Ghost.UP:
                return self.ghostUp 
            case Ghost.DOWN:
                return self.ghostDown
            case Ghost.LEFT:
                return self.ghostLeft 
            case Ghost.RIGHT:
                return self.ghostRight
            case _:
                return self.ghostRight
    
    def pack(self) -> tuple[str, dict[str, Any]]:
        info = {
            "facing"    : self.getFacing(),
            "direction" : self.goingTo()
        }
        return ("ghost", info)
    
    def unpack(self, info):
        self.setDirection(info["direction"])
        self.setFacing(info["facing"])
        return self