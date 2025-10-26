from engine import engine, Modes
import pygame
from .plate.fragment import Fragment
from .plate.plate_supervisor import PlateSupervisor
from .stats import Stats
from .loading_bar import Loadingbar
from .game_over_screen import Gameoverscreen
from .golden_poop import Goldenpoop
import random

class Game:
    def __init__(self):
        self.wave_number = 0        
        # self.hond = Hond()
        self.floor_image=pygame.transform.scale(engine.get_image('resources/images/Floor.png'),(engine.DISPLAY_W,0.42*engine.DISPLAY_H))
        self.repeating_cupboard=3
        self.cupboard_game_background=pygame.transform.scale(engine.get_image('resources/images/cupboard.png'),(engine.DISPLAY_W/self.repeating_cupboard,0.6*engine.DISPLAY_H))
        self.elephant_ass=engine.get_image("resources/images/elephant_ass.png")
        self.elephant_ass=pygame.transform.scale_by(self.elephant_ass,0.2)
        self.width_elephant_ass, self.length_elephant_ass=self.elephant_ass.get_size()
        self.stats = Stats()
        self.loading_bar = Loadingbar()
        self.gameoverscreen = Gameoverscreen(self)
        self.plate_supervisor = PlateSupervisor(self, self.loading_bar, self.stats)
        self.plate_supervisor.spawn_plate()
        self.golden_poop = Goldenpoop()
        self.time_until_gouden_kak = 0 # random.normalvariate(10, 5)
    
    def play_again(self):
        self.time_until_gouden_kak = 0 #random.normalvariate(10, 5)
        self.wave_number = 0
        self.repeating_cupboard=3
        # self.elephant_ass=pygame.transform.scale_by(self.elephant_ass,0.2)
        # self.width_elephant_ass, self.length_elephant_ass=self.elephant_ass.get_size()
        self.stats.play_again()
        self.loading_bar = Loadingbar()
        self.gameoverscreen = Gameoverscreen(self)
        self.plate_supervisor = PlateSupervisor(self, self.loading_bar, self.stats)
    
    def back_to_main_menu(self):
        engine.mode = Modes.main_menu

    def update(self, delta_t: float, events: list):
        if self.stats.gouden_kak_bought:
            self.time_until_gouden_kak -= delta_t
        if self.time_until_gouden_kak <= 0:
            # spawn
            self.golden_poop.golden_poop_appears()
        if self.time_until_gouden_kak <= 3:
            # set new poop
            self.time_until_gouden_kak = random.normalvariate(10, 5)
        if self.golden_poop.captured:
            # CAPTURED
            self.golden_poop.captured = False
            self.stats.add_money(1000)
            # Effects
            self.plate_supervisor.fragments = []
            for i in range(12):
                engine.spawn_particles((i*100, 50), count=20, color=(255,200,60), spread=30, speed=200, lifetime=4, radius=5)
            engine.spawn_particles((self.golden_poop.x_goldenpoop, self.golden_poop.y_goldenpoop), count=100, color=(255,200,60), spread=30, speed=200, lifetime=5, radius=5, gravity=0)
            self.golden_poop.y_goldenpoop = 1000 # out of screen
        
        
        if self.stats.lives > 0:
            self.plate_supervisor.update(delta_t, events)
        
            self.stats.update(delta_t,events)
            self.loading_bar.update(delta_t,events)
            self.golden_poop.update(delta_t,events)
        else:
            self.gameoverscreen.update(delta_t,events,self.stats,self.loading_bar)
        
    def render(self):
        engine.fill((0, 0, 0))
        self.plate_supervisor.prerender()
        engine.render_image(self.floor_image,(0,engine.DISPLAY_H*0.58))
        for cupboard_nr in range(self.repeating_cupboard):
            engine.render_image(self.cupboard_game_background,(cupboard_nr*engine.DISPLAY_W/self.repeating_cupboard,0))
        engine.render_image(self.elephant_ass,(engine.DISPLAY_W/2-self.width_elephant_ass/2,engine.DISPLAY_H-self.length_elephant_ass-50))
        self.plate_supervisor.render()
        self.stats.render()
        self.loading_bar.render()
        if self.stats.lives <=0:
            self.gameoverscreen.render()
            self.stats.gouden_kak_bought = False
        self.golden_poop.render()

    
game = Game()