from Board import Board

from Wall import Wall 
from Player import Player 
from Ghost import Ghost 
from Pellet import Pellet 
from PowerPellet import PowerPellet 

class BoardBuilder:
    def __init__(self, size : tuple = (10, 11)):
        '''
            Params  : None
            Purpose : Creates the board factory
            Return  : (BoardBuilder) An empty board builder
        '''
        self.board = Board(size) 
        self.idMap = {
            "wall"         : [], 
            "player"       : [],
            "ghost"        : [],
            "pellet"       : [],
            "power pellet" : []
        }

    def addWall(self, position : tuple):
        '''
            Params : ((int, int)) position := Position of the wall to add
            Purpose: Adds a wall at the given location of the board
            Return : (BoardBuilder) A board builder with the wall
        '''
        id = self.board.addObject(Wall(), position)
        self.idMap["wall"].append(id)
        return self
    
    def addPlayer(self, position : tuple): 
        '''
            Params : ((int, int)) position := Position of the player to add
            Purpose: Adds a player at the given location of the board
            Return : (BoardBuilder) A board builder with the player
        '''
        id = self.board.addObject(Player(), position)
        self.idMap["player"].append(id)
        return self 
    
    def addGhost(self, position : tuple): 
        '''
            Params : ((int, int)) position := Position of the ghost to add
            Purpose: Adds a ghost at the given location of the board
            Return : (BoardBuilder) A board builder with the ghost
        '''
        id = self.board.addObject(Ghost(), position) 
        self.idMap["ghost"].append(id)
        return self 
    
    def addPellet(self, position : tuple): 
        '''
            Params : ((int, int)) position := Position of the pellet to add
            Purpose: Adds a pellet at the given location of the board
            Return : (BoardBuilder) A board builder with the pellet
        '''
        id = self.board.addObject(Pellet(), position) 
        self.idMap["pellet"].append(id)
        return self 
    
    def addPowerPellet(self, position : tuple):
        '''
            Params : ((int, int)) position := Position of the power pellet to add
            Purpose: Adds a power pellet at the given location of the board
            Return : (BoardBuilder) A board builder with the power pellet
        '''
        id = self.board.addObject(PowerPellet(), position) 
        self.idMap["power pellet"].append(id)
        return self 
    
    def getBoard(self):
        '''
            Params : (None)
            Purpose: Returns the completed board
            Return : (Board) The board with all of the objects
                     (dict)  The ids of all of the objects
        '''
        return self.board, self.idMap
    
from os import environ
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as py

from TestTools import outputLn

def makeBoardFromImage(imagePath : str):
   
    image = py.image.load(imagePath)
    w, h = image.get_width(), image.get_height()
    boardBuilder = BoardBuilder((h, w)) 
    for r in range(h):
        for c in range(w):
            match tuple(image.get_at((c, r))):
                case (0, 0, 0, 255):
                    boardBuilder.addWall((r, c))
                case color:
                    continue
    
    return boardBuilder.getBoard()