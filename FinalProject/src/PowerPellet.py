from Interactable import Interactable
from Player import Player 

class PowerPellet(Interactable):
    def __init__(self, position : tuple, surface : tuple):
        super().__init__(position, surface)
        pass 

    def onGet(self, player : Player) -> None:
        pass