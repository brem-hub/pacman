import pygame
from pysmile.renderer import PyGameRenderer


class ObjectRenderer(PyGameRenderer):
    def __init__(self, obj):
        super().__init__()
        self.obj = obj

    def render(self, entity, rect):
        self.obj.game.screen = pygame.Surface(rect.size)
        self.obj.game.screen.set_colorkey((0, 0, 0))
        self.obj.process_draw()
        return self.obj.game.screen
