from Interactable import Interactable
from Player import Player 

class PowerPellet(Interactable):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)
        

    def onGet(self, player : Player) -> str:
        player.setInvincible()
        return "set_invincible"