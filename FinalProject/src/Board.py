import numpy as np

from GameObject import GameObject
from Player import Player 
from Interactable import Interactable
from Ghost import Ghost
from Wall import Wall 

from TestTools import outputLn

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
        self.idCount = 1
        # dicts IDs -> GameObject
        self.gameObject = dict()
        # dicts ID -> position
        self.locations = dict()
        # dicts position -> ID 
        self.positions = dict() 

        # Checks what things are on top of another
            # dicts ID -> ID or ID -> None
        self.onTopOf = dict() 

    def getBoard(self) -> np.ndarray:
        '''
            Name    : getBoard
            Params  : (None)
            Purpose : Gets the data of the board as a 2-d grid
            Return  : (np.ndarray) A ndarray with the game objects in 
                                   their respective locations
        '''
        board = np.empty(self.size, GameObject)
        for loc, gameObjectID in self.positions.items():
            board[loc] = self.gameObject[gameObjectID]

        return board 

    def getAt(self, position : tuple) -> GameObject | None:
        '''
            Name    : getAt
            Params  : ((int, int)) position := The position of the gameObject
            Purpose : Gets the top-most game object at the given position, 
                      or none if there is nothing there
            Return  : (GameObject) The object at that location, 
                                   or none if there is nothing there
        '''
        return None if position not in self.positions \
                    else self.gameObject[self.positions[position]]
    
    def isIn(self, objectID : int) -> bool:
        '''
            Name    : isIn
            Params  : (ID) objectID := The id to check is in
            Purpose : Checks if the object is in the board properly
            Return  : (bool) Whether it is in the board or not
        '''
        return objectID in self.locations and \
               self.locations[objectID] in self.positions

    def getAtAll(self, position : tuple) -> list:
        
        current = self.__getAtID(position)
        onSquare = []
        while current: 
            onSquare.append(self.getObject(current))
            current = self.__getIDUnder(current)
            
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
        self.__setOnTopOf(objectID, position)

        return objectID

    def moveObject(self, objectID : int, position : tuple) -> GameObject | None:
        '''
            Name    : moveObject
            Params  : (ID)         objectID := The ID of the object to move
                      ((int, int)) position := The new position of the object
            Purpose : Moves the object to the new position
            Return  : The ID of the object at the new location, or none if it 
                      was an empty spot
        '''

        originalPosition = self.__getIDPosition(objectID)
        if not originalPosition:
            raise Exception("Move object that doesn't exist")

        if position == originalPosition:
            atSquare = self.getObject(objectID)
            if not atSquare:
                raise Exception("Moving nothing")
            return atSquare
        
        if self.__getAtID(originalPosition) != objectID:
            raise Exception("Moving with something on top")
        
        atPosition = self.getAt(position)

        # Replace the object with what it is on top of
        self.__takeOffTop(objectID, originalPosition)
        
        # Put the object on top of whatever is there
        self.__setOnTopOf(objectID, position)

        return atPosition 

    def removeObject(self, objectID : int) -> GameObject:
        '''
            Name    : removeObject
            Params  : (ID) objectID := The ID of the object to remove
            Purpose : Removes the object from the board
            Return  : (GameObject) The GameObject removed from the board
        '''
        originalPosition = self.__getIDPosition(objectID)
        if not originalPosition:
            raise Exception("Removing something that doesn't exist")

        if self.__getAtID(originalPosition) != objectID:
            raise Exception("Removing with something on top")
        
        self.__takeOffTop(objectID, originalPosition)
        
        del self.locations[objectID]
        gameObject = self.getObject(objectID)
        del self.gameObject[objectID]
        if not gameObject:
            raise Exception("No object found to remove")
        return gameObject
    
    def getObject(self, objectID : int) -> GameObject | None:
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
        gameObject = self.__getAtID(position)
        if not gameObject:
            return (True, None) 
        
        if isinstance(gameObject, Interactable):
            return (True, gameObject) 
        
        
        outputLn("--Game Object: " + str(gameObject))

        return (False, gameObject)

    def getSize(self) -> tuple:
        '''
            Name    : getSize
            Params  : (None)
            Purpose : Returns the size of the board
            Return  : ((int, int)) The size of the board
        '''
        return self.size

    def getAllOfType(self, objectType) -> list:
        '''
            Name    : getAllOfType
            Params  : (Class) The class to get the types of 
            Purpose : Gets all of the game objects with the types
            Return  : ((ID, GameObject)...) The list of the ids and game objects
        '''
        return [(id, gameObject) for id, gameObject in self.gameObject.items()
                                 if isinstance(gameObject, objectType)]

    def getPosition(self, objectID : int) -> tuple:
        '''
            Name    : getPosition
            Params  : (ID) objectID := The ID of the object
            Purpose : Gets the position of the object
            Return  : ((int, int)) The position of the object
        '''
        if objectID not in self.locations:
            raise Exception("Try to get position of object that doesn't exist")
        return self.locations[objectID]
    
    def isObjectOfType(self, objectID : int, checkType) -> bool:
        '''
            Name    : isObjectOfType
            Params  : (ID) objectID     := The ID of the object
                      (class) checkType := The type to check the is object is
            Purpose : Returns if the object is of the suspected type
            Return  : (bool) Whether the object is the given type
        '''

        outputLn("> In isObjectOfType")
        gameObject = self.getObject(objectID)
        outputLn(":::: isObjectOfType: " + str(gameObject))
        if not gameObject:
            return False
        
        return isinstance(gameObject, checkType)
    
    
    def __getAtID(self, position : tuple) -> int | None: 
        return self.positions[position] if position in self.positions else None
    
    def __setAtID(self, objectID : int, position : tuple) -> None: 
        self.locations[objectID] = position 
        self.positions[position] = objectID 

    def __getIDPosition(self, objectID : int) -> tuple | None:
        return self.locations[objectID] if objectID in self.locations else None

    def __getIDUnder(self, objectID : int) -> int | None:
        return self.onTopOf[objectID] if objectID in self.onTopOf else None
    
    def __setOnTopOf(self, objectID : int, position : tuple):
        idAtPosition = self.__getAtID(position) 
        self.onTopOf[objectID] = idAtPosition
        self.__setAtID(objectID, position)

    def __takeOffTop(self, objectID : int, position : tuple): 
        idUnder = self.__getIDUnder(objectID)
        del self.onTopOf[objectID]
        if idUnder:
            self.__setAtID(idUnder, position)
        else:
            del self.positions[position]