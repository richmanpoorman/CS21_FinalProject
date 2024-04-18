from GameObject import GameObject

from os import environ 
environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
from pygame import Surface 

class Wall(GameObject):
    def __init__(self):
        super().__init__(None)

    def getSurface(self) -> Surface | None:
        surface = Surface((200, 200))
        surface.fill((100, 200, 0))
        return surface
    
    def pack(self) -> tuple[str, dict[str, str]]:
        return ("wall", dict())
    
    def unpack(self, data : dict):
        pass