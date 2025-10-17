from engine import Engine, engine, Modes
from engine import button as btn
import pygame

class Menu:
    def __init__(self):
        self.state = "main_menu"
        self.buttons = []
        
        self.play_button = btn.Button('resources/buttons/play_paper.jpeg', (400, 160), height=100)
        self.credits_button = btn.Button('resources/buttons/credits_paper.jpeg', (400, 300), height=100)

    def update(self, delta_t, events):
        if self.play_button.is_clicked():
            engine.mode = Modes.game
        elif self.credits_button.is_clicked():
            self.state = "credits"

    def render(self):
        engine.fill((60, 60, 60))
        
        paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1000, 600))
        engine.render_image(paper_background, (0, 0))

        self.play_button.render()
        self.credits_button.render()

        if self.state == "main_menu":
            title = engine.render_text("pixel", 48, "KUL Game Jam 2025", (255, 255, 255))
            engine.render_image(title, (250, 20))
        
        elif self.state == "credits":
            
            credits_text = pygame.transform.scale(engine.get_image('resources/buttons/credits_list_paper.png'), (2448/6, 3262/6))
            engine.render_image(credits_text, (500 - credits_text.get_width()/2, -100))

            back_button = pygame.transform.scale(engine.get_image('resources/buttons/back_paper.jpeg'), (200, 100))
            engine.render_image(back_button, (400, 400))


menu = Menu() # singleton