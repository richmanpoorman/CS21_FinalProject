from Player import Player 
from GameObject import GameObject 

class Interactable(GameObject):
    def __init__(self):
        '''
            Params  : (None) 
            Purpose : Creates an interactable
        '''
        super().__init__(None)

    def onGet(self, player : Player) -> str:
        '''
            Params  : (Player) player := The player that picked up the object
            Purpose : Does something when picked up by a player
            Return  : The name of the interactable
        '''
        pass