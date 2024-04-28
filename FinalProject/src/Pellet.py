from Interactable import Interactable
from Player import Player 

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
import pygame as py

class Pellet(Interactable):
    path = "./images/pellet.png"
    pelletImage = py.image.load(path)
    def __init__(self):
        '''
            Params  : (None) 
            Purpose : Creates an pellet
        '''
        super().__init__()

    def onGet(self, player : Player) -> str:
        '''
            Params  : (Player) player := The player that picked up the object
            Purpose : Does something when picked up by a player
            Return  : The name of the interactable
        '''
        return "pellet_pickup"
    
    @staticmethod 
    def convertImage():
        '''
            Params  : (None)
            Purpose : Converts the surface into an image which is 
                      easier to render
            Return  : (None)
        '''
        Pellet.pelletImage = Pellet.pelletImage.convert()

    def getSurface(self) -> Surface | None:
        '''
            Params  : (None)
            Purpose : Gets the image for the object to render
            Return  : (Surface) The display of the object
        '''
        return self.pelletImage
    
    def pack(self) -> tuple[str, dict[str, str]]:
        '''
            Params  : (None)
            Purpose : Packs the object to cross the erlang channel
            Return  : (["pellet", Message]) The packed object
        '''
        return ("pellet", dict())
    
    def unpack(self, info):
        '''
            Params  : (dict) info := The data from the object
            Purpose : Unpacks the object from the erlang channel
            Return  : (self) The object with all the information
        '''
        return self