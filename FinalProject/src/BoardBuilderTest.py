
from BoardBuilder import BoardBuilder 
from Display import Display 
import pygame as py 
from time import sleep 

py.init() 
board, _ = BoardBuilder((10, 11))\
    .addWall((0, 0))\
    .addGhost((0, 1))\
    .getBoard()

display = Display()

print(board.getBoard())

display.receiveUpdate(board.getBoard())

display.display_window()
py.quit() 