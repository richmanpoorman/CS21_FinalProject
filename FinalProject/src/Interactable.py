from Player import Player 
from GameObject import GameObject 

class Interactable(GameObject):
    def __init__(self, position : tuple, surface : tuple):
        super().__init__(position, surface)
        pass 

    def onGet(self, player : Player) -> None:
        pass