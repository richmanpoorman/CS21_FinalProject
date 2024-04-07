from pygame import Surface 

class GameObject:
    def __init__(self, surface : Surface):
        self.setSurface(surface)
        self.onTopOf = None

    def getSurface(self) -> Surface: 
        return self.surface

    def setSurface(self, surface : Surface) -> None:
        self.surface = surface
