from GameObject import GameObject
from Board import Board 

class Ghost(GameObject):
    def __init__(self, position : tuple, surface : tuple):
        super().__init__(position, surface)
        pass 

    def move(self, board : Board) -> None:
        pass 

    def die(self) -> None:
        pass 