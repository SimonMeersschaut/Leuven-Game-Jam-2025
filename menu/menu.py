from engine import Engine, engine, Modes
import pygame

class Menu:
    def __init__(self):
        ...
    
    def update(self, delta_t, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] in range(400, 600) and pygame.mouse.get_pos()[1] in range(160, 240):
                    engine.mode = Modes.game
                elif pygame.mouse.get_pos()[0] in range(400, 600) and pygame.mouse.get_pos()[1] in range(300, 380):
                    engine.mode = Modes.credits

    def render(self):
        engine.fill((60, 60, 60))

        surf = engine.render_text("pixel", 48, "KUL Game Jam 2025", (255, 255, 255))
        engine.render_image(surf, (250, 20))
        engine.render_image(engine.get_image('resources/buttons/play.png') , (400, 160))
        engine.render_image(engine.get_image('resources/buttons/credits.png') , (400, 300))

    

menu = Menu() # singleton