from Board import Board

class GameProcess:
    def __init__(self, board : Board = Board()):
        self.board = board

    def getBoard(self):
        return self.board.getBoard()

    def playerMove(self, playerID : int, direction : tuple) -> None:
        playerPos = self.board.getPosition(playerID) 
        newPos    = self.__moveWrap(direction, playerPos) 

        canMove, atSpot = self.board.canMoveTo(newPos) 

        if canMove:
            self.board.moveObject(playerID, newPos) 
            if atSpot:
                self.pickUp(atSpot, playerID)

    
    def moveGhosts(self) -> None:
        pass
    
    def __moveSingleGhost(self) -> None:
        pass
    
    def __ghostAI(self) -> tuple[int, int]:
        return (0, 0)
    
    def playerDie(self, playerID : int) -> None:
        pass 
    
    def ghostDie(self, ghostID : int) -> None:
        pass
    
    def addPlayer(self) -> None:
        pass
    
    def pickUp(self, interactableID : int, playerID : int) -> None:
        pass
    
    def decrementInvincibility(self) -> None:
        pass

    def __moveWrap(self, direction : tuple[int, int], position : tuple[int, int]) -> tuple[int, int]:
        w , h  = self.board.getSize() 
        dx, dy = direction 
        x , y  = position 
        newX, newY = x + dx, y + dy 

        return ((newX + w) % w, (newY + h) % h)
