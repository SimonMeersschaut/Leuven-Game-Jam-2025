from engine import Engine, engine, Modes
from engine import sprite as btn
import pygame

class Credits:
    def __init__(self, main_menu):
        self.state = "main_menu"
        self.back_button = btn.Button('resources/buttons/back_paper.jpeg', (400, 400), height=100)
        self.main_menu = main_menu

    def update(self, delta_t, events):
        if self.back_button.is_clicked():
            self.main_menu.state = "main_menu"
            

    def render(self):
        engine.fill((60, 60, 60))
        
        paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1000, 600))
        engine.render_image(paper_background, (0, 0))

        self.back_button.render()

        credits_text = pygame.transform.scale(engine.get_image('resources/buttons/credits_list_paper.png'), (2448/6, 3262/6))
        engine.render_image(credits_text, (500 - credits_text.get_width()/2, -100))