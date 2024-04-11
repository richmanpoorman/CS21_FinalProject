from Interactable import Interactable
from Player import Player 
from pygame import Surface

class Pellet(Interactable):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__()

    def onGet(self, player : Player) -> str:
        return "pellet_pickup"
    
    def getSurface(self) -> Surface | None:
        surface = Surface((200, 200))
        surface.fill((0, 200, 0))
        return surface