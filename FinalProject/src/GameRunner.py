from GameProcess import GameProcess
from erpy import stdio_port_connection
from term import Atom, Pid
from GameObject import GameObject
from Board import Board 
from BoardBuilder import BoardBuilder

from threading import Thread, Lock
from time import sleep
from sys import stdout

from TestTools import outputLn, outputInit

class GameRunner: 
    UPDATE_TIME = 0.25
    POSITION = {
        "up"    : (-1,  0), 
        "down"  : ( 1,  0),
        "left"  : ( 0, -1),
        "right" : ( 0,  1)
    }

    def __init__(self):
        self.logic = self.__initializeLogic()
        self.inbox, self.port = stdio_port_connection()
        self.playerIDs = dict()
        self.isRunning = True
        
        self.updateLock   = Lock() 
        self.updateThread = Thread(target = self.updateCycle)
        self.updateThread.start()

        self.isRunning = True

        self.__run()


    def __initializeLogic(self) -> GameProcess:
        # wall_count = 20
        # boardBuild = BoardBuilder()
        # board, _ = BoardBuilder()\
        #             .addWall((0, 5))\
        #             .addWall((6, 0))\
        #             .addGhost((1, 1))\
        #             .getBoard()
        return GameProcess()


    def updateCycle(self):
        while self.isRunning:
            with self.updateLock:
                self.logic.updateBoard()
            sleep(GameRunner.UPDATE_TIME)

    def __run(self):
        outputLn("at top of running loop")
        for msg in self.inbox:
            with self.updateLock:
                self.__receiveMessage(msg)
            if not self.isRunning:
                break
        self.isRunning = False
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
            case "clock":
                self.__sendBoard()
            case _: 
                outputLn("No match was found for " + str(command))

    def __endServer(self):
        self.isRunning = False
        # self.port.send(Atom("done"))

    def __sendBoard(self):
        board : list[list[GameObject | None]] = self.logic.getBoard().tolist()
        nonePack : tuple[str, dict[str, str]] = GameObject.defaultPack()
        packedBoard = [[item.pack() if item else nonePack for item in row] for row in board]
        self.port.send((Atom("display"), {"data" : packedBoard}))


stdout.flush()
outputInit()
GameRunner() 