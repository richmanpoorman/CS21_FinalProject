
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from typing import Any

class GameObject:

    def __init__(self, surface : pygame.Surface | None = None):
        if surface:
            self.setSurface(surface)


    @staticmethod 
    def convertImage():
        pass

    def getSurface(self) -> pygame.Surface: 
        return self.surface

    def setSurface(self, surface : pygame.Surface) -> None:
        self.surface = surface

    def pack(self) -> tuple[str, dict[str, Any]]: 
        return ("", dict())
    
    def unpack(self, data : dict[str, Any]):
        return self

    @staticmethod
    def defaultPack() -> tuple[str, dict[str, Any]]:
        return ("", dict())