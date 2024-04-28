from Movable import Movable
from Player import Player
import pygame as py
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
from random import randrange
from typing import Any
from TestTools import outputLn

class Ghost(Movable):
    

    pathUp    = "./images/ghost/ghostUp.png"
    pathDown  = "./images/ghost/ghostDown.png"
    pathLeft  = "./images/ghost/ghostLeft.png"
    pathRight = "./images/ghost/ghostRight.png"
    ghostUp    = py.image.load(pathUp)
    ghostDown  = py.image.load(pathDown)
    ghostLeft  = py.image.load(pathLeft)
    ghostRight = py.image.load(pathRight)
    def __init__(self):
        '''
            Params  : (None) 
            Purpose : Creates a new ghost
        '''
        super().__init__()
        self.memory = None

    @staticmethod 
    def convertImage():
        '''
            Params  : (None)
            Purpose : Converts the surfaces into an image which is 
                      easier to render
            Return  : (None)
        '''
        Ghost.ghostUp    = Ghost.ghostUp.convert_alpha()
        Ghost.ghostDown  = Ghost.ghostDown.convert_alpha()
        Ghost.ghostLeft  = Ghost.ghostLeft.convert_alpha()
        Ghost.ghostRight = Ghost.ghostRight.convert_alpha()


    def getSurface(self) -> Surface:
        '''
            Params  : (None)
            Purpose : Gets the image for the object to render
            Return  : (Surface) The display of the object
        '''
        match self.getFacing():
            case Ghost.UP:
                return self.ghostUp 
            case Ghost.DOWN:
                return self.ghostDown
            case Ghost.LEFT:
                return self.ghostLeft 
            case Ghost.RIGHT:
                return self.ghostRight
            case _:
                return self.ghostRight
    
    def pack(self) -> tuple[str, dict[str, Any]]:
        '''
            Params  : (None)
            Purpose : Packs the object to cross the erlang channel
            Return  : (["ghost", Message]) The packed object
        '''
        _, movableInfo = super().pack()
        info = {
            "movable" : movableInfo
        }
        return ("ghost", info)
    
    def unpack(self, info):
        '''
            Params  : (dict) info := The data from the object
            Purpose : Unpacks the object from the erlang channel
            Return  : (self) The object with all the information
        '''
        super().unpack(info["movable"])
        return self