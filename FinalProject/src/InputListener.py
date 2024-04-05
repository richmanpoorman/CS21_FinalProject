import pygame as py
import os
from erpy import stdio_port_connection # TODO: pip install erpy currently 
                                       # doesn't work

class InputListener:
    def __init__(self):
        pass 


    def checkAndSendInput(self): # TODO: py.get()? or py.event.get()
        for event in py.get():
            inputValue = map()
            if event == py.QUIT:
                inputValue["QUIT"] = "QUIT" 
            elif event == py.KEYDOWN:
                inputValue["KEY"] = event.key
            
            self.sendInput(inputValue)

    
    def sendInput(self, inputValue : map):
        """Message format: {PID, command}"""
        # TODO: Use the erlang channel to send the (string, value) map over
        # TODO: Need testing if anyone is able to install erpy
        _, port = stdio_port_connection()
        port.send(self.__format_message(inputValue))
        
    def __map_key_to_direction(self, key):
        """Map Pygame key events to direction strings."""
        match key:
            case py.K_UP:
                return 'up'
            case py.K_DOWN:
                return 'down'
            case py.K_LEFT:
                return 'left'
            case py.K_RIGHT:
                return 'right'
            case _:
                return None  # Default case if no direction is matched

    
    def __format_message(self, inputValue: map):
        """Format the movement message according to specified pattern."""
        if "QUIT" in inputValue:
            return "{" + os.getpid() + ", quit}"
        elif "KEY" in inputValue:
            return "{" + f"{os.getpid()}, {self.__map_key_to_direction(inputValue['KEY'])}" + "}"
        return None
        