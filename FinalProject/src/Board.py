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

    def addPlayer(player : Player) -> int: 
        pass 

    def removePlayer(playerID : int) -> Player:
        pass 

    def addInteractable(interactable : Interactable) -> int:
        pass 

    def removeInteractable(interactableID : int) -> Interactable:
        pass 

    def addGhost(ghost : Ghost) -> int: 
        pass 
    
    def removeGhost(ghostID : int) -> Ghost:
        pass 