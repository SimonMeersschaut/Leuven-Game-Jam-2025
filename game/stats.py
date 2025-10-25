from engine import engine 
import pygame

class Stats:
    def __init__(self):
        self.lives_image = engine.get_image('resources/images/lives_tijdelijk.png')
        self.lives_image = pygame.transform.scale_by(self.lives_image,0.1)
        self.width_lives_image=self.lives_image.get_size()[0]
        self.length_lives_image=self.lives_image.get_size()[1]
        self.lost_lives_image=engine.get_image('resources/images/broken_heart_emoticon.jpeg')
        self.lost_lives_image=pygame.transform.scale_by(self.lost_lives_image,0.1)
        self.width_lost_lives_image=self.lost_lives_image.get_size()[0]
        self.length_lost_lives_image=self.lost_lives_image.get_size()[0]
        self.lives=2
        self.money=0
        self.money_image=engine.render_text('pixel',80,f'€{self.money}',(0,255,0))
        self.width_money_image=self.money_image.get_size()[0]
    
    def lose_life(self):
        if self.lives>0:
            self.lives-=1
    
    def update_money(self,amount):
        self.money+=amount
        self.money_image=engine.render_text('pixel',60,f'€{self.money}',(0,255,0))


    
    def update(self, delta_t: float, events: list):
        ...
    
    def render(self):
        for live in range(self.lives):
            engine.render_image(self.lives_image,(50+1.5*live*self.width_lives_image,50))

        for lost_live in range(5-self.lives):
            engine.render_image(self.lost_lives_image,(50+1.5*(self.lives*self.width_lives_image)+self.width_lost_lives_image*lost_live*1.5,50))

        engine.render_image(self.money_image,(engine.DISPLAY_W-self.width_money_image*1.5,30))