from Board import Board 
from GameObject import GameObject 
from Interactable import Interactable
from Player import Player 
from Ghost import Ghost 
from Wall import Wall 
from Pellet import Pellet 
from PowerPellet import PowerPellet 



def makeBoard():
    board = Board()

def makeSmallBoard():
    board = Board((2, 2))

def getBoard():
    board = Board((2, 2)) 
    boardArr = board.getBoard() 
    print(boardArr)

def addObjectToBoard():
    board = Board((2, 2))
    testObject = GameObject(None)
    board.addObject(testObject, (0, 0))
    print(board.getBoard()) 
    assert testObject == board.getAt((0, 0)), "Not the same: got " + str(testObject) + " and " + str(board.getAt((0, 0)))
    

def addMultipleObjectToBoard():
    board = Board((2, 2))
    testP = Player(None) 
    testI = Interactable(None)
    testG = Ghost(None)
    testW = Wall(None)
    board.addObject(testP, (0, 0))
    board.addObject(testI, (0, 1))
    board.addObject(testG, (1, 0))
    board.addObject(testW, (1, 1))
    print(board.getBoard())
    assert testP == board.getAt((0, 0)), "Not the same: got " + str(testP) + " and " + str(board.getAt((0, 0)))
    assert testI == board.getAt((0, 1)), "Not the same: got " + str(testI) + " and " + str(board.getAt((0, 1)))
    assert testG == board.getAt((1, 0)), "Not the same: got " + str(testG) + " and " + str(board.getAt((1, 0)))
    assert testW == board.getAt((1, 1)), "Not the same: got " + str(testW) + " and " + str(board.getAt((1, 1)))
    

def addOnTop():
    board = Board((2, 2))

    test1 = GameObject(None) 
    test2 = GameObject(None) 

    board.addObject(test1, (1, 1))
    board.addObject(test2, (1, 1))

    assert test2 == board.getAt((1, 1)), "1: Got: " + str(board.getAt((1, 1)))
    assert [test2, test1] == board.getAtAll((1, 1)), "2: Got: " + str(board.getAtAll((1, 1)))

    testG = Ghost(None)
    testP = Player(None) 
    testI = Interactable(None) 
    
    board.addObject(testI, (0, 0))
    board.addObject(testP, (0, 0))
    board.addObject(testG, (0, 0)) 

    print(board.getBoard())
    assert testG == board.getAt((0, 0)), "Not the same: got " + str(testG) + " and " + str(board.getAt((0, 0)))
    assert [testG, testP, testI] == board.getAtAll((0, 0)), "Got " + str(board.getAtAll((0, 0)))

def moveTest():
    board = Board((2, 2)) 
    test = GameObject(None) 
    testID = board.addObject(test, (0, 0))
    board.moveObject(testID, (1, 1))
    assert board.getAt((0, 0)) == None, "Not Empty (0, 0)"
    assert board.getAt((1, 1)) == test, "Board has " + str(board.getAt((1, 1)))
    print(board.getBoard())

def moveStacked():
    board = Board((2, 2))
    test1 = GameObject(None) 
    test2 = GameObject(None) 
    t1 = board.addObject(test1, (0, 0)) 
    t2 = board.addObject(test2, (0, 0))
    board.moveObject(t2, (1, 1))
    print(board.getBoard())
    assert board.getAt((0, 0)) == test1, "Board has (0, 0) = " + str(board.getAt((0, 0)))
    assert board.getAt((1, 1)) == test2, "Board has (1, 1) = " + str(board.getAt((1, 1)))

def removeObject():
    board = Board((2, 2)) 
    test = GameObject(None) 
    t = board.addObject(test, (0, 0))
    removed = board.removeObject(t)
    print(board.getBoard())
    assert removed == test, "Wrong Object: " + str(removed)
    assert board.getAt((0, 0)) == None, "Object: " + board.getAt((0, 0))

def removeStacked(): 
    board = Board((2, 2)) 
    test1 = GameObject(None) 
    test2 = GameObject(None) 
    t1 = board.addObject(test1, (0, 0)) 
    t2 = board.addObject(test2, (0, 0)) 
    removed = board.removeObject(t2) 
    print(board.getBoard())
    assert removed == test2, "Wrong Object: " + str(removed) 
    assert board.getAt((0, 0)) == test1, "Wrong (0, 0): " + board.getAt((0, 0))

tests = [makeBoard, 
         makeSmallBoard, 
         getBoard, 
         addObjectToBoard, 
         addMultipleObjectToBoard,
         addOnTop,
         moveTest,
         moveStacked,
         removeObject,
         removeStacked] 
testID = 1
for test in tests:
    print("TestID: ", testID)
    try:
        test() 
    except Exception as e:
        print("Exception: ", e)
    print("Test Done\n")
    testID += 1
