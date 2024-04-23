
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame as py
from GameObject import GameObject
from Movable import Movable
import numpy as np
import random as rand
from pygame.math import lerp

from Board import Board
from threading import Lock, Thread
from pygame.time import delay, Clock

from TestTools import outputLn

SCALE_FACTOR = 50
WINDOW_DIM = (Board.BOARD_SIZE[1] * SCALE_FACTOR, Board.BOARD_SIZE[0] * SCALE_FACTOR)
class Display:
    DOWNTIME = 0.25
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
        self.clock = Clock()
        #(self.window) is the display surface that is shown on the screen 
        self.window = py.display.set_mode(self.dim)

    def updateDisplay(self) -> None:

        '''
            Name    : updateDisplay
            Params  : N/A
            Purpose : Update the display window with all the gameObjects in the board
            Return  : N/A
        '''
        self.__drawScreen()
        steps = 10
        totalTime = 0.1
        framerate = round(steps / totalTime)
        for i in range(steps):
            self.clock.tick(framerate)
            weight = i / steps 
            self.__drawScreen(weight)
            delay(10)
        self.__drawScreen(1)

    def __drawScreen(self, interpolationWeight : float = 1) -> None:
        self.window.fill((0, 0, 0))
        rows, cols = self.size
        dim_col, dim_row = WINDOW_DIM
        #Get the size of any surface in each cell of the display window
        cell_width = (dim_col // cols)
        cell_height = (dim_row // rows)

        for r in range(rows):
            for c in range(cols):
                obj = self.board[r][c]
                if not obj: 
                    continue 

                if isinstance(obj, Movable):
                    self.__drawMovable(obj, interpolationWeight, r, c, cell_width, cell_height)
                else: 
                    self.__drawImmovable(obj, r, c, cell_width, cell_height)
        
        py.display.update()

    def __drawImmovable(self, gameObject : GameObject, r : int, c : int, cell_width : int, cell_height : int):
        suf = gameObject.getSurface()
        #scale the sufarce gotten from the board
        newSuf = py.transform.scale(suf, (cell_width, cell_height))
        # calculate the new postion of the surface in the bigger display window
        x = (c) * cell_width
        y = (r) * cell_height
        # Draw the upscaled surfaces onto the screen window
        self.window.blit(newSuf, (x , y))

    def __drawMovable(self, movable : Movable, interpolationWeight : float, r : int, c : int, cell_width : int, cell_height : int):
        suf = movable.getSurface()
        #scale the sufarce gotten from the board
        newSuf = py.transform.scale(suf, (cell_width, cell_height))
        # calculate the new postion of the surface in the bigger display window
        dirR, dirC = movable.getWentTo()
        dx = lerp(-dirC, 0, interpolationWeight)
        dy = lerp(-dirR, 0, interpolationWeight)
        outputLn(str(dx) + ", " + str(dy))
        x = (c + dx) * cell_width
        y = (r + dy) * cell_height
        # Draw the upscaled surfaces onto the screen window
        self.window.blit(newSuf, (x , y))

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
       