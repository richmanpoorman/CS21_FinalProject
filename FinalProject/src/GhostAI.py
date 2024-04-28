
from Board import Board
from Ghost import Ghost
from Player import Player
from Wall import Wall
from random import choice

def searchAndFind(ghostID : int, board : Board):
    '''
        Params  : (ID)    ghostID := The ID of the ghost to move
                  (Board) board   := The entire board state
        Purpose : Tries to search and move the ghost AI
        Return  : ([int, int]) The direction to move to
        Note    : THIS IS UNUSED; THERE WERE BUGS, SO A SIMPLER AI WAS USED
    '''
    ghost = board.getObject(ghostID)
    face = ghost.facing
    row, col = board.getPosition(ghostID)
    if ghost.memory == (row, col):
        ghost.memory = None
    elif ghost.memory:
        return face
    
    if not ghost.memory:
        #Directions
        LEFT = (0, -1)
        RIGHT = (0, 1)
        UP = (1, 0)
        DOWN = (-1, 0)

        def _ghost_scan(face:tuple[int, int]):
            start = end = dim = 0
            step = 1
            seen = False

            if face == LEFT:
                start = col - 1 
                dim = row
                step = -1
            elif face == RIGHT:
                start = col + 1
                end = board.size[1]
                dim = row
            elif face == UP:
                start = row - 1
                dim = col
                step = -1
            else:
                dim = col
                start = row + 1
                end = board.size[0]

            for x in range(start, end, step):
                obj = board.getAt((dim, x))
                if isinstance(obj, Player):
                    seen = True
                    ghost.memory = (dim, x)
                    ghost.face = face
                    break
                elif isinstance(obj, Wall):
                    break

            if seen == False:
                return choice([RIGHT, UP, LEFT, DOWN])
        
            return ghost.face
        
    return _ghost_scan(face)


def moveForwardIfPossible(ghostID : int, board : Board) -> tuple: 
    '''
        Params  : (ID)    ghostID := The ID of the ghost to move
                  (Board) board   := The entire board state
        Purpose : Tries to move the ghost in a direction that is possible
        Return  : ([int, int]) The direction to move to
        Note    : THIS IS THE USED AI
    '''
    ghost         = board.getObject(ghostID)
    behind        = __getOppositeDirection(ghost.getFacing())
    ghostPosition = board.getPosition(ghostID) 
    allPossible   = [Ghost.LEFT, Ghost.RIGHT, Ghost.UP, Ghost.DOWN]

    # Only choose options that work, that aren't moving backwards
    choiceOptions = [direction 
                        for direction in allPossible 
                        if (direction != behind and 
                            __canGhostMoveTo(direction, ghostPosition, board))
                    ]
    
    if choiceOptions: # If there are possible options
        return choice(choiceOptions)
    return behind # Otherwise backtrack


def __canGhostMoveTo(direction : tuple, position : tuple, 
                     board : Board) -> bool:
    '''
        Params  : ([int, int]) direction := The ID of the ghost to move
                  ([int, int]) position  := The position that ghost started at
                  (Board)      board     := The entire board state
        Purpose : Checks if it legal for the ghost to move in that direction
        Return  : (bool) True if the ghost can move there, false if it can not
    '''
    position = __moveWrap(direction, position, board)
    canMove, objectAtPosition = board.canMoveTo(position)
    if canMove:
        return True 
    if board.isObjectOfType(objectAtPosition, Player): 
        return not board.getObject(objectAtPosition).isInvincible() 
    return False

def __moveWrap(direction : tuple[int, int], position : tuple[int, int], 
               board : Board) -> tuple[int, int]:
        '''
        Params  : ([int, int]) direction := The ID of the ghost to move
                  ([int, int]) position  := The position that ghost started at
                  (Board)      board     := The entire board state
        Purpose : Gets the position after moving in the direction, wrapping 
                  around the edge of the board if needed
        Return  : ([int, int]) The new position after moving
    '''
        w , h  = board.getSize() 
        dx, dy = direction 
        x , y  = position 
        newX, newY = x + dx, y + dy 

        return ((newX + w) % w, (newY + h) % h)

def __getOppositeDirection(direction : tuple) -> tuple:
    '''
        Params  : ([int, int]) direction := The direction to get the opposite of
        Purpose : Gets the opposite direction of the direction given
        Return  : ([int, int]) The opposite direction
    '''
    behind = None 
    match direction:
        case Ghost.UP:
            behind = Ghost.DOWN
        case Ghost.DOWN:
            behind = Ghost.UP 
        case Ghost.LEFT: 
            behind = Ghost.RIGHT 
        case Ghost.RIGHT:
            behind = Ghost.LEFT 
        case _: 
            behind = Ghost.LEFT
    return behind