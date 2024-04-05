import numpy as np

from GameObject import GameObject
from Player import Player 
from Interactable import Interactable
from Ghost import Ghost
from Wall import Wall 

class Board:
    BOARD_SIZE = (10, 11)
    def __init__(self, boardSize : tuple = BOARD_SIZE):
        '''
            Name    : init
            Params  : (None)
            Purpose : Creates a new board to add things to 
        '''
        self.size = boardSize
        # Keeps track of the IDS of the objects
        self.idCount = 0 
        # Maps IDs -> GameObject
        self.gameObject = map() 
        # Maps position -> ID
        self.locations = map()
        # Maps ID -> position 
        self.positions = map() 

        # Checks what things are on top of another
            # Maps ID -> ID or ID -> None
        self.onTopOf = map() 

    def getBoard(self) -> np.ndarray:
        '''
            Name    : getBoard
            Params  : (None)
            Purpose : Gets the data of the board as a 2-d grid
            Return  : (np.ndarray) A ndarray with the game objects in 
                                   their respective locations
        '''
        board = np.empty(self.size, GameObject)
        for loc, gameObjectID in self.locations.items():
            board[loc] = self.gameObject[gameObjectID]

        return board 

    def getAt(self, position : tuple) -> GameObject:
        '''
            Name    : getAt
            Params  : ((int, int)) position := The position of the gameObject
            Purpose : Gets the top-most game object at the given position, 
                      or none if there is nothing there
            Return  : (GameObject) The object at that location, 
                                   or none if there is nothing there
        '''
        return None if position not in self.locations \
                    else self.gameObject[self.locations[position]]
    
    def getAtAll(self, position : tuple) -> GameObject:
        
        current = self.positions[position]
        onSquare = []
        while current: 
            onSquare.append(current)
            current = self.onTopOf[current]
            
        return onSquare



    def addObject(self, gameObject : GameObject, position : tuple) -> int:
        '''
            Name    : addObject
            Params  : (GameObject) gameObject := The object to add to the board 
                      ((int, int)) position   := The position to start at 
            Purpose : Adds the object to the board at the given locations
            Return  : (ID) The id used to reference the gameObject in the board
        '''
        objectID = self.idCount 
        self.idCount += 1
        self.gameObject[objectID] = gameObject 
        self.onTopOf[objectID] = self.positions[position] \
                                    if position in self.positions \
                                    else None
        self.locations[objectID] = position 
        self.positions[position] = objectID
        return objectID

    def moveObject(self, objectID : int, position : tuple) -> GameObject:
        '''
            Name    : moveObject
            Params  : (ID)         objectID := The ID of the object to move
                      ((int, int)) position := The new position of the object
            Purpose : Moves the object to the new position
            Return  : The GameObject at the new location, or none if it was 
                      an empty spot
        '''
        if position == self.locations[objectID]:
            return self.gameObject[objectID]
        
        atPosition = self.gameObject[self.positions[position]] \
                        if position in self.positions \
                        else None

        # Replace the object with what it is on top of
        if not self.onTopOf[objectID]:
            del self.positions[self.locations[objectID]]
        else: 
            self.positions[self.locations[objectID]] = self.onTopOf[objectID]
        
        # Put the object on top of whatever is there
        if not atPosition:
            self.onTopOf[objectID] = None 
        else:
            self.onTopOf[objectID] = self.positions[position]
        
        # Move the object to the location
        self.locations[objectID] = position 
        self.positions[position] = objectID 

        return atPosition 

    def removeObject(self, objectID : int) -> GameObject:
        '''
            Name    : removeObject
            Params  : (ID) objectID := The ID of the object to remove
            Purpose : Removes the object from the board
            Return  : (GameObject) The GameObject removed from the board
        '''
        if not self.onTopOf[objectID]:
            del self.positions[self.locations[objectID]]
        else: 
            self.positions[self.locations[objectID]] = self.onTopOf[objectID]
        
        del self.locations[objectID]
        gameObject = self.getObject(objectID)
        del self.gameObject[objectID]
        del self.onTopOf[objectID]

        return gameObject
    
    def getObject(self, objectID : int) -> GameObject:
        '''
            Name    : getObject
            Params  : (ID) objectID := The ID of the object to get
            Purpose : Gets the game object associated with the ID 
            Return  : (GameObject) The game object associated, or None if none
        '''
        return self.gameObject[objectID] if objectID in self.gameObject \
                                         else None

    def canMoveTo(self, position : tuple) -> tuple: 
        '''
            Name    : canMoveTo
            Params  : ((int, int)) position := The position to check
            Purpose : Checks if a game object to go to the given position
            Return  : ((bool, GameObject)) Whether or not the object can move 
                                           there, and the object stopping it
        '''
        if position not in self.positions or not self.positions[position]:
            return (True, None) 
        gameObject = self.gameObject[self.positions[position]]
        if isinstance(gameObject, Interactable):
            return (True, gameObject) 
        
        return (False, gameObject)

    def getSize(self) -> tuple:
        '''
            Name    : getSize
            Params  : (None)
            Purpose : Returns the size of the board
            Return  : ((int, int)) The size of the board
        '''
        return self.size

    def getAllOfType(self, objectType) -> map:
        '''
            Name    : getAllOfType
            Params  : (Class) The class to get the types of 
            Purpose : Gets all of the game objects with the types
            Return  : ((ID, GameObject)...) The list of the ids and game objects
        '''
        return [(id, gameObject) for (id, gameObject) in self.gameObject 
                                 if isinstance(gameObject, objectType)]
