
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

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
import numpy as np


from TestTools import outputLn, outputInit

class ClientRunner:
    def __init__(self):

        ## TODO:: TESTING INITIALIZATION
        # outputInit()
        
        self.serverIdMap   = dict() 
        self.display       = Display() 
        self.inputListener = InputListener() 

        self.isRunning = True

        self.inbox, self.port = stdio_port_connection()

        
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
        match command:
            case "clock":
                self.sendInputs()
            case "display":
                extractedData = data["data"]
                arrData = [ [unpack(item) for item in row] 
                                          for row in extractedData ]
                self.display.receiveUpdate(np.array(arrData))
            case "done":
                self.isRunning = False

    def sendInputs(self):
        input, data = self.inputListener.checkAndSendInput()
        if input:
            self.sendMessage(input, data)


def unpack(data) -> GameObject | None:
    name, info = data 
    match name:
        case "wall": 
            return Wall().unpack(info)
        case "player":
            return Player().unpack(info)
        case "ghost":
            return Ghost().unpack(info)
        case "pellet":
            return Pellet().unpack(info)
        case "powerpellet":
            return PowerPellet().unpack(info)
        case _:
            return None


py.init()
ClientRunner()
py.quit()