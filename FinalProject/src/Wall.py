from GameObject import GameObject

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface 

import pygame as py

class Wall(GameObject):
    path = "./images/wall.png"
    wallImage = py.image.load(path)
    def __init__(self):
        super().__init__(None)

    @staticmethod 
    def convertImage():
        Wall.wallImage = Wall.wallImage.convert()

    def getSurface(self) -> Surface | None:
        
        return self.wallImage
    
    def pack(self) -> tuple[str, dict[str, str]]:
        return ("wall", dict())
    
    def unpack(self, data : dict):
        return self