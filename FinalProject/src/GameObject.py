
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame

from typing import Any

class GameObject:
    UP, DOWN, LEFT, RIGHT, NEUTRAL = (-1, 0), (1, 0), (0, -1), (0, 1), (0, 0)
    def __init__(self, surface : pygame.Surface | None = None):
        self.facing    = GameObject.RIGHT
        self.direction = GameObject.NEUTRAL
        if surface:
            self.setSurface(surface)

    def setFacing(self, direction : tuple):
        self.facing = direction 

    def setDirection(self, direction : tuple) -> None:
        self.direction = direction

    def setGoingTo(self, direction : tuple):
        self.setFacing(direction)
        self.setDirection(direction)
    
    def setStuck(self) -> None:
        self.direction = self.NEUTRAL

    def goingTo(self) -> tuple:
        return self.direction 
    
    def getFacing(self) -> tuple: 
        return self.facing

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