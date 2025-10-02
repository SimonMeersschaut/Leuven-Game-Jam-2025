import pygame
from engine.scene import Scene

class MenuScene(Scene):
    """A scene for the main menu."""

    def __init__(self):
        super().__init__()

    def load(self, engine):
        pygame.font.init()
        self.title_font = pygame.font.SysFont("Arial", 80)
        self.button_font = pygame.font.SysFont("Arial", 50)
        self.title = self.title_font.render("My Game", True, (255, 255, 255))
        self.start_button = self.button_font.render("Start", True, (255, 255, 255))
        self.start_button_rect = self.start_button.get_rect()

        self.start_button_rect.center = (engine.screen.get_width() / 2, engine.screen.get_height() / 2)

    def render(self, engine):
        engine.screen.fill((0, 0, 0))
        engine.screen.blit(self.title, (engine.screen.get_width() / 2 - self.title.get_width() / 2, 100))
        engine.screen.blit(self.start_button, self.start_button_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button_rect.collidepoint(event.pos):
                    engine.switch_scene("GAME")
