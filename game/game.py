from engine import engine 
import pygame
from .hond import Hond
from .slang import Snake

class Game:
    def __init__(self):
        self.hond = Hond()
        self.slang = Snake()
 
    def update(self, delta_t: float, events: list):
        self.hond.update(delta_t, events)
        self.slang.update(delta_t,events)

    def render(self):
        engine.fill((0, 0, 0))
        self.hond.render()
        self.slang.render()

    
game = Game()