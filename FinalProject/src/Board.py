import numpy as np

from GameObject import GameObject
from Player import Player 
from Interactable import Interactable
from Ghost import Ghost
from Wall import Wall 

class Board:
    def __init__(self):
        pass 

    def getBoard(self) -> np.ndarray:
        pass 

    def getPlayers(self) -> map:
        pass 

    def getWalls(self) -> list:
        pass 

    def getInteractable(self) -> map: 
        pass 

    def getGhosts(self) -> map:
        pass 

    def getAt(self, position : tuple) -> GameObject:
        pass

    def addPlayer(self, player : Player) -> int: 
        pass 

    def removePlayer(self, playerID : int) -> Player:
        pass 

    def addInteractable(self, interactable : Interactable) -> int:
        pass 

    def removeInteractable(self, interactableID : int) -> Interactable:
        pass 

    def addGhost(self, ghost : Ghost) -> int: 
        pass 
    
    def removeGhost(self, ghostID : int) -> Ghost:
        pass 

    def canMoveTo(self, position : tuple) -> bool: 
        pass

    def getSize(self) -> tuple:
        pass 