from Board import Board 
import pygame as py
import sys
from GameObject import GameObject # just for testing
import random
import numpy as np

class Display:
    def __init__(self,dimension: tuple[int, int] = (10, 12)):
        '''
            Name    : init
            Params  : (dimension) tuple[int, int] := optional parameter that has the 
                      width and height of the board
            Purpose : initalize specific class variables
            Return  : N/A
        '''
        self.board = np.empty(dimension, dtype=GameObject)
        self.dim = dimension
        #(self.window) is the display surface that is shown on the screen 
        self.window = py.display.set_mode(self.dim)
        self.window.fill((0,0,0)) # initalize the screen to be blank

    def updateDisplay(self) -> None:

        '''
            Name    : __updateDisplay
            Params  : N/A
            Purpose : Update the display window with all the gameObjects in the board
            Return  : N/A
        '''

        rows, cols = self.dim

        for r in range(rows):
            for c in range(cols):
                obj = self.board[r][c]
                suf = obj.getSurface()
                # MUST UPDATE WHAT SIZE EACH GAMEOBJECT SHOULD BE
                self.window.blit(suf, (r * 10, c * 10))
        
    
        py.display.update()

        
    def display_window(self):
        '''
            Name    : display_window
            Params  : N/A
            Purpose : To display the self.window to the screen 
            Return  : N/A
        '''
        run = True
        while run:
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False

            self.__updateDisplay()
        

    def receiveUpdate(self, newBoard: Board) -> None:
       self.Board = newBoard
       self.__updateDisplay()
       
    



###################
#
# Testing Stuff
#
###################

py.init()

# Create a Display object
ROWS = 500
COLS = 500
dis = Display((COLS, ROWS))
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


# Create GameObjects and add them to the display
for c in range(COLS):
    for r in range(ROWS):
        surf = py.Surface((10, 10))
        surf.fill(GREEN)
        if (c % 2) == 0:
            surf.fill(RED)
        dis.board[c][r] = GameObject(surf)

dis.display_window()

py.quit()

