from Display import Display
from InputListener import InputListener
from Board import Board

from GameObject import GameObject
from Ghost import Ghost 
from InputListener import InputListener
from Pellet import Pellet
from PowerPellet import PowerPellet
from Player import Player
from Wall import Wall 


from Erpy import stdio_port_connection
from term import Atom

from sys import stdout
from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
import pygame as py


inbox, port = stdio_port_connection()
for i in range(100):
    port.send((Atom("atom"), i))