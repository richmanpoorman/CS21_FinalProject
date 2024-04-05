from erpy import stdio_port_connection
from term import Atom

from Board import Board
from Ghost import Ghost
from Player import Player
class GameLogic:
    def __init__(self):
        self.board = Board()
        self.isRunning = True
        self.inbox, self.port = stdio_port_connection() 
        self.run()
        
    ### RECEIEVE MESSAGES ###
    def updateModel(self) -> None:
        for msg in self.inbox:
            pid, command, data = msg 

            if command == Atom("close"):
                self.onClose()
            elif command == Atom("player_join"):
                self.onJoin(pid, data)

        
    def onClose(self) -> None:
        self.isRunning = False

    def onJoin(self, pid, playerID):
        pass 

    ### RUN GAME LOGIC ###

    def runLogic(self) -> None:
        pass 

    def moveGhosts(self) -> None:
        ghosts = self.board.getAllOfType(Ghost)
        for ghostID, _ in ghosts: 
            ghostPos = self.board.getPosition(ghostID)
            newPosition = Ghost.move(self.board, ghostPos)
            canMove, blocker = self.board.moveObject(ghostID, newPosition)

            if not canMove:
                if isinstance(blocker, Player):
                    

    
    ### SEND MESSAGES ###

    def sendUpdates(self) -> None: 
        pass 

    def run(self) -> None:
        while self.isRunning: 
            self.updateModel()
            self.runLogic()
            self.sendUpdates() 


GameLogic()