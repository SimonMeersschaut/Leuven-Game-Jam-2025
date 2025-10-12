from engine import Engine, engine, Modes
import pygame

class Menu:
    def __init__(self):
        ...
    
    def update(self, delta_t, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                engine.mode = Modes.game

    def render(self):
        engine.fill((60, 60, 60))

        surf = engine.render_text("pixel", 48, "KUL Game Jam 2025", (255, 255, 255))
        engine.render_image(surf, (250, 20))

    

menu = Menu() # singleton