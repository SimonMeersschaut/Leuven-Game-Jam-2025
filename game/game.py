from engine import engine, Modes
import pygame
from .plate.fragment import Fragment
from .plate.plate_supervisor import PlateSupervisor
from .stats import Stats
from .loading_bar import Loadingbar
from .game_over_screen import Gameoverscreen

class Game:
    def __init__(self):
        self.wave_number = 0        
        self.repeating_cupboard=3
        self.cupboard_game_background=pygame.transform.scale(engine.get_image('resources/images/cupboard.png'),(engine.DISPLAY_W/self.repeating_cupboard,0.75*engine.DISPLAY_H))
        self.elephant_ass=engine.get_image("resources/images/elephant_ass.png")
        self.elephant_ass=pygame.transform.scale_by(self.elephant_ass,0.2)
        self.width_elephant_ass, self.length_elephant_ass=self.elephant_ass.get_size()
        self.stats = Stats()
        self.loading_bar = Loadingbar()
        self.gameoverscreen = Gameoverscreen(self)
        self.plate_supervisor = PlateSupervisor(self, self.loading_bar, self.stats)
    
    def play_again(self):
        self.wave_number = 0
        self.repeating_cupboard=3
        self.elephant_ass=pygame.transform.scale_by(self.elephant_ass,0.2)
        self.width_elephant_ass, self.length_elephant_ass=self.elephant_ass.get_size()
        self.stats.play_again()
        self.loading_bar = Loadingbar()
        self.gameoverscreen = Gameoverscreen(self)
        self.plate_supervisor = PlateSupervisor(self, self.loading_bar, self.stats)
    
    def back_to_main_menu(self):
        engine.mode = Modes.main_menu

    def update(self, delta_t: float, events: list):
        if self.stats.lives > 0:
            self.plate_supervisor.update(delta_t, events)
        
            self.stats.update(delta_t,events)
            self.loading_bar.update(delta_t,events)
        else:
            self.gameoverscreen.update(delta_t,events,self.stats,self.loading_bar)

    def render(self):
        engine.fill((0, 0, 0))
        self.plate_supervisor.prerender()
        for cupboard_nr in range(self.repeating_cupboard):
            engine.render_image(self.cupboard_game_background,(cupboard_nr*engine.DISPLAY_W/self.repeating_cupboard,0))
        engine.render_image(self.elephant_ass,(engine.DISPLAY_W/2-self.width_elephant_ass/2,engine.DISPLAY_H-self.length_elephant_ass-50))
        self.plate_supervisor.render()
        self.stats.render()
        self.loading_bar.render()
        if self.stats.lives <=0:
            self.gameoverscreen.render()

    
game = Game()