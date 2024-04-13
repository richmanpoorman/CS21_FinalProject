import pygame as py
# import os
# from erpy import stdio_port_connection # TODO: pip install erpy currently 
#                                        # doesn't work

from TestTools import outputLn # TODO::TESTING FUNCTION

class InputListener:
    def __init__(self):
        pass 


    def checkAndSendInput(self): 
        command = ""
        info = dict()
        for event in py.event.get():
            match event.type:
                case py.QUIT:
                    info = dict() 
                    command = "quit"
                case py.KEYDOWN:
                    info = dict() 
                    command = "input"
                    info["direction"] = self.__map_key_to_direction(event.key)
                case _:
                    pass


            # TODO:: Check that the event is proper
            
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
            case py.K_w:
                return 'up'
            case py.K_s:
                return 'down'
            case py.K_a:
                return 'left'
            case py.K_d:
                return 'right'
            case _:
                return None  # Default case if no direction is matched
