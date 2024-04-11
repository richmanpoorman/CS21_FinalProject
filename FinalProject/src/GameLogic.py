from erpy import stdio_port_connection
from term import Atom, Pid
from random import randrange

from Board import Board
from Ghost import Ghost
from Player import Player
from Interactable import Interactable

class GameLogic:
    def __init__(self, board = Board()):
        self.board = board
        self.isRunning = True
        self.inbox, self.port = stdio_port_connection() 
        self.playerIDs = dict()
        self.updateQueue = []
        self.run()

    ### SEND BOARD INFORMATION TO ALL USERS ### 
    def setUpBoard(self):
        pass
    
    def sendFullBoardState(self):
        pass 

    ### RECEIEVE MESSAGES ###
    def updateModel(self) -> None:
        for msg in self.inbox:
            pid, command = msg 

            if command == Atom("close"):
                self.onClose()
            elif command == Atom("player_join"):
                self.onJoin(pid)
            elif command == Atom("up"):
                self.onPlayerMove(pid, Player.UP)
            elif command == Atom("down"):
                self.onPlayerMove(pid, Player.DOWN)
            elif command == Atom("left"):
                self.onPlayerMove(pid, Player.LEFT)
            elif command == Atom("right"):
                self.onPlayerMove(pid, Player.RIGHT)
            
    def onPlayerMove(self, pid : Pid, direction : tuple) -> None:
        player = self.playerIDs[pid]
        newPosition = \
            self.movePlayer(direction, 
                            self.board.getPosition(self.playerIDs[pid]))
        
        canMove, blocker = self.board.canMoveTo(newPosition)

        if canMove: 
            self.board.moveObject(player, newPosition)
            self.tryToPickUp(blocker, player)
        else: 
            if not blocker:
                return

            playerObject = self.board.getObject(player)
            isInvincible = playerObject.isInvincible()
            
            if self.board.isObjectOfType(blocker, Ghost):
                if isInvincible:
                    self.ghostDie(blocker)
                else:
                    self.playerDie(player)
            elif self.board.isObjectOfType(blocker, Player):
                blockedBy = self.board.getObject(blocker)
                if isInvincible and not blockedBy.isInvincible():
                    self.playerDie(blocker)
    
    def movePlayer(self, dir : tuple, position : tuple) -> tuple:
        w , h  = self.board.getSize()
        dx, dy = dir 
        x , y  = position
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
    ### RUN NON-PLAYER LOGIC GAME LOGIC ###

    def runLogic(self) -> None:
        self.moveAllGhosts()
        self.decrementPlayerTimers()

    def moveAllGhosts(self) -> None:
        ghosts = self.board.getAllOfType(Ghost)
        for ghostID, _ in ghosts: 
            self.moveGhost(ghostID)
    
    def moveGhost(self, ghostID : int) -> None:
        attemptCounter = 0
        while attemptCounter < 1000:
            newPosition = self.moveGhostAttempt(ghostID)
            canMove, blocker = self.board.canMoveTo(newPosition)
            if canMove:
                self.board.moveObject(ghostID, newPosition)
                return 
            
            blockedBy = self.board.getObject(blocker) 

            if self.board.isObjectOfType(blocker, Player):
                if blockedBy.isInvincible():
                    self.ghostDie(ghostID)
                else:
                    self.playerDie(blocker)
                    self.board.moveObject(ghostID, newPosition)
                return
            
            attemptCounter += 1

    
    def moveGhostAttempt(self, ghostID : int) -> tuple:
        directions = ((0, 1), (1, 0), (0, -1), (-1, 0))
        w, h = self.board.getSize()
        x, y = self.board.getPosition(ghostID)
        dx, dy = directions[randrange(0, len(directions))]
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
    ### STATE UPDATES ### 

    def playerDie(self, playerID : int) -> None:
        self.updateQueue.append((Atom("player_die"), {"id" : playerID}))
    
    def ghostDie(self, ghostID : int) -> None: 
        self.updateQueue.append((Atom("ghost_die"), {"id" : ghostID}))
    
    def onClose(self) -> None:
        self.isRunning = False
        self.updateQueue.append((Atom("quit"), dict()))

    def onJoin(self, pid : Pid) -> None:
        self.playerIDs[pid] = self.board.addObject(Player(), (0, 0))
        self.updateQueue.append((Atom("player_join"), {"id" : self.playerIDs[pid]}))

    def tryToPickUp(self, interactable : int, player : int) -> None:
        if not interactable:
            return 
        if self.board.isObjectOfType(interactable, Interactable):
            blockerObject = self.board.getObject(interactable)
            pickupType = blockerObject.onGet(self.board.getObject(player))
            self.updateQueue.append((Atom(pickupType), {"id" : interactable, 
                                                         "playerID" : player}))

    def decrementPlayerTimers(self) -> None:
        players = self.board.getAllOfType(Player)
        for playerID, player in players:
            isPreviouslyInvincible = player.isInvincible()
            isInvincible = player.decrementInvincibleTimer()
            
            if isPreviouslyInvincible and not isInvincible:
                self.updateQueue.append((Atom("player_vulnerable"), {"id" : playerID}))
    
    ### SEND MESSAGES ###

    def sendUpdates(self) -> None: 
        for msg in self.updateQueue:
            self.port.send(msg)
        self.updateQueue = []

    def run(self) -> None:
        while self.isRunning: 
            self.updateModel()
            self.runLogic()
            self.sendUpdates() 


GameLogic()