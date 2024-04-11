from Display import Display
import pygame as py
from GameObject import GameObject
###################
#
# Testing Stuff
#
###################

py.init()

# Create a Display object
# ROWS = 500
# COLS = 500
dis = Display()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ROWS, COLS = dis.size

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