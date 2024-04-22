from Interactable import Interactable
from Player import Player 

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface 

import pygame as py

class PowerPellet(Interactable):
    path = "./images/power-pellet.png"
    powerPelletImage = py.image.load(path)
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__()
        

    def onGet(self, player : Player) -> str:
        player.setInvincible()
        return "set_invincible"
    
    def getSurface(self) -> Surface | None:
        return self.powerPelletImage
    

    def pack(self) -> tuple[str, dict[str, str]]:
        return ("powerpellet", dict()) 
    
    def unpack(self, info):
        return self