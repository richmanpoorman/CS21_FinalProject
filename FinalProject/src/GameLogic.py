from erpy import stdio_port_connection
from term import Atom, Pid
from random import randrange

from Board import Board
from Ghost import Ghost
from Player import Player
from Interactable import Interactable

from threading import Thread, Lock

## TESTING FUNCTIONS
from TestTools import outputInit, outputLn
class GameLogic:
    POSITION_DICT = {
        "up"    : ( 0,  1), 
        "down"  : ( 0, -1),
        "left"  : (-1,  0),
        "right" : ( 1,  0)
    }

    def __init__(self, board = Board()):
        ## TESTING 
        outputInit()
        outputLn("Server Start")
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

    def updateModel(self, msg) -> None:  
        outputLn("SERVER RECEIEVED SOME MESSAGE")
        match msg:
            case (pid, command, info):
                self.parseMessage(pid, command, info)
            case _:
                outputLn("Unknown message received")
    
    def parseMessage(self, pid, command, info):
        outputLn("SERVER RECEIVES: " + str(command) + str(info))
        match command:
            case "close":
                # self.onClose()
                outputLn("Closing")
            case "input":
                # self.onPlayerMove(pid, GameLogic.POSITION_DICT[info["direction"]])
                outputLn("input of: " + str(info))
            case "player_join":
                # self.onJoin(pid)
                outputLn("player join of: " + str(info))
            case "done":
                outputLn("Server Done")
                self.isRunning = False
            case "py_port":
                outputLn(command + " " + info)
            case _: 
                outputLn("No match was found")
            
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

            playerObject : Player = self.board.getObject(player)
            isInvincible = playerObject.isInvincible()
            
            if self.board.isObjectOfType(blocker, Ghost):
                if isInvincible:
                    self.ghostDie(blocker)
                else:
                    self.playerDie(player)
            elif self.board.isObjectOfType(blocker, Player):
                blockedBy : Player = self.board.getObject(blocker)
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
                player : Player = blockedBy
                if player.isInvincible():
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
        info = {"id" : playerID}
        self.queueMessage("player_die", info)
    
    def ghostDie(self, ghostID : int) -> None: 
        info = {"id" : ghostID}
        self.queueMessage("ghost_die", info)
    
    def onClose(self) -> None:
        self.isRunning = False
        self.queueMessage("done", dict())

    def onJoin(self, pid : Pid) -> None:
        self.playerIDs[pid] = self.board.addObject(Player(), (0, 0))
        info = {"id" : self.playerIDs[pid]}
        self.queueMessage("player_join", info)

    def tryToPickUp(self, interactable : int, player : int) -> None:
        if not interactable:
            return 
        if self.board.isObjectOfType(interactable, Interactable):
            blockerObject = self.board.getObject(interactable)
            blockerObject.onGet(self.board.getObject(player))
            info = {"id" : interactable, "playerID" : player}
            self.queueMessage("remove_object", info)

    def decrementPlayerTimers(self) -> None:
        players : list = self.board.getAllOfType(Player)
        for playerID, player in players:
            isPreviouslyInvincible = player.isInvincible()
            isInvincible = player.decrementInvincibleTimer()
            
            if isPreviouslyInvincible and not isInvincible:
                info = {"id" : playerID}
                self.queueMessage("player_vulnerable", info)
    
    ### SEND MESSAGES ###

    def sendUpdates(self) -> None: 
        for msg in self.updateQueue:
            self.port.send(msg)
        self.updateQueue = []

    def run(self) -> None:
        # while self.isRunning:
        outputLn("at top of running loop")
        # TODO:: Self.inbox is ending unexpectedly when sent message
        for msg in self.inbox:
            outputLn("in updateModel")
            self.updateModel(msg)
            self.runLogic()
            self.sendUpdates() 
            # if not self.isRunning:
            #     return
        outputLn("Finished Running")

    def queueMessage(self, command : str, info : dict):
        self.updateQueue.append((Atom(command), info))


GameLogic()