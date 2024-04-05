from GameObject import GameObject
from Player import Player
from Board import Board 

from random import randrange

class Ghost(GameObject):
    __DIRECTIONS = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def __init__(self, surface : tuple):
        super().__init__(surface)
        pass 

    @staticmethod
    def move(board : Board, position : tuple) -> tuple:
        boardSize = board.getSize()
        newPosition = Ghost.__goInDirection(boardSize)
        canGoTo, blocker = board.canMoveTo(newPosition)
        while not canGoTo and not isinstance(board.getObject(blocker), Player):
            newPosition = Ghost.__goInDirection(boardSize)
        return newPosition

    def die(self) -> None:
        pass 
    
    @staticmethod
    def __goInDirection(boardSize : tuple, position : tuple) -> tuple:
        w, h = boardSize 
        x, y = position
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