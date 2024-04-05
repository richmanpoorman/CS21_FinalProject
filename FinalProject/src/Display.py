from Board import Board 
import pygame as py
import sys
import GameObject # just for testing
import random

class Display:
    def __init__(self,dimension: tuple[int, int] = (10, 12)):
        self.board = Board(dimension)
        self.dim = dimension
        self.window = py.display.set_mode(self.dim)

    def updateDisplay(self) -> None:
        visual = self.board.getBoard()
        rows, cols = self.board.size

        for r in range(rows):
            for c in range(cols):
                obj = visual[r][c]
                suf = obj.getSurface()
                self.window.blit(suf, (300, 250))

                py.display.update()
        

    def receiveUpdate(self, update : map) -> None:
        pass 
    



###################
#
# Testing Fuctions
#
###################

test_display = Display((800, 600))
obj1 = GameObject((200,100))
obj2 = GameObject((400, 100))
test_display.board.addObject(obj1, (random.randint(0, 800)
                                    , random.randint(0,600)))
test_display.board.addObject(obj2, (random.randint(0, 800)
                                    , random.randint(0,600)))

test_display.updateDisplay()