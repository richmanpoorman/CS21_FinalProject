
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as py
from Display import Display
from GameObject import GameObject
import random as rd
###################
#
# Testing Stuff
#
###################

py.init()

# Create a Display object
dis = Display()
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ROWS, COLS = dis.size
image_path = "/Users/timi/Downloads/pac_man.jpg"
# Create GameObjects and add them to the display
for r in range(ROWS):
    for c in range(COLS):
        if r == 0 and c == 0:
            surf = py.image.load(image_path)
        else:
            surf = py.Surface((rd.randint(10, 50),rd.randint(36, 90)))
            surf.fill(GREEN)
        # if (r % 2) == 0:
        #     surf.fill(RED)
        dis.board[r][c] = GameObject(surf)

dis.display_window()

py.quit()
