from GameObject import GameObject
from Player import Player

from random import randrange

class Ghost(GameObject):
    def __init__(self, surface : tuple):
        super().__init__(surface)
        pass 
