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
    UPDATE_TIME = 0.1
    POSITION = {
        "up"    : (-1,  0), 
        "down"  : ( 1,  0),
        "left"  : ( 0, -1),
        "right" : ( 0,  1)
    }

    def __init__(self):
        '''
            Params  : (None)
            Purpose : Creates the python side of a server
        '''
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
        '''
            Params  : (None)
            Purpose : Sets up the server logic
            Return  : The logic module that was set up
        '''
        return GameProcess()


    def updateCycle(self):
        '''
            Params  : (None)
            Purpose : A thread which updates the board at given intervals
            Return  : (None)
        '''
        while self.isRunning:
            with self.updateLock:
                self.logic.updateBoard()
            sleep(GameRunner.UPDATE_TIME)

    def __run(self):
        '''
            Params  : (None)
            Purpose : Receives messages and responds to incoming messages 
                      while running
            Return  : (None)
        '''
        for msg in self.inbox:
            with self.updateLock:
                self.__receiveMessage(msg)
            if not self.isRunning:
                break
        self.isRunning = False
        outputLn("Finished Running")

    def __receiveMessage(self, msg):
        '''
            Params  : (Message) msg := Message received
            Purpose : Receives the messages and runs the correct response
            Return  : (None) 
        '''
        match msg:
            case (pid, command, info):
                self.__parseMessage(pid, command, info)
            case _:
                outputLn("Bad Message Received")

    def __parseMessage(self, pid, command, info):
        '''
            Params  : (Pid)  pid     := The PID the message came from
                      (str)  command := The type of message 
                      (dict) info    := The information to run the message
            Purpose : Runs the appropriate message given the 
                      pieces of the message
            Return  : (None)
        '''
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
                outputLn("Server Recieved input of: " + str(info))
            case "player_join":
                playerID = self.logic.addPlayer()
                self.playerIDs[pid] = playerID
                outputLn("player join of: " + str(info))
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
        '''
            Params  : (None)
            Purpose : Sets the server to not running
            Return  : (None)
        '''
        self.isRunning = False
        # self.port.send(Atom("done"))

    def __sendBoard(self):
        '''
            Params  : (None)
            Purpose : Packs and sends the board across the erlang channel
            Return  : (None)
        '''
        board : list[list[GameObject | None]] = self.logic.getBoard().tolist()
        nonePack : tuple[str, dict[str, str]] = GameObject.defaultPack()
        packedBoard = [[item.pack() if item else nonePack for item in row] 
                                                          for row in board]
        self.port.send((Atom("display"), {"data" : packedBoard}))


stdout.flush()
outputInit()
outputInit()
GameRunner() 