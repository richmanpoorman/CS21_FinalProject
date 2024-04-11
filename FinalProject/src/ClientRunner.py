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
from Term import Atom

class ClientRunner:
    def __init__(self):
        self.display       = Display() 
        self.inputListener = InputListener() 
        self.board         = Board()

        self.serverIdMap   = dict() 
        self.inbox, self.port = stdio_port_connection()
        self.initialize()
        self.run() 

    def initialize(self):
        pass 

    def sendInputs(self):
        input, data = self.inputListener.checkAndSendInput()
        if input:
            self.sendMessage(input, data)

    def sendMessage(self, command, info):
        match command:
            case "input":
                self.port.send((Atom("input"), info))
            case "player_join":
                self.port.send((Atom("player_join", info)))
            case "quit":
                self.port.send((Atom("quit"), info))
            
        self.port.send(command, info)

    def receiveUpdates(self):
        for _, command, data in self.inbox():
            self.receiveMessage(command, data)

    def receiveMessage(self, command : str, data : dict):
        match command:
            case "add_wall":
                wall = Wall() 
                clientId = self.__clientID(data["id"])
                self.board.addObject()
            case "add_player":
                pass 
            case "add_ghost":
                pass 
            case "add_pellet":
                pass 
            case "add_power_pellet":
                pass 
            case "move_object":
                pass 
            case "remove_object":
                pass 
            case "on_pick_up":
                pass 
            case "done":
                pass 

    def __addObject(self, gameObject : GameObject, serverId : int, position : tuple) -> None:
        clientID = self.board.addObject(gameObject, position)
        self.serverIdMap[serverId] = clientID

    def __clientID(self, serverId : int):
        return self.serverIdMap[serverId]

    def run(self):
        self.receiveUpdates() 
        self.sendInputs()


ClientRunner()