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

from TestTools import outputLn, outputInit

class ClientRunner:
    def __init__(self):

        ## TODO:: TESTING INITIALIZATION
        # outputInit()
        
        self.serverIdMap   = dict() 
        self.display       = Display() 
        self.inputListener = InputListener() 
        self.board         = Board()

        self.isRunning = True

        self.inbox, self.port = stdio_port_connection()

        self.port.send(Atom("test_message"))
        
        self.initialize()
        self.run() 
        outputLn("Client Successfully quit")

    def initialize(self):
        outputLn("Client Runninng")
        self.sendMessage("player_join", dict())

    def run(self):
        while True:
            # PREAMBLE TO TRICK PYGAME
            for event in py.event.get():
                if event.type == py.QUIT:
                    return
            
            for msg in self.inbox:
                match msg:
                    case (_, command, info):
                        self.receiveMessage(command, info) 
                    case badmessage:
                        outputLn(badmessage)
                if not self.isRunning:
                    return
        
    def sendMessage(self, command : str, info : dict) -> None:
        outputLn("Client Message Send: " + command + " : " + str(info))
        match command:
            case "input":
                outputLn("Client sending input")
                message = (Atom("input"), info)
                self.port.send(message)
            case "player_join":
                message = (Atom("player_join"), info)
                self.port.send(message)
            case "quit":
                outputLn("Client Quitting")
                self.isRunning = False
                message = (Atom("quit"), info)
                self.port.send(message)
            case _:
                outputLn("Unknown Message Sent")
                message = Atom("client_badmessage")
                self.port.send(message)

    def receiveMessage(self, command : str, data : dict) -> None:
        outputLn("Received command: " + command)
        match command:
            case "clock":
                outputLn("client clock signal received")
                self.sendInputs()
                self.__updateBoard()
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

    def sendInputs(self):
        input, data = self.inputListener.checkAndSendInput()
        if input:
            self.sendMessage(input, data)

    def __addObject(self, gameObject : GameObject, serverId : int, position : tuple) -> None:
        clientID = self.board.addObject(gameObject, position)
        self.serverIdMap[serverId] = clientID

    def __clientID(self, serverId : int) -> int:
        return self.serverIdMap[serverId]

    def __updateBoard(self):
        self.display.receiveUpdate(self.board.getBoard())

py.init()
ClientRunner()
py.quit()