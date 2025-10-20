from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
import pygame

class Credits:
    def __init__(self, main_menu):
        self.state = "main_menu"
        self.back_button = Button('resources/buttons/back_paper.jpeg', (-1, 600), height=100, align_x="center")
        self.main_menu = main_menu
        
        self.credits_text = Sprite('resources/buttons/credits_list_paper.png', (-1, 200), 2448/6, align_x="center")

        self.paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1920, 1080))


    def update(self):        
        if self.back_button.update_and_check_clicked():
            self.main_menu.state = "main_menu"
            

    def render(self):
        engine.fill((60, 60, 60))
        
        engine.render_image(self.paper_background, (0, 0))

        self.back_button.render()
        
        self.credits_text.render()