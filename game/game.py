from engine import engine 
import pygame
from .hond import Hond
from .slang import Snake
from .stats import Stats

class Game:
    def __init__(self):
        self.hond = Hond()
        self.slang = Snake()
        self.stats = Stats()
 
    def update(self, delta_t: float, events: list):
        self.hond.update(delta_t, events)
        self.slang.update(delta_t,events)
        self.stats.update(delta_t,events)

    def render(self):
        engine.fill((0, 0, 0))
        self.hond.render()
        self.slang.render()
        self.stats.render()

    
game = Game()