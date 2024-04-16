from Interactable import Interactable
from Player import Player 

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface 

class PowerPellet(Interactable):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__()
        

    def onGet(self, player : Player) -> str:
        player.setInvincible()
        return "set_invincible"
    
    def getSurface(self) -> Surface | None:
        surface = Surface((200, 200))
        surface.fill((200, 100, 0))
        return surface