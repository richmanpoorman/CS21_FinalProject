import pygame as py
# import os
# from erpy import stdio_port_connection # TODO: pip install erpy currently 
#                                        # doesn't work

class InputListener:
    def __init__(self):
        pass 


    def checkAndSendInput(self): # TODO: py.get()? or py.event.get()
        command = ""
        info = dict()
        for event in py.get():
            info = dict() 
            match event:
                case py.QUIT:
                    command = "quit"
                case py.KEYDOWN:
                    command = "input"
                    info["direction"] = self.__map_key_to_direction(event.key)
        return command, info

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
