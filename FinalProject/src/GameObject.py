
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame
class GameObject:
    def __init__(self, surface : pygame.Surface | None = None):
        if surface:
            self.setSurface(surface)

    def getSurface(self) -> pygame.Surface: 
        return self.surface

    def setSurface(self, surface : pygame.Surface) -> None:
        self.surface = surface

    def pack(self) -> tuple[str, str]: 
        return ("", "")
    
    @staticmethod
    def unpack(data):
        pass