from GameObject import GameObject
from Board import Board 

from random import randrange

class Ghost(GameObject):
    __DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, position : tuple, surface : tuple):
        super().__init__(position, surface)
        pass 

    def move(self, board : Board) -> None:
        boardSize = board.getSize()
        newPosition = self.__goInDirection(boardSize)
        while not board.canMoveTo(newPosition):
            newPosition = self.__goInDirection(boardSize)
        self.setPosition(newPosition)

    def die(self) -> None:
        pass 

    def __goInDirection(self, boardSize : tuple):
        w, h = boardSize 
        x, y = self.getPosition() 
        dx, dy = randrange(0, len(Ghost.__DIRECTIONS))
        newX, newY = x + dx, y + dy 
        
        # Wrap if going off of the board
        if newX < 0:
            newX = w - 1 
        elif newX >= w:
            newX = 0 
        elif newY < 0:
            newY = h - 1 
        elif newY >= h:
            newY = 0

        return (newX, newY)