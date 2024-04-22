
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as py
from GameObject import GameObject
import numpy as np
import random as rand


from Board import Board
from threading import Lock, Thread

SCALE_FACTOR = 50
WINDOW_DIM = (Board.BOARD_SIZE[1] * SCALE_FACTOR, Board.BOARD_SIZE[0] * SCALE_FACTOR)
class Display:
    def __init__(self, dimension : tuple[int, int] = WINDOW_DIM):
        '''
            Name    : init
            Params  : (dimension) tuple[int, int] := optional parameter that has the 
                      width and height of the board
            Purpose : initalize specific class variables
            Return  : N/A
        '''
        
        self.board = np.empty(Board.BOARD_SIZE, dtype=GameObject)
        self.size = Board.BOARD_SIZE
        self.dim = dimension
        
        self.boardLock = Lock()
        self.frameCount = 
        #(self.window) is the display surface that is shown on the screen 
        self.window = py.display.set_mode(self.dim)

    def updateDisplay(self) -> None:

        '''
            Name    : updateDisplay
            Params  : N/A
            Purpose : Update the display window with all the gameObjects in the board
            Return  : N/A
        '''
        # self.window.fill((0, 0, 0))
        # rows, cols = self.size
        # dim_col, dim_row = WINDOW_DIM
        # #Get the size of any surface in each cell of the display window
        # cell_width = (dim_col // cols)
        # cell_height = (dim_row // rows)

        # for r in range(rows):
        #     for c in range(cols):
        #         obj = self.board[r][c]
        #         if not obj: # Checks that it is not none
        #             continue
        #         suf = obj.getSurface()
        #         #scale the sufarce gotten from the board
        #         newSuf = py.transform.scale(suf, (cell_width, cell_height))
        #         # calculate the new postion of the surface in the bigger display window
        #         x = c * cell_width
        #         y = r * cell_height
        #         # Draw the upscaled surfaces onto the screen window
        #         self.window.blit(newSuf, (x , y))
        
        # py.display.update()

        thread = Thread(target = self.__movingUpdate)
        thread.start()

    
    def __movingUpdate(self):

        with self.boardLock:
            self.window.fill((0, 0, 0))
            rows, cols = self.size
            dim_col, dim_row = WINDOW_DIM
            #Get the size of any surface in each cell of the display window
            cell_width = (dim_col // cols)
            cell_height = (dim_row // rows)

            for r in range(rows):
                for c in range(cols):
                    obj = self.board[r][c]
                    if not obj: # Checks that it is not none
                        continue
                    suf = obj.getSurface()
                    #scale the sufarce gotten from the board
                    newSuf = py.transform.scale(suf, (cell_width, cell_height))
                    # calculate the new postion of the surface in the bigger display window
                    x = c * cell_width
                    y = r * cell_height
                    # Draw the upscaled surfaces onto the screen window
                    self.window.blit(newSuf, (x , y))
            
            py.display.update()

    def display_window(self):
        '''
            Name    : display_window (for testing only)
            Params  : N/A
            Purpose : To display the self.window to the screen 
            Return  : N/A
        '''
        run = True
        while run:
            for event in py.event.get():
                if event.type == py.QUIT:
                    run = False

            self.updateDisplay()
        

    def receiveUpdate(self, newBoard : np.ndarray) -> None:
       self.board = newBoard
       self.size  = newBoard.shape
       self.updateDisplay()
       