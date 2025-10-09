import pygame
from engine import Engine
from scenes.scene import Scene

class MenuScene(Scene):
    """A scene for the main menu."""

    def __init__(self):
        super().__init__()

    def load(self, engine: Engine):
        self.title_font = engine.get_font("pixel", 80)
        self.button_font = engine.get_font("pixel", 50)
        self.title = self.title_font.render("My Game", True, (255, 255, 255))
        self.start_button = self.button_font.render("Start", True, (255, 255, 255))
        self.start_button_rect = self.start_button.get_rect()

        self.start_button_rect.center = (engine.get_width() / 2, engine.get_height() / 2)

    def render(self, engine: Engine, events: list, dt: float):
        engine.fill((0, 0, 0))
        engine.blit(self.title, (engine.get_width() / 2 - self.title.get_width() / 2, 100))
        engine.blit(self.start_button, self.start_button_rect)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    engine.switch_scene("GAME")
