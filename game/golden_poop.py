from engine import engine
from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
import pygame

class Goldenpoop:
    def __init__(self):
        self.golden_poop_button=Button('resources/buttons/golden_poop.png', (engine.DISPLAY_W/2, 160), height=100, align_x="center")
        self.speed=500
        self.golden_poop=False
        self.y_goldenpoop=0
        self.captured=False

    def update(self, delta_t: float, events: list):
        if self.golden_poop:
            self.y_goldenpoop+=self.speed*delta_t
            self.golden_poop_button.move(engine.DISPLAY_W/2,self.y_goldenpoop)
            if self.golden_poop_button.update_and_check_clicked():
                self.captured=True
            if self.y_goldenpoop>engine.DISPLAY_H:
                self.golden_poop=False            

    def golden_poop_appears(self):
        self.x_goldenpoop=engine.DISPLAY_W/2
        self.y_goldenpoop=engine.DISPLAY_H/2
        self.golden_poop=True

    def render(self):
        if self.golden_poop:
            self.golden_poop_button.render()


        



