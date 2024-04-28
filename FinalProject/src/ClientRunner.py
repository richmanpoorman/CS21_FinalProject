
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as py
import numpy as np

py.init()

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





from TestTools import outputLn, outputInit

class ClientRunner:
    def __init__(self):
        '''
            Params  : (None)
            Purpose : Creates a client
        '''
        
        self.serverIdMap   = dict() 
        self.display       = Display() 
        self.inputListener = InputListener() 

        self.isRunning = True

        self.inbox, self.port = stdio_port_connection()

        
        self.initialize()
        self.run() 
        outputLn("Client Successfully quit")

    def initialize(self):
        '''
            Params  : (None)
            Purpose : Performs actions needed when the client is spawned
            Return  : (None)
        '''
        outputLn("Client Runninng")
        self.sendMessage("player_join", dict())

    def run(self):
        '''
            Params  : (None)
            Purpose : Runs the client loop to receive and send messages
            Return  : (None)
        '''

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
        '''
            Params  : (str)  command := The message type to send
                      (dict) info    := The information needed to execute the 
                                        message
            Purpose : Sends the message in the correct format across the erlang
                      channel to the server
            Return  : (None)
        '''

        outputLn("Client Message Send: " + command + " : " + str(info))
        match command:
            case "input":
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
        '''
            Params  : (str)  command := The message type received from the server
                      (dict) info    := The data needed to execute the command
            Purpose : Receives messages from the erlang channel, and performs 
                      the correct action in response to the message
            Return  : (None)
        '''
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
        '''
            Params  : (None)
            Purpose : Gets the inputs from the user and sends the message 
                      across the channel
            Return  : (None)
        '''
        input, data = self.inputListener.checkAndSendInput()
        if input:
            self.sendMessage(input, data)


def unpack(data) -> GameObject | None:
    '''
        Params  : (Any) data := The packed information of each cell
        Purpose : Unpacks the erlang message into a new instance of the 
                  correct object
        Return  : (GameObject) The game object with the correct information,
                               or None if not given anything that matches
                               the possible objects
    '''
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



ClientRunner()
py.quit()