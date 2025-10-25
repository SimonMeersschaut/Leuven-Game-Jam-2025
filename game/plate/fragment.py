from engine import engine 
from engine.draggable_sprite import DraggableSprite
import pygame

class Fragment(DraggableSprite):
    def __init__(self, image_path="resources/images/plate.png", position=(100, 100), height=None, width=None):
        super().__init__(image_path, position, height, width)
 
    def update(self):
        super().update()

    def render(self):
        super().render()