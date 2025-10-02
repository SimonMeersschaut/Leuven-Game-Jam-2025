import pygame
from engine.scene import Scene

class LoadingScene(Scene):
    """A scene for loading assets."""

    def __init__(self):
        super().__init__()

    def load(self, engine):
        pygame.font.init()
        self.font = pygame.font.SysFont("Arial", 50)
        self.text = self.font.render("Loading...", True, (255, 255, 255))

    def render(self, engine):
        engine.screen.fill((0, 0, 0))
        engine.screen.blit(self.text, (engine.screen.get_width() / 2 - self.text.get_width() / 2, engine.screen.get_height() / 2 - self.text.get_height() / 2))
