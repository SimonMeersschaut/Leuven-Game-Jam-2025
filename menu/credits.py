from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
import pygame

class Credits:
    def __init__(self, main_menu):
        self.state = "main_menu"
        self.back_button = Button('resources/buttons/main_menu.png', (-1, 600), height=100, align_x="center")
        self.main_menu = main_menu
        
        self.credits_text = Sprite('resources/images/credits.png', (-1, 100), 2448/6, align_x="center")

        self.credits_background = pygame.transform.scale(pygame.transform.rotate(engine.get_image('resources/images/splash_screen.jpg'),-90), (engine.DISPLAY_W, engine.DISPLAY_H))


    def update(self):        
        if self.back_button.update_and_check_clicked():
            self.main_menu.state = "main_menu"
            

    def render(self):
        engine.fill((60, 60, 60))
        
        engine.render_image(self.credits_background, (0, 0))

        self.back_button.render()
        
        self.credits_text.render()