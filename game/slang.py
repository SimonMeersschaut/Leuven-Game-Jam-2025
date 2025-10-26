from engine import engine 
import pygame
import random
from .golden_poop import Goldenpoop

class Snake:
    def __init__(self):
        self.slang_image = engine.get_image('resources/images/snake_jump_obstacle.png')
        self.slang_image = pygame.transform.scale_by(self.slang_image,0.4)
        self.x=random.randint(100,900)
        self.y=random.randint(100,500)
        self.slang_image_button=self.slang_image.get_rect(topleft=(self.x,self.y))

    def update(self, delta_t: float, events: list,loading_bar,stats,golden_poop):
        mouse_pos = pygame.mouse.get_pos()
        if self.slang_image_button.collidepoint(mouse_pos):
            for event in events:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.x=random.randint(1,1000)
                    self.y=random.randint(1,600)
                    self.slang_image_button=self.slang_image.get_rect(topleft=(self.x,self.y))
                    stats.lose_life()
                    stats.add_money(1)
                    loading_bar.start_wave(2)
                    golden_poop.golden_poop_appears()
                    

    def render(self):
        engine.render_image(self.slang_image,(self.x,self.y))

