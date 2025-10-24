from engine import engine 
import pygame
from .hond import Hond
from .slang import Snake
from engine.draggable_sprite import Draggable_Sprite

class Game:
    def __init__(self):
        self.hond = Hond()
        self.slang = Snake()
        self.draggable_sprite = Draggable_Sprite("resources/images/plate.jpeg")
 
    def update(self, delta_t: float, events: list):
        self.hond.update(delta_t, events)
        self.slang.update(delta_t,events)
        self.draggable_sprite.update()

    def render(self):
        engine.fill((0, 0, 0))
        self.hond.render()
        self.slang.render()
        self.draggable_sprite.render()

    
game = Game()