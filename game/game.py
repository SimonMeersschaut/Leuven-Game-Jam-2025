from engine import engine 
import pygame
from .hond import Hond
from .slang import Snake
from .stats import Stats
from .loading_bar import Loading_bar

class Game:
    def __init__(self):
        self.hond = Hond()
        self.slang = Snake()
        self.stats = Stats()
        self.loading_bar = Loading_bar()
 
    def update(self, delta_t: float, events: list):
        self.hond.update(delta_t, events)
        self.slang.update(delta_t,events,self.loading_bar,self.stats)
        self.stats.update(delta_t,events)
        self.loading_bar.update(delta_t,events)

    def render(self):
        engine.fill((0, 0, 0))
        self.hond.render()
        self.slang.render()
        self.stats.render()
        self.loading_bar.render()

    
game = Game()