from pygame import Surface 

class GameObject:
    def __init__(self, surface : Surface | None):
        self.setSurface(surface)
        self.onTopOf = None

    def getSurface(self) -> Surface | None: 
        return self.surface

    def setSurface(self, surface : Surface | None) -> None:
        self.surface = surface
