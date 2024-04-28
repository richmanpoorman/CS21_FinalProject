
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from typing import Any

class GameObject:

    def __init__(self, surface : pygame.Surface | None = None):
        '''
            Params  : (Surface) The inital image 
            Purpose : Creates an object
        '''
        if surface:
            self.setSurface(surface)

    @staticmethod 
    def convertImage():
        '''
            Params  : (None)
            Purpose : Converts the surface into an image which is easier to render
            Return  : (None)
        '''
        pass

    def getSurface(self) -> pygame.Surface: 
        '''
            Params  : (None)
            Purpose : Gets the image for the object to render
            Return  : (Surface) The display of the object
        '''
        return self.surface

    def setSurface(self, surface : pygame.Surface) -> None:
        '''
            Params  : (Surface) The surface to set
            Purpose : Update the surface to return 
            Return  : (None)
            Note    : THIS FEATURE IS DEPRECIATED; IT IS BETTER TO OVERRIDE
                      THE getSurface FUNCTION FOR EACH SUBCLASS
        '''
        self.surface = surface

    def pack(self) -> tuple[str, dict[str, Any]]: 
        '''
            Params  : (None)
            Purpose : Packs the object to cross the erlang channel
            Return  : ([ClassName, Message]) The packed object
        '''
        return ("", dict())
    
    def unpack(self, info : dict[str, Any]):
        '''
            Params  : (dict) info := The data from the object
            Purpose : Unpacks the object from the erlang channel
            Return  : (self) The object with all the information
        '''
        return self

    @staticmethod
    def defaultPack() -> tuple[str, dict[str, Any]]:
        '''
            Params  : (None)
            Purpose : The default for unpacking
            Return  : (["", dict]) Represents an empty object
        '''
        return ("", dict())