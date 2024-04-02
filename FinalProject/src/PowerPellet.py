from Interactable import Interactable
from Player import Player 

class PowerPellet(Interactable):
    def __init__(self, surface : tuple):
        super().__init__(surface)
        pass 

    def onGet(self, player : Player) -> None:
        player.setInvincible()