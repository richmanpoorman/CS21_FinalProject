from Board import Board
from Player import Player
from Ghost import Ghost 
from Interactable import Interactable
from Pellet import Pellet 
from PowerPellet import PowerPellet

from Wall import Wall

from random import randrange
from random import choice
from TestTools import outputLn

from BoardBuilder import makeBoardFromImage
from GhostAI import searchAndFind, moveForwardIfPossible

class GameProcess:
    NUM_PELLETS = 80
    NUM_POWER_PELLETS = 20
    NUM_GHOSTS = 12
    def __init__(self, board : Board | None = None, isRandom = False):
        '''
            Params  : (Board) board    := [OPTIONAL] An initial set up 
                      (bool)  isRandom := [OPTIONAL] randomizes the set up
            Purpose : Creates a new logic module 
        '''
        self.timer    = 0
        if board:
            self.board = board
        elif isRandom:
            self.board = Board()
            self.__makeRandomBoard()
        else:
            self.__makeDefaultBoard()
        
        
    def __makeDefaultBoard(self):
        '''
            Params  : (None)
            Purpose : Creates a default board to run with
            Return  : (None)
        '''
        boardPath = "./images/BoardSetup2.png"
        self.board, _ = makeBoardFromImage(boardPath)
        for _ in range(self.NUM_GHOSTS):
            self.board.addObject(Ghost(), self.__getBlankSpot())

        for _ in range(self.NUM_PELLETS):
            self.board.addObject(Pellet(), self.__getBlankSpot())

        for _ in range(self.NUM_POWER_PELLETS):
            self.board.addObject(PowerPellet(), self.__getBlankSpot())

    def __makeRandomBoard(self):
        '''
            Params  : (None)
            Purpose : Creates a random board to run with
            Return  : (None)
        '''
        numWalls = 20
        for _ in range(numWalls):
            self.board.addObject(Wall(), self.__getBlankSpot())
        
        for _ in range(self.NUM_GHOSTS):
            self.board.addObject(Ghost(), self.__getBlankSpot())

        for _ in range(self.NUM_PELLETS):
            self.board.addObject(Pellet(), self.__getBlankSpot())

        for _ in range(self.NUM_POWER_PELLETS):
            self.board.addObject(PowerPellet(), self.__getBlankSpot())


    def updateBoard(self):
        '''
            Params  : (None)
            Purpose : Runs one update step
            Return  : (None)
        '''
        if self.timer % 3 == 0:
            self.__moveGhosts()
        
        if self.timer % 2 == 0:
            self.__moveAllPlayers()
            self.__decrementInvincibility()
            
        self.timer += 1

    def getBoard(self):
        '''
            Params  : (None)
            Purpose : Gets the whole board
            Return  : (ndarray) The board of game objects
        '''
        return self.board.getBoard()

    def playerMove(self, playerID : int, direction : tuple) -> None:
        '''
            Params  : (ID)         playerID  := The player to move
                      ([int, int]) direction := The direction the 
                                                player tries to move
            Purpose : Receives input from player to try to move to a direction
            Return  : (None)
        '''
        if not self.board.isIn(playerID):
            return
        self.board.getObject(playerID).setGoingTo(direction)

    def __moveAllPlayers(self):
        '''
            Params  : (None)
            Purpose : Moves all the players in the direction that 
                      they are facing
            Return  : (None)
        '''
        players = self.board.getAllOfType(Player)
        for playerID, player in players:
            direction = player.getFacing()
            if direction != Player.NEUTRAL:
                self.__playerMoveObject(playerID, direction)

    def __playerMoveObject(self, playerID : int, direction : tuple):
        '''
            Params  : (ID)         playerID  := The player to move
                      ([int, int]) direction := The direction the 
                                                players try to move
            Purpose : Tries to move the player, and updates the 
                      board state when they move
            Return  : (None)
        '''
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
            if self.board.isObjectOfType(atSpot, Player):
                # If the 2 players collide with each other

                p1 : Player = self.board.getObject(playerID)
                p2 : Player = self.board.getObject(atSpot)
                if p1.isInvincible() and not p2.isInvincible():
                    self.playerDie(atSpot)
                    self.board.moveObject(playerID, newPos)
                elif p2.isInvincible() and not p1.isInvincible():
                    self.playerDie(playerID)
            elif self.board.isObjectOfType(atSpot, Ghost):
                # If a player runs into a ghost
                player : Player = self.board.getObject(playerID)
                if player.isInvincible():
                    self.__ghostDie(atSpot)
                    self.board.moveObject(playerID, newPos)
                else:
                    self.playerDie(playerID)

    def __moveGhosts(self) -> None:
        '''
            Params  : (None)
            Purpose : Moves all of the ghosts in the board
            Return  : (None)
        '''
        ghosts = [id for id, _ in self.board.getAllOfType(Ghost)]
        for ghostID in ghosts:
            self.__moveSingleGhost(ghostID)
        
    
    def __moveSingleGhost(self, ghostID : int) -> None:
        '''
            Params  : (ID) ghostID := The ghost to move
            Purpose : Moves the ghost according to the AI and 
                      updates the board state
            Return  : (None)
        '''
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
            # If a ghost runs into a player
            if self.board.isObjectOfType(atSpot, Player):
                player : Player = self.board.getObject(atSpot)
                if not player.isInvincible():
                    self.playerDie(atSpot) 
                    self.board.moveObject(ghostID, newPos)

        self.board.getObject(ghostID).setFacing(direction)
    
    def __ghostAI(self, ghostID : int) -> tuple[int, int]:
        '''
            Params  : (ID) ghostID := The ghost to do the AI on
            Purpose : Uses the ghost AI to return a direction to move
            Return  : ([int, int]) The direction to move
        '''
        if not self.board.isIn(ghostID):
            return (0, 0)
         # searchAndFind(ghostID, self.board)
        return moveForwardIfPossible(ghostID, self.board)

    
    def playerDie(self, playerID : int) -> None:
        '''
            Params  : (ID) playerID := The ID of the player that died
            Purpose : Kills a player, and does the updates
            Return  : (None)
        '''
        if not self.board.isIn(playerID):
            return
        self.board.removeObject(playerID)
    
    def __ghostDie(self, ghostID : int) -> None:
        '''
            Params  : (ID) ghostID := The ID of the ghost that died
            Purpose : Kills a ghost, and does the updates
            Return  : (None)
        '''
        if not self.board.isIn(ghostID):
            return
        ### TODO :: CHANGE THE GHOST SPAWN LOCATION
        self.board.moveObject(ghostID, self.__getBlankSpot())
    
    def addPlayer(self) -> int:
        '''
            Params  : (None)
            Purpose : Creates a new player in the game
            Return  : (ID) The ID of the newly created character
        '''
        spot = self.__getBlankSpot()
        playerID = self.board.addObject(Player(), spot)
        return playerID
    
    def __pickUp(self, interactableID : int, playerID : int) -> None:
        '''
            Params  : (ID) interactableID := The ID of the interactable
                      (ID) playerID       := The ID of the player that picked up
                                             the interactable
            Purpose : Do the updates when the player tries to 
                      pick up an interactable
            Return  : (None)
        '''
        if not self.board.isIn(interactableID) or not self.board.isIn(playerID):
            return
        
        interactable : Interactable = self.board.getObject(interactableID)
        player       : Player       = self.board.getObject(playerID)
        interactable.onGet(player)
        self.board.removeObject(interactableID)

        self.__checkAndSpawnPellets()
    

    def __checkAndSpawnPellets(self):
        '''
            Params  : (None)
            Purpose : Checks if there are no pellets left; if there aren't, 
                      spawn all of the pellets again
            Return  : (None)
        '''
        pelletCount = len(self.board.getAllOfType(Interactable))
        if pelletCount != 0: 
            return 
        
        for _ in range(self.NUM_PELLETS):
            self.board.addObject(Pellet(), self.__getBlankSpot())
        
        for _ in range(self.NUM_POWER_PELLETS):
            self.board.addObject(PowerPellet(), self.__getBlankSpot())
        

    def __decrementInvincibility(self) -> None:
        '''
            Params  : (None)
            Purpose : Decrement the invincibility timer of all players
            Return  : (None)
        '''
        players = self.board.getAllOfType(Player)
        for _, player in players:
            player.decrementInvincibleTimer()
    
    def __getBlankSpot(self) -> tuple[int, int]:
        '''
            Params  : (None)
            Purpose : Finds a random blank spot on the board
            Return  : ([int, int]) The position of the blank spot
        '''
        possibleSpots = self.__findBlankSpots()
        spot = possibleSpots[randrange(0, len(possibleSpots))]
        return spot

    def __findBlankSpots(self) -> list[tuple[int, int]]:
        '''
            Params  : (None)
            Purpose : Finds all blank spots on the board
            Return  : (list) The list of all of the blank spots
        '''
        board = self.getBoard()
        w, h = board.shape

        emptySpots : list[tuple[int, int]] = []
        for r in range(w):
            for c in range(h):
                if not board[r, c]:
                    emptySpots.append((r, c))

        return emptySpots

    def __moveWrap(self, direction : tuple[int, int], 
                   position : tuple[int, int]) -> tuple[int, int]:
        '''
            Params  : ([int, int]) direction := The direction to move
                      ([int, int]) position  := The starting position
            Purpose : Moves the object, wrapping around the board if necessary
            Return  : ([int, int]) The position to end up at
        '''
        w , h  = self.board.getSize() 
        dx, dy = direction 
        x , y  = position 
        newX, newY = x + dx, y + dy 

        return ((newX + w) % w, (newY + h) % h)
