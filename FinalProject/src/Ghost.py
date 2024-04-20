from GameObject import GameObject
from Player import Player
import pygame as py
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
from random import randrange

from TestTools import outputLn

class Ghost(GameObject):
    path = "./images/ghosts.png"
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)
        

    def getSurface(self) -> Surface | None:
        surface = py.image.load(self.path)
        return surface
    
    def pack(self) -> tuple[str, dict[str, str]]:
        return ("ghost", dict())
    
    def unpack(self, info):
        return self