from GameObject import GameObject
from Player import Player

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
from random import randrange

class Ghost(GameObject):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)

    def getSurface(self) -> Surface | None:
        surface = Surface((200, 200))
        surface.fill((200, 0, 200))
        return surface