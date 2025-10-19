from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
import pygame

class Credits:
    def __init__(self, main_menu):
        self.state = "main_menu"
        self.back_button = Button('resources/buttons/back_paper.jpeg', (-1, 400), height=100, align_x="center")
        self.main_menu = main_menu
        
        self.credits_text = Sprite('resources/buttons/credits_list_paper.png', (-1, 0), 2448/6, align_x="center")


    def update(self):
        self.back_button.update()
        
        if self.back_button.is_clicked():
            self.main_menu.state = "main_menu"
            

    def render(self):
        engine.fill((60, 60, 60))
        
        paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1000, 600))
        engine.render_image(paper_background, (0, 0))

        self.back_button.render()
        
        self.credits_text.render()