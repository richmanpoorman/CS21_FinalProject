from Player import Player 
from GameObject import GameObject 

class Interactable(GameObject):
    def __init__(self, surface : tuple):
        super().__init__(surface)
        pass 

    def onGet(self, player : Player) -> None:
        pass