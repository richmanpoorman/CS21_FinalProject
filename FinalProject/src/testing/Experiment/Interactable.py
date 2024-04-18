from Player import Player 
from GameObject import GameObject 

class Interactable(GameObject):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)

    def onGet(self, player : Player) -> str:
        pass