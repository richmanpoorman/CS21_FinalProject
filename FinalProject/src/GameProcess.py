from Board import Board
from Player import Player
from Ghost import Ghost 
from Interactable import Interactable
from Pellet import Pellet 
from PowerPellet import PowerPellet

from Wall import Wall

from random import randrange

from TestTools import outputLn

class GameProcess:
    def __init__(self, board : Board = Board(), isRandom = False):
        self.board = board
        self.numPellets = 5
        self.numPowerPellets = 2
        if isRandom:
            self.__makeRandomBoard()

    def __makeRandomBoard(self):
        numWalls = 20
        for _ in range(numWalls):
            self.board.addObject(Wall(), self.__getBlankSpot())
        
        numGhosts = 5 
        for _ in range(numGhosts):
            self.board.addObject(Ghost(), self.__getBlankSpot())

        for _ in range(self.numPellets):
            self.board.addObject(Pellet(), self.__getBlankSpot())

        for _ in range(self.numPowerPellets):
            self.board.addObject(PowerPellet(), self.__getBlankSpot())


    def updateBoard(self):
        self.__moveGhosts()
        self.__decrementInvincibility()
        self.__moveAllPlayers()

    def getBoard(self):
        return self.board.getBoard()

    def playerMove(self, playerID : int, direction : tuple) -> None:
        if not self.board.isIn(playerID):
            return
        self.board.getObject(playerID).setGoingTo(direction)

    def __moveAllPlayers(self):
        players = self.board.getAllOfType(Player)
        for playerID, player in players:
            direction = player.goingTo()
            if direction != Player.NEUTRAL:
                self.__playerMoveObject(playerID, direction)

    def __playerMoveObject(self, playerID : int, direction : tuple):
        if not self.board.isIn(playerID):
            return
        
        playerPos = self.board.getPosition(playerID) 
        newPos    = self.__moveWrap(direction, playerPos) 

        canMove, atSpot = self.board.canMoveTo(newPos) 
        
        if canMove:
            if atSpot:
                self.__pickUp(atSpot, playerID)
            self.board.moveObject(playerID, newPos) 
        else: 
            outputLn("Player sees: " + str(self.board.getObject(atSpot)))
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
                    self.__ghostDie(atSpot)
                    self.board.moveObject(playerID, newPos)
                else:
                    self.playerDie(playerID)

    def __moveGhosts(self) -> None:
        ghosts = [id for id, _ in self.board.getAllOfType(Ghost)]
        for ghostID in ghosts:
            self.__moveSingleGhost(ghostID)
        
    
    def __moveSingleGhost(self, ghostID : int) -> None:
        if not self.board.isIn(ghostID):
            return 
        direction = self.__ghostAI(ghostID)
        position  = self.board.getPosition(ghostID)
        if direction == (0, 0):
            return 
        
        newPos = self.__moveWrap(direction, position)
        
        canMove, atSpot = self.board.canMoveTo(newPos) 
        if canMove:
            self.board.moveObject(ghostID, newPos) 
        else:
            # outputLn(str(self.board.getObject(atSpot)))
            if self.board.isObjectOfType(atSpot, Player):
                player : Player = self.board.getObject(atSpot)
                if not player.isInvincible():
                    self.playerDie(atSpot) 
                    self.board.moveObject(ghostID, newPos)

        self.board.getObject(ghostID).setFacing(direction)
    
    def __ghostAI(self, ghostID : int) -> tuple[int, int]:
        if not self.board.isIn(ghostID):
            return (0, 0)
        
        directions = [( 0,  1),
                      ( 1,  0),
                      ( 0, -1),
                      (-1,  0)]
        return directions[randrange(0, len(directions))]
    
    def playerDie(self, playerID : int) -> None:
        if not self.board.isIn(playerID):
            return
        self.board.removeObject(playerID)
    
    def __ghostDie(self, ghostID : int) -> None:
        if not self.board.isIn(ghostID):
            return
        ### TODO :: CHANGE THE GHOST SPAWN LOCATION
        self.board.moveObject(ghostID, self.__getBlankSpot())
    
    def addPlayer(self) -> int:
        spot = self.__getBlankSpot()
        playerID = self.board.addObject(Player(), spot)
        return playerID
    
    def __pickUp(self, interactableID : int, playerID : int) -> None:
        if not self.board.isIn(interactableID) or not self.board.isIn(playerID):
            return
        
        interactable : Interactable = self.board.getObject(interactableID)
        player       : Player       = self.board.getObject(playerID)
        interactable.onGet(player)
        self.board.removeObject(interactableID)

        self.__checkAndSpawnPellets()
    

    def __checkAndSpawnPellets(self):
        pelletCount = len(self.board.getAllOfType(Interactable))
        if pelletCount != 0: 
            return 
        
        for _ in range(self.numPellets):
            self.board.addObject(Pellet(), self.__getBlankSpot())
        
        for _ in range(self.numPowerPellets):
            self.board.addObject(PowerPellet(), self.__getBlankSpot())
        

    def __decrementInvincibility(self) -> None:
        players = self.board.getAllOfType(Player)
        for _, player in players:
            player.decrementInvincibleTimer()
    
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
