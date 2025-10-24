from engine import engine 
import pygame
from .hond import Hond
from .slang import Snake
from .plate.fragment import Fragment

class Game:
    def __init__(self):
        self.hond = Hond()
        self.slang = Snake()
        self.plate_1 = Fragment("resources/images/plate.png", width=200)
        self.plate_2 = Fragment("resources/images/plate.png", width=150)
 
    def update(self, delta_t: float, events: list):
        self.hond.update(delta_t, events)
        self.slang.update(delta_t,events)
        self.plate_1.update()
        # self.plate_2.update()

    def render(self):
        engine.fill((0, 0, 0))
        self.hond.render()
        self.slang.render()
        self.plate_1.render()
        self.plate_2.render()

    
game = Game()