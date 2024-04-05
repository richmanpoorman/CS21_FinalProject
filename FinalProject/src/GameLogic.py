from erpy import stdio_port_connection
from term import Atom, Pid

from Board import Board
from Ghost import Ghost
from Player import Player
class GameLogic:
    def __init__(self):
        self.board = Board()
        self.isRunning = True
        self.inbox, self.port = stdio_port_connection() 
        self.playerIDs = map()
        self.updateQueue = []
        self.run()
        
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
            


    def onPlayerMove(self, pid : Pid, direction : tuple):
        player = self.playerIDs[pid]
        newPosition = \
            Player.movePlayer(direction, 
                              self.board.getSize(), 
                              self.board.getPosition(self.playerIDs[pid]))
        canMove, blocker = self.board.canMoveTo(newPosition)
        if canMove: 
            self.board.moveObject(player, newPosition)
        


    def onClose(self) -> None:
        self.isRunning = False

    def onJoin(self, pid : Pid) -> None:
        self.playerIDs[pid] = self.board.addObject(Player(), (0, 0))

    def getPickUp(self, interactableID : int):


    ### RUN GAME LOGIC ###

    def runLogic(self) -> None:
        self.moveAllGhosts()
        pass 

    def moveAllGhosts(self) -> None:
        ghosts = self.board.getAllOfType(Ghost)
        for ghostID, _ in ghosts: 
            self.moveSingleGhost(ghostID)

    def moveSingleGhost(self, ghostID : int):
        ghostPos = self.board.getPosition(ghostID)
        newPosition = Ghost.move(self.board, ghostPos)
        goToID = self.board.moveObject(ghostID, newPosition) 
        if goToID:
            atPos = self.board.getObject(goToID)
            if isinstance(atPos, Player):
                if atPos.isInvincible():
                    self.ghostDie(ghostID) 
                else:
                    self.playerDie(goToID)


    def playerDie(self, playerID : int) -> None:
        pass 
    
    def ghostDie(self, ghostID : int) -> None: 
        pass 

    ### SEND MESSAGES ###

    def sendUpdates(self) -> None: 
        pass 

    def run(self) -> None:
        while self.isRunning: 
            self.updateModel()
            self.runLogic()
            self.sendUpdates() 


GameLogic()