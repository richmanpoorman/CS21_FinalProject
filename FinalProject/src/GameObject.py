import pygame
class GameObject:
    def __init__(self, surface : pygame.Surface | None = None):
        if surface:
            self.setSurface(surface)

    def getSurface(self) -> pygame.Surface: 
        return self.surface

    def setSurface(self, surface : pygame.Surface) -> None:
        self.surface = surface
