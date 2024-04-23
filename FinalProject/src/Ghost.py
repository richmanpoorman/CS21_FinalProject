from Movable import Movable

from Player import Player
import pygame as py
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
from random import randrange

from TestTools import outputLn

class Ghost(Movable):
    UP, DOWN, LEFT, RIGHT, NEUTRAL= (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)

    path = "./images/ghosts.png"
    ghostImage = py.image.load(path)
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__()
        self.facing = Ghost.RIGHT
        self.direction = Ghost.NEUTRAL

    def getSurface(self) -> Surface:
        return self.ghostImage
    
    def pack(self) -> tuple[str, dict[str, str]]:
        return ("ghost", dict())
    
    def unpack(self, info):
        return self