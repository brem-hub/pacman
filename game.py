import pygame
from pysmile.game import Game as PSGame
from scenes.menu import MenuScene
from scenes.main import MainScene
from scenes.base import Scene
from pysmile.components.exit_on_escape import ExitOnEscape
from pysmile.component import Component

from settings import Settings


class Game(PSGame):
    def __init__(self, width=1024, height=768):
        pygame.display.init()
        pygame.font.init()
        pygame.mixer.init()
        super().__init__()

        self.screen = None
        self.setup_default_components((width, height))
        self.current_scene = MenuScene
        self.add_component(ExitOnEscape())
        self.settings = Settings()

    def __setattr__(self, key, value):
        if key == "current_scene":
            if isinstance(self.scene, Scene):
                self.scene.removed()

            if isinstance(value, Scene):
                self.scene = value
            else:
                self.scene = value(self)

            self.scene.bind_events()
            for comp in self.get_components(Component):
                comp.scene = self.scene
        else:
            object.__setattr__(self, key, value)

    def main_loop(self):
        self.run()

    @property
    def width(self):
        return self.screen_size[0]

    @property
    def height(self):
        return self.screen_size[1]
