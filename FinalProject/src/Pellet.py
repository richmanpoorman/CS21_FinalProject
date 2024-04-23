from Interactable import Interactable
from Player import Player 

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
import pygame as py

class Pellet(Interactable):
    path = "./images/pellet.png"
    pelletImage = py.image.load(path)
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        #Example for sanity purpose
        suf = py.Surface((20, 20))
        super().__init__()

    def onGet(self, player : Player) -> str:
        return "pellet_pickup"
    
    @staticmethod 
    def convertImage():
        Pellet.pelletImage = Pellet.pelletImage.convert()


    def getSurface(self) -> Surface | None:
        return self.pelletImage
    
    def pack(self) -> tuple[str, dict[str, str]]:
        return ("pellet", dict())
    
    def unpack(self, info):
        return self