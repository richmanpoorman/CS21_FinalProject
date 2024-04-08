from GameObject import GameObject
from Player import Player

from random import randrange

class Ghost(GameObject):
    def __init__(self):
        # TODO:: Replace the surface with the starting image
        super().__init__(None)