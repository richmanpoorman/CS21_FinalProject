from pygame import Surface 

class GameObject:
    def __init__(self, position : tuple, surface : tuple):
        self.setPosition(position)
        self.setSurface(surface)

    def getPosition(self) -> tuple:
        return self.position

    def setPosition(self, position : tuple) -> None:
        self.position = position 

    def getSurface(self) -> Surface: 
        return self.surface

    def setSurface(self, surface : Surface) -> None:
        self.surface = surface