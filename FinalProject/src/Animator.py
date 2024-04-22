import pygame as py
from GameObject import GameObject
import Pellet
import Player
import Ghost
class Animator:
    def __init__(self, imgs:list[str], obj:GameObject):
        self.imgs = imgs
        self.surfaces = [py.image.load(x) for x in imgs]
        self.type = Player if isinstance(obj, Player) else \
                    Ghost if isinstance(obj, Ghost) else \
                    Pellet
        
    def get_frame(self, frame_id:int, obj):
        
        return self.surfaces[frame_id] if isinstance(obj, self.type) else \
                             None
    

class PacMan_Animator:
    # animations variable can be changed, wanted to have a dict
    # where each direction coresponded to an Animator
    def __init__(self, animations:list[list[str]]):
        self.frames = dict()
        self.dir = ["left", "right", "up", "down"]
        for i in range(len(self.dir)):
            self.frames[self.dir[i]] = Animator(animations[i], obj=Player())

    def getAsurface(self, dir:str, frame_id:int):
        obj = self.frames[dir]
        return obj.get_frame(frame_id)
    
    

