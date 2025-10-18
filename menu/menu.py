from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
from .credits import Credits
import pygame

class Menu:
    def __init__(self):
        self.state = "main_menu"

        self.play_button = Button('resources/buttons/play_paper.jpeg', (-1, 160), height=100, align_x="center")
        self.credits_button = Button('resources/buttons/credits_paper.jpeg', (-1, 300), height=100, align_x="center")

        self.credits = Credits(self)

    def update(self, delta_t, events):
        if self.state == "credits":
            self.credits.update(delta_t, events)
        else:
            if self.play_button.is_clicked():
                engine.mode = Modes.game
            elif self.credits_button.is_clicked():
                self.state = "credits"

    def render(self):
        
        if self.state == "credits":
            self.credits.render()
        
        else:
            engine.fill((60, 60, 60))
            
            paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1000, 600))
            engine.render_image(paper_background, (0, 0))

            self.play_button.render()
            self.credits_button.render()

            title = engine.render_text("pixel", 48, "KUL Game Jam 2025", (255, 255, 255))
            engine.render_image(title, (250, 20))


menu = Menu() # singleton