from Display import Display
from InputListener import InputListener
from Board import Board

from GameObject import GameObject
from Ghost import Ghost 
from InputListener import InputListener
from Pellet import Pellet
from PowerPellet import PowerPellet
from Player import Player
from Wall import Wall 

from erpy import stdio_port_connection
from term import Atom
import pygame as py

from threading import Lock, Thread

from TestTools import outputLn, outputInit

class ClientRunner:
    def __init__(self):

        ## TODO:: TESTING INITIALIZATION
        # outputInit()
        
        self.display       = Display() 
        self.inputListener = InputListener() 
        self.board         = Board()

        self.serverIdMap   = dict() 
        self.inbox, self.port = stdio_port_connection()
        
        self.messageLock = Lock() 
        self.messages = []

        self.isRunning = True
        self.initialize()
        self.run() 
        outputLn("Client Successfully quit")

    def initialize(self):
        outputLn("Client Runninng")
        self.inboxThread = Thread(target = self.messageListener)
        self.inboxThread.start()
        self.sendMessage("player_join", dict())

    def sendInputs(self):
        input, data = self.inputListener.checkAndSendInput()

        if input:
            self.sendMessage(input, data)

    def sendMessage(self, command : str, info : dict) -> None:
        match command:
            case "input":
                self.port.send((Atom("input"), info))
            case "player_join":
                self.port.send((Atom("player_join"), info))
            case "quit":
                outputLn("Client Quitting")
                self.port.send((Atom("quit"), info))
                self.isRunning = False
            case _:
                outputLn("Unknown Message Sent")

    def messageListener(self) -> None:
        for msg in self.inbox:
            _, command, data = msg
            with self.messageLock:
                outputLn(command)
                self.messages.append((command, data))
                if command == "quit":
                    return

    def receiveUpdates(self) -> None:
        with self.messageLock:
            for msg in self.messages:
                command, data = msg
                outputLn("CLIENT RECEIVES: " + command)
                self.receiveMessage(command, data)
            self.messages = []

    def receiveMessage(self, command : str, data : dict) -> None:
        match command:
            case "add_wall":
                wall = Wall() 
                serverId = data["id"]
                position = data["position"]
                self.__addObject(wall, serverId, position)
            case "add_player":
                player = Player() 
                serverId = data["id"]
                position = data["position"]
                self.__addObject(player, serverId, position)
            case "add_ghost":
                ghost = Ghost() 
                serverId = data["id"]
                position = data["position"]
                self.__addObject(ghost, serverId, position)
            case "add_pellet":
                pellet = Pellet() 
                serverId = data["id"]
                position = data["position"]
                self.__addObject(pellet, serverId, position)
            case "add_power_pellet":
                powerPellet = PowerPellet()
                serverId = data["id"]
                position = data["position"]
                self.__addObject(powerPellet, serverId, position)
            case "move_object":
                clientId = self.__clientID(data["id"])
                position = data["position"]
                self.board.moveObject(clientId, position)
            case "remove_object":
                clientId = self.__clientID(data["id"])
                self.board.removeObject(clientId)
            case "done":
                self.isRunning = False

    def __addObject(self, gameObject : GameObject, serverId : int, position : tuple) -> None:
        clientID = self.board.addObject(gameObject, position)
        self.serverIdMap[serverId] = clientID

    def __clientID(self, serverId : int) -> int:
        return self.serverIdMap[serverId]

    def __updateBoard(self):
        self.display.receiveUpdate(self.board.getBoard())

    def run(self):
        while self.isRunning:
            self.receiveUpdates() 
            self.__updateBoard()
            self.sendInputs()

            
py.init()
ClientRunner()
py.quit()