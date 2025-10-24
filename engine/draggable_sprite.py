import resources
from engine import Engine, engine, Modes
from engine.sprite import Sprite
import pygame

class Draggable_Sprite(Sprite):
    def __init__(self, image_path, position=(100, 100), height=None, width=None):
        super().__init__(image_path, position, height, width)
        
        self.holding = False

    def update(self):
        if self.is_clicked():
            self.holding = True
        if not self.is_clicked():
            self.holding = False

        if self.holding:
            self.scale_factor(1.1)
            self.move(pygame.mouse.get_pos()[0] - self.true_width*1.1 // 2, pygame.mouse.get_pos()[1] - self.true_height*1.1 // 2)
        else:
            self.scale_factor(1.0)
            
            
    def render(self):
        super().render()