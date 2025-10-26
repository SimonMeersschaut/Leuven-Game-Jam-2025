from engine import engine 
import pygame
import random

class Stats:
    def __init__(self, multiplier):
        self.lives_image = engine.get_image('resources/images/life.png')
        self.lives_image = pygame.transform.scale_by(self.lives_image,0.02)
        self.width_lives_image, self.length_lives_image=self.lives_image.get_size()

        self.lost_lives_image=engine.get_image('resources/images/lost_life.png')
        self.lost_lives_image=pygame.transform.scale_by(self.lost_lives_image,0.02)
        self.width_lost_lives_image, self.length_lost_lives_image=self.lost_lives_image.get_size()

        self.money=10000000
        self.multiplier=multiplier
        self.money_image=engine.render_text('birthstone',60,f'€{self.money}',(255,255,255))
        self.width_money_image,self.length_money_image=self.money_image.get_size()

        self.lives=5
        self.plates_merged = 12 # temp.

    def lose_life(self):
        if self.lives>0:
            self.lives-=1
    
    def update_money(self,amount):
        self.money+=amount*self.multiplier
        self.money_image=engine.render_text('birthstone',60,f'€{self.money}',(255,255,255))
        self.width_money_image,self.length_money_image=self.money_image.get_size()
    
    def update(self, delta_t: float, events: list):
        self.money_image=engine.render_text('birthstone',60,f'€{self.money}',(255,255,255))

    def render(self):
        for live in range(self.lives):
            engine.render_image(self.lives_image,(50+1.5*live*self.width_lives_image,50))

        for lost_live in range(5-self.lives):
            engine.render_image(self.lost_lives_image,(50+1.5*(self.lives*self.width_lives_image)+self.width_lost_lives_image*lost_live*1.5,50))

        engine.render_image(self.money_image,(engine.DISPLAY_W-self.width_money_image-30,30))
