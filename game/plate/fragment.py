from engine import engine 
from engine.draggable_sprite import DraggableSprite
import pygame

class Fragment(DraggableSprite):
    def __init__(self, left_gold_glue, surface, right_gold_glue, position=(100, 100), height=None, width=None):
        super().__init__(surface, position, height, width)
 
    def update(self):
        super().update()

    def render(self):
        super().render()