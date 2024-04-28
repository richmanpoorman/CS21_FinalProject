from Movable import Movable

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface
import pygame as py

from pygame.transform import rotate

from typing import Any

from TestTools import outputLn

class Player(Movable):
    
    INVINCIBLE_DURATION   = 20
    path = "./images/pac_man_frame2.png"
    invinciblePath = "./images/halo.png"
    playerImage = py.image.load(path)
    invincibleEffect = py.image.load(invinciblePath)
    def __init__(self):
        '''
            Params  : (None)
            Purpose : Creates a new player
        ''' 
        super().__init__()
        self.invincibleTimer = 0

    
    def isInvincible(self) -> bool:
        '''
            Params  : (None)
            Purpose : Checks if the player is invincible
            Return  : (bool) Whether or not the player is invincible
        '''
        return self.invincibleTimer > 0

    def setInvincible(self) -> None:
        '''
            Params  : (None)
            Purpose : Makes the player invincible
            Return  : (None)
        '''
        self.invincibleTimer = Player.INVINCIBLE_DURATION

    def removeInvincible(self) -> None:
        '''
            Params  : (None)
            Purpose : Removes invincibility from the player
            Return  : (None)
            Note    : DEPRECIATED
        '''
        self.invincibleTimer = 0

    def decrementInvincibleTimer(self) -> bool:
        '''
            Params  : (None)
            Purpose : Decrements the invincibility timer
            Return  : (bool) Whether or not the player is still invincible
        '''
        self.invincibleTimer -= 1
        return self.isInvincible()
    
    @staticmethod 
    def convertImage():
        '''
            Params  : (None)
            Purpose : Converts the surface into an image which is easier to render
            Return  : (None)
        '''
        Player.invincibleEffect = Player.invincibleEffect.convert_alpha() 
        Player.playerImage      = Player.playerImage.convert()


    def getSurface(self) -> Surface:
        '''
            Params  : (None)
            Purpose : Gets the image for the object to render
            Return  : (Surface) The display of the object
        '''
        surface = self.playerImage.copy() 
        
        if self.isInvincible():
            # surface.blit(self.invincibleEffect, (0, 0))
            w, h = surface.get_width(), surface.get_height()
            color = (0, 195, 255, 255) if self.invincibleTimer > Player.INVINCIBLE_DURATION / 2 else \
                    (199, 152, 0, 255) if self.invincibleTimer > Player.INVINCIBLE_DURATION / 4 else \
                    (199, 0, 0, 255)
            py.draw.circle(surface, 
                           color, 
                           (w // 2, h // 2), 
                           (w + h) / 4 , 
                           width = 10)

        match self.getFacing():
            case Player.UP:
                surface = rotate(surface, 90)
            case Player.DOWN:
                surface = rotate(surface, -90)
            case Player.LEFT:
                surface = rotate(surface, 180)
            case Player.RIGHT:
                pass
            case _:
                raise RuntimeError("No direction found")
            
        

        return surface

    def pack(self) -> tuple[str, dict[str, Any]]: 
        '''
            Params  : (None)
            Purpose : Packs the object to cross the erlang channel
            Return  : (["player", Message]) The packed object
        '''
        _, movableInfo = super().pack()
        info = {
            "invincible" : self.invincibleTimer,
            "movable"    : movableInfo
        }
        return ("player", info)
    
    def unpack(self, info):
        '''
            Params  : (dict) info := The data from the object
            Purpose : Unpacks the object from the erlang channel
            Return  : (self) The object with all the information
        '''
        self.invincibleTimer = info["invincible"]

        super().unpack(info["movable"])
        
        return self