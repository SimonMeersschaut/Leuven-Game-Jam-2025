from engine import engine 
import pygame

class Gameoverscreen:
    def __init__(self):
        self.prev_wave_level=0
        self.wave_level=0
        self.prev_money_amount=0
        self.money_amount=0
        self.plates_merged=0
        self.game_over_screen_line1_image=engine.render_text('birthstone',50,f'Wave level reached: {self.wave_level}',(255,255,255))
        self.game_over_screen_line2_image=engine.render_text('birthstone',50,f'Money collected: {self.money_amount}',(255,255,255))

    def update(self, delta_t: float, events: list,stats,loadingbar): #plate_merger
        self.wave_level=loadingbar.wave_level
        self.money_amount=stats.money
        #self.plates_merged=plate_merger.give_plates_merged()
        if self.prev_wave_level!=self.wave_level:
            self.game_over_screen_line1_image=engine.render_text('birthstone',50,f'Wave level reached: {self.wave_level}',(255,255,255))
            self.prev_wave_level=self.wave_level
        if self.prev_money_amount!=self.money_amount:
            self.game_over_screen_line2_image=engine.render_text('birthstone',50,f'Money collected: {self.money_amount}',(255,255,255))
            

    def render(self):
        engine.render_image(self.game_over_screen_line1_image,(200,200))
        engine.render_image(self.game_over_screen_line2_image,(200,300))

        
    
    