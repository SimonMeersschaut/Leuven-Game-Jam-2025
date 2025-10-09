import pygame
from engine import Engine
from scenes import Scene

class GameScene(Scene):
    """A scene for the main game."""

    def __init__(self):
        super().__init__()

    def load(self, engine: Engine):
        self.font = engine.get_font("pixel", 40)
        self.text = self.font.render("Game Scene", True, (255, 255, 255))

    def render(self, engine: Engine, events: list, dt: float):
        engine.fill((0, 0, 0))
        engine.blit(self.text, (engine.get_width() / 2 - self.text.get_width() / 2, engine.get_height() / 2 - self.text.get_height() / 2))
