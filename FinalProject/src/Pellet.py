from Interactable import Interactable
from Player import Player 

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
import pygame as py

class Pellet(Interactable):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        #Example for sanity purpose
        suf = py.Surface((20, 20))
        super().__init__()

    def onGet(self, player : Player) -> str:
        return "pellet_pickup"
    
    def getSurface(self) -> Surface | None:
        surface = Surface((200, 200))
        surface.fill((0, 200, 0))
        return surface