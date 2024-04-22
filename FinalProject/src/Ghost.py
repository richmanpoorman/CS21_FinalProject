from GameObject import GameObject
from Player import Player
import pygame as py
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
from random import randrange

from TestTools import outputLn

class Ghost(GameObject):
    UP, DOWN, LEFT, RIGHT, NEUTRAL= (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)

    path = "./images/ghosts.png"
    ghostImage = py.image.load(path)
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
        return self.ghostImage
    
    def pack(self) -> tuple[str, dict[str, str]]:
        return ("ghost", dict())
    
    def unpack(self, info):
        return self