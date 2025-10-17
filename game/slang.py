from engine import engine 
import pygame
import random

class Snake:
    def __init__(self):
        self.slang_image = engine.get_image('resources/images/snake_jump_obstacle.png')
        self.slang_image = pygame.transform.scale_by(self.slang_image,0.4)
        self.x=random.randint(100,900)
        self.y=random.randint(100,500)
        self.slang_image_button=self.slang_image.get_rect(topleft=(self.x,self.y))

    def update(self, delta_t: float, events: list):
        mouse_pos = pygame.mouse.get_pos()
        # print(mouse_pos)
        if self.slang_image_button.collidepoint(mouse_pos):
            # print('dit lukt')
            for event in events:
                if event.type==pygame.MOUSEBUTTONDOWN:
                    self.x=random.randint(1,1000)
                    self.y=random.randint(1,600)
                    self.slang_image_button=self.slang_image.get_rect(topleft=(self.x,self.y))


    def render(self):
        engine.render_image(self.slang_image,(self.x,self.y))

