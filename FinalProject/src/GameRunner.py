from GameProcess import GameProcess
from Erpy import stdio_port_connection
from term import Atom, Pid
from GameObject import GameObject

from TestTools import outputLn, outputInit

class GameRunner: 

    POSITION = {
        "up"    : ( 0,  1), 
        "down"  : ( 0, -1),
        "left"  : (-1,  0),
        "right" : ( 1,  0)
    }

    def __init__(self):
        self.logic = GameProcess()
        self.inbox, self.port = stdio_port_connection()
        self.playerIDs = dict()
        self.isRunning = True


        self.__run()


    def __run(self):
        outputLn("at top of running loop")
        for msg in self.inbox:
            self.__receiveMessage(msg)
            self.logic.updateBoard()
            self.__sendBoard()
            if not self.isRunning:
                return 
        outputLn("Finished Running")

    def __receiveMessage(self, msg):
        match msg:
            case (pid, command, info):
                self.__parseMessage(pid, command, info)
            case _:
                outputLn("Bad Message Received")

    def __parseMessage(self, pid, command, info):
        match command:
            case "quit":
                playerID = self.playerIDs[pid]
                self.logic.playerDie(playerID)
                outputLn("Player quit")
            case "input":
                playerID = self.playerIDs[pid]
                directionName = info["direction"]
                direction = GameRunner.POSITION[directionName]
                self.logic.playerMove(playerID, direction)
                # self.__onPlayerMove(pid, GameLogic.POSITION_DICT[info["direction"]]) # need testing
                outputLn("input of: " + str(info))
            case "player_join":
                playerID = self.logic.addPlayer()
                self.playerIDs[pid] = playerID
                outputLn("player join of: " + str(info))
                outputLn(f"{self.logic.getBoard()}")
            case "done":
                self.__endServer()
                outputLn("Server Done")
            case "py_port":
                outputLn(command + " " + info)
            case _: 
                outputLn("No match was found for " + str(command))

    def __endServer(self):
        self.port.send(Atom("done"))

    def __sendBoard(self):
        board : list[list[GameObject | None]] = self.logic.getBoard().tolist()
        nonePack : tuple[str, dict[str, str]] = GameObject.defaultPack()
        packedBoard = [[item.pack() if item else nonePack for item in row] for row in board]
        self.port.send((Atom("display"), {"data" : packedBoard}))


outputInit()
GameRunner() 