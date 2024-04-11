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
                self.port.send((Atom("player_join", info)))
            case "quit":
                self.port.send((Atom("quit"), info))

    def receiveUpdates(self) -> None:
        for _, command, data in self.inbox():
            self.receiveMessage(command, data)

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
                pass 

    def __addObject(self, gameObject : GameObject, serverId : int, position : tuple) -> None:
        clientID = self.board.addObject(gameObject, position)
        self.serverIdMap[serverId] = clientID

    def __clientID(self, serverId : int) -> int:
        return self.serverIdMap[serverId]

    def __updateBoard(self):
        self.display.update(self.board.getBoard())

    def run(self):
        self.receiveUpdates() 
        self.display.updateDisplay()
        self.sendInputs()


ClientRunner()