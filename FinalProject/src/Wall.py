from GameObject import GameObject

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface 

import pygame as py

class Wall(GameObject):
    path = "./images/wall.png"
    wallImage = py.image.load(path)
    def __init__(self):
        '''
            Params  : (None)
            Purpose : Creates a wall
        '''
        super().__init__(None)

    @staticmethod 
    def convertImage():
        '''
            Params  : (None)
            Purpose : Converts the surface into an image which is easier to render
            Return  : (None)
        '''
        Wall.wallImage = Wall.wallImage.convert()

    def getSurface(self) -> Surface | None:
        '''
            Params  : (None)
            Purpose : Gets the image for the object to render
            Return  : (Surface) The display of the object
        '''
        return self.wallImage
    
    def pack(self) -> tuple[str, dict[str, str]]:
        '''
            Params  : (None)
            Purpose : Packs the object to cross the erlang channel
            Return  : (["wall", Message]) The packed object
        '''
        return ("wall", dict())
    
    def unpack(self, info : dict):
        '''
            Params  : (dict) info := The data from the object
            Purpose : Unpacks the object from the erlang channel
            Return  : (self) The object with all the information
        '''
        return self