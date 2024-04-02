from Interactable import Interactable
from Player import Player 

class Pellet(Interactable):
    def __init__(self, surface : tuple):
        super().__init__(surface)
        pass 

    def onGet(self, player : Player) -> None:
        pass