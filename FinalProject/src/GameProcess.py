from Board import Board
from Player import Player
from Ghost import Ghost 
from Interactable import Interactable

from Wall import Wall

from random import randrange

class GameProcess:
    def __init__(self, board : Board = Board(), isRandom = False):
        self.board = board
        if isRandom:
            self.__makeRandomBoard()

    def __makeRandomBoard(self):
        numWalls = 20
        for _ in range(numWalls):
            self.board.addObject(Wall(), self.__getBlankSpot())
        
        numGhosts = 5 
        for _ in range(numGhosts):
            self.board.addObject(Ghost(), self.__getBlankSpot())


    def updateBoard(self):
        self.__moveGhosts()
        self.__decrementInvincibility()

    def getBoard(self):
        return self.board.getBoard()

    def playerMove(self, playerID : int, direction : tuple) -> None:
        playerPos = self.board.getPosition(playerID) 
        newPos    = self.__moveWrap(direction, playerPos) 

        canMove, atSpot = self.board.canMoveTo(newPos) 

        if canMove:
            self.board.moveObject(playerID, newPos) 
            if atSpot:
                self.__pickUp(atSpot, playerID)
        else: 
            if self.board.isObjectOfType(atSpot, Player):
                p1 : Player = self.board.getObject(playerID)
                p2 : Player = self.board.getObject(atSpot)
                if p1.isInvincible() and not p2.isInvincible():
                    self.playerDie(atSpot)
                    self.board.moveObject(playerID, newPos)
                elif p2.isInvincible() and not p1.isInvincible():
                    self.playerDie(playerID)
            elif self.board.isObjectOfType(atSpot, Ghost):
                player : Player = self.board.getObject(playerID)
                
                if player.isInvincible():
                    self.board.moveObject(playerID, newPos)
                    self.__ghostDie(atSpot)
                else:
                    self.playerDie(playerID)

    def __moveGhosts(self) -> None:
        ghosts = [id for id, _ in self.board.getAllOfType(Ghost)]
        for ghostID in ghosts:
            self.__moveSingleGhost(ghostID)
        
    
    def __moveSingleGhost(self, ghostID : int) -> None:
        direction = self.__ghostAI(ghostID)
        position  = self.board.getPosition(ghostID)
        if direction == (0, 0):
            return 
        
        newPos = self.__moveWrap(direction, position)
        
        canMove, atSpot = self.board.canMoveTo(newPos) 
        if canMove:
            self.board.moveObject(ghostID, newPos) 
        else:
            if self.board.isObjectOfType(atSpot, Player):
                player : Player = self.board.getObject(atSpot)
                if not player.isInvincible():
                    self.playerDie(atSpot) 
                    self.board.moveObject(ghostID, newPos)
    
    def __ghostAI(self, ghostID : int) -> tuple[int, int]:
        directions = [( 0,  1),
                      ( 1,  0),
                      ( 0, -1),
                      (-1,  0)]
        return directions[randrange(0, len(directions))]
    
    def playerDie(self, playerID : int) -> None:
        self.board.removeObject(playerID)
    
    def __ghostDie(self, ghostID : int) -> None:
        self.board.moveObject(ghostID, (5, 5))
    
    def addPlayer(self) -> int:
        spot = self.__getBlankSpot()
        playerID = self.board.addObject(Player(), spot)
        return playerID
    
    def __pickUp(self, interactableID : int, playerID : int) -> None:
        interactable : Interactable = self.board.getObject(interactableID)
        player       : Player       = self.board.getObject(playerID)
        interactable.onGet(player)
    
    def __decrementInvincibility(self) -> None:
        pass
    
    def __getBlankSpot(self) -> tuple[int, int]:
        possibleSpots = self.__findBlankSpots()
        spot = possibleSpots[randrange(0, len(possibleSpots))]
        return spot

    def __findBlankSpots(self) -> list[tuple[int, int]]:
        board = self.getBoard()
        w, h = board.shape

        emptySpots : list[tuple[int, int]]= []
        for r in range(w):
            for c in range(h):
                if not board[r, c]:
                    emptySpots.append((r, c))

        return emptySpots

    def __moveWrap(self, direction : tuple[int, int], position : tuple[int, int]) -> tuple[int, int]:
        w , h  = self.board.getSize() 
        dx, dy = direction 
        x , y  = position 
        newX, newY = x + dx, y + dy 

        return ((newX + w) % w, (newY + h) % h)
