import pygame as py
# import os
# from erpy import stdio_port_connection # TODO: pip install erpy currently 
#                                        # doesn't work

from TestTools import outputLn # TODO::TESTING FUNCTION

class InputListener:
    def __init__(self):
        pass 

    def checkAndSendInput(self): 
        '''
            Params  : (None)
            Purpose : Gets the input from the player
            Return  : ([InputType, dict]) The most recent input gotten
        '''
        command = None
        info = dict()
        for event in py.event.get():
            match event.type:
                case py.QUIT:
                    info = dict() 
                    command = "quit"
                case py.KEYDOWN:
                    info = dict() 
                    command = "input"
                    direction = self.__map_key_to_direction(event.key)
                    if direction:
                        info["direction"] = direction
                    else:
                        command = None
                case _:
                    continue
        if command:
            return command, info
        return None, None

    def __map_key_to_direction(self, key):
        '''
            Params  : (Key) key := The pygame key input
            Purpose : Map Pygame key events to direction strings
            Return  : (str) The string mapping to the direction of the input
        '''
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
