from engine import engine 
import pygame
# from .hond import Hond
from .slang import Snake
from .plate.fragment import Fragment
from .plate.plate_supervisor import PlateSupervisor
from .stats import Stats
from .loading_bar import Loadingbar
from .game_over_screen import Gameoverscreen
from .golden_poop import Goldenpoop

class Game:
    def __init__(self):
        self.wave_number = 0        
        # self.hond = Hond()
        self.slang = Snake()
        self.floor_image=pygame.transform.scale(engine.get_image('resources/images/Floor.png'),(engine.DISPLAY_W,0.42*engine.DISPLAY_H))
        self.repeating_cupboard=3
        self.cupboard_game_background=pygame.transform.scale(engine.get_image('resources/images/cupboard.png'),(engine.DISPLAY_W/self.repeating_cupboard,0.6*engine.DISPLAY_H))
        self.elephant_ass=engine.get_image("resources/images/elephant_ass.png")
        self.elephant_ass=pygame.transform.scale_by(self.elephant_ass,0.2)
        self.width_elephant_ass,self.length_elephant_ass=self.elephant_ass.get_size()
        self.stats = Stats(1)
        self.loading_bar = Loadingbar()
        self.gameoverscreen = Gameoverscreen()
        self.plate_supervisor = PlateSupervisor(self, self.loading_bar, self.stats)
        self.plate_supervisor.spawn_plate()
        self.golden_poop = Goldenpoop()
        

    def update(self, delta_t: float, events: list):
        # self.hond.update(delta_t, events)
        self.slang.update(delta_t,events,self.loading_bar,self.stats,self.golden_poop)
        
        self.plate_supervisor.update(delta_t, events)
        
        self.stats.update(delta_t,events)
        self.loading_bar.update(delta_t,events)
        self.gameoverscreen.update(delta_t,events,self.stats,self.loading_bar)
        self.golden_poop.update(delta_t,events)

    def render(self):
        engine.fill((0, 0, 0))
        # self.hond.render()
        # self.slang.render()
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
        self.slang.render()
        self.golden_poop.render()

    
game = Game()