from erpy import stdio_port_connection
from term import Atom, Pid
from random import randrange

from Board import Board
from Ghost import Ghost
from Player import Player
from Interactable import Interactable
from Wall import Wall 
from Pellet import Pellet 
from PowerPellet import PowerPellet

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
        

        self.__setUpBoard()
        self.__run()

    ### SEND BOARD INFORMATION TO ALL USERS ### 
    def __setUpBoard(self):

        self.__sendBoardInfo()
        pass
    
    def __sendBoardInfo(self):
        playersOnBoard      = [(id, self.board.getPosition(id)) for id, _ in self.board.getAllOfType(Player)     ]
        ghostsOnBoard       = [(id, self.board.getPosition(id)) for id, _ in self.board.getAllOfType(Ghost)      ]
        wallsOnBoard        = [(id, self.board.getPosition(id)) for id, _ in self.board.getAllOfType(Wall)       ]
        pelletsOnBoard      = [(id, self.board.getPosition(id)) for id, _ in self.board.getAllOfType(Pellet)     ] 
        powerPelletsOnBoard = [(id, self.board.getPosition(id)) for id, _ in self.board.getAllOfType(PowerPellet)]

        self.__sendInitialObjects("add_player", playersOnBoard)
        self.__sendInitialObjects("add_ghost", ghostsOnBoard)
        self.__sendInitialObjects("add_wall", wallsOnBoard)
        self.__sendInitialObjects("add_pellet", pelletsOnBoard)
        self.__sendInitialObjects("add_power_pellet", powerPelletsOnBoard)
    
    def __sendInitialObjects(self, command : str, idPosPairs : list):
        for id, pos in idPosPairs:
            info = {"id" : id, "position" : pos}
            self.__queueMessage(command, info)

    def __updateModel(self, msg) -> None:  
        outputLn("SERVER RECEIEVED SOME MESSAGE")
        match msg:
            case (pid, command, info):
                self.__parseMessage(pid, command, info)
            case _:
                outputLn("Unknown message received")
    
    def __parseMessage(self, pid, command, info):
        outputLn("SERVER RECEIVES: " + str(command) + str(info))
        match command:
            case "quit":
                self.__playerDie(pid) # need testing
                outputLn("Closing")
            case "input":
                self.__onPlayerMove(pid, GameLogic.POSITION_DICT[info["direction"]]) # need testing
                outputLn("input of: " + str(info))
            case "player_join":
                self.__onJoin(pid) # need testing
                outputLn("player join of: " + str(info))
            case "done":
                self.__onClose() # need testing
                outputLn("Server Done")
                self.isRunning = False
            case "py_port":
                outputLn(command + " " + info)
            case _: 
                outputLn("No match was found for " + str(command))
            
    def __onPlayerMove(self, pid : Pid, direction : tuple) -> None:
        player = self.playerIDs[pid]
        newPosition = \
            self.__movePlayer(direction, 
                              self.board.getPosition(self.playerIDs[pid]))
        
        canMove, blocker = self.board.canMoveTo(newPosition)

        if canMove: 
            self.board.moveObject(player, newPosition)
            self.__tryToPickUp(blocker, player)
        else: 
            if not blocker:
                return

            playerObject : Player = self.board.getObject(player)
            isInvincible = playerObject.isInvincible()
            
            if self.board.isObjectOfType(blocker, Ghost):
                if isInvincible:
                    self.__ghostDie(blocker)
                else:
                    self.__playerDie(player)
            elif self.board.isObjectOfType(blocker, Player):
                blockedBy : Player = self.board.getObject(blocker)
                if isInvincible and not blockedBy.isInvincible():
                    self.__playerDie(blocker)
    
    def __movePlayer(self, dir : tuple, position : tuple) -> tuple:
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
        self.__moveAllGhosts()
        self.__decrementPlayerTimers()

    def __moveAllGhosts(self) -> None:
        ghosts = self.board.getAllOfType(Ghost)
        for ghostID, _ in ghosts: 
            self.__moveGhost(ghostID)
    
    def __moveGhost(self, ghostID : int) -> None:
        attemptCounter = 0
        while attemptCounter < 1000:
            newPosition = self.__moveGhostAttempt(ghostID)
            canMove, blocker = self.board.canMoveTo(newPosition)
            if canMove:
                self.board.moveObject(ghostID, newPosition)
                return 
            
            blockedBy = self.board.getObject(blocker) 

            if self.board.isObjectOfType(blocker, Player):
                player : Player = blockedBy
                if player.isInvincible():
                    self.__ghostDie(ghostID)
                else:
                    self.__playerDie(blocker)
                    self.board.moveObject(ghostID, newPosition)
                return
            
            attemptCounter += 1

    
    def __moveGhostAttempt(self, ghostID : int) -> tuple:
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

    def __playerDie(self, playerID : int) -> None:
        info = {"id" : playerID}
        self.__queueMessage("player_die", info)
    
    def __ghostDie(self, ghostID : int) -> None: 
        info = {"id" : ghostID}
        self.__queueMessage("ghost_die", info)
    
    def __onClose(self) -> None:
        self.isRunning = False
        self.__queueMessage("done", dict())

    def __onJoin(self, pid : Pid) -> None:
        self.playerIDs[pid] = self.board.addObject(Player(), (0, 0))
        info = {"id" : self.playerIDs[pid]}
        self.__queueMessage("player_join", info)

    def __tryToPickUp(self, interactable : int, player : int) -> None:
        if not interactable:
            return 
        if self.board.isObjectOfType(interactable, Interactable):
            blockerObject = self.board.getObject(interactable)
            blockerObject.onGet(self.board.getObject(player))
            info = {"id" : interactable, "playerID" : player}
            self.__queueMessage("remove_object", info)

    def __decrementPlayerTimers(self) -> None:
        players : list = self.board.getAllOfType(Player)
        for playerID, player in players:
            isPreviouslyInvincible = player.isInvincible()
            isInvincible = player.decrementInvincibleTimer()
            
            if isPreviouslyInvincible and not isInvincible:
                info = {"id" : playerID}
                self.__queueMessage("player_vulnerable", info)
    
    ### SEND MESSAGES ###

    def __sendUpdates(self) -> None: 
        for msg in self.updateQueue:
            self.port.send(msg)
        self.updateQueue = []

    def __run(self) -> None:
        # while self.isRunning:
        outputLn("at top of running loop")
        # TODO:: Self.inbox is ending unexpectedly when sent message
        for msg in self.inbox:
            outputLn("in __updateModel")
            self.__updateModel(msg)
            self.runLogic()
            self.__sendUpdates() 
            # if not self.isRunning:
            #     return
        outputLn("Finished Running")

    def __queueMessage(self, command : str, info : dict):
        self.updateQueue.append((Atom(command), info))


GameLogic()