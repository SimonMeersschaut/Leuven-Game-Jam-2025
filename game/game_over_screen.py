from engine import engine 
from engine.sprite import Button, Sprite
import pygame

class Gameoverscreen:
    def __init__(self, game):
        self.game = game
        self.prev_wave_level=0
        self.wave_level=0
        self.prev_money_amount=0
        self.money_amount=0
        self.prev_plates_merged=0
        self.plates_merged=0
        self.game_over_screen_image=engine.get_image('resources/images/game_over_screen.jpg')
        self.game_over_screen_image=pygame.transform.scale_by(self.game_over_screen_image,0.12)
        self.width_game_over_screen_image, self.length_game_over_screen_image=self.game_over_screen_image.get_size()
        
        self.game_over_screen_line2_image=engine.render_text('birthstone',30,f'{self.wave_level}',(0,0,0))
        self.game_over_screen_line3_image=engine.render_text('birthstone',30,f'€{self.money_amount}',(0,0,0))
        self.game_over_screen_line1_image=engine.render_text('birthstone',30,f'{self.plates_merged}',(0,0,0))

        self.x_game_over_screen=engine.DISPLAY_W/2-self.width_game_over_screen_image/2

        self.y_game_over_screen=85
        self.back_to_menu_button=Button('resources/buttons/main_menu.png',(self.x_game_over_screen + 0.5*self.width_game_over_screen_image,self.y_game_over_screen+ 0.85*self.length_game_over_screen_image),height=50,align_x='center')
        
        self.play_again_button=Button('resources/buttons/play_again.png',(self.x_game_over_screen + 0.5*self.width_game_over_screen_image,self.y_game_over_screen+ 0.75*self.length_game_over_screen_image),height=50,align_x='center')

    def update(self, delta_t: float, events: list,stats,loadingbar): #plate_merger
        if self.play_again_button.just_unclicked():
            self.game.play_again()
        elif self.back_to_menu_button.just_unclicked():
            self.game.back_to_main_menu()
        
        self.wave_level=loadingbar.wave_level
        self.money_amount=stats.money
        self.plates_merged=stats.plates_merged
        #self.plates_merged=plate_merger.give_plates_merged()
        if self.prev_wave_level!=self.wave_level:
            self.game_over_screen_line2_image=engine.render_text('birthstone',30,f'{self.wave_level}',(0,0,0))
            self.prev_wave_level=self.wave_level
        if self.prev_money_amount!=self.money_amount:
            self.game_over_screen_line3_image=engine.render_text('birthstone',30,f'€{self.money_amount}',(0,0,0))
        if self.prev_plates_merged!=self.plates_merged:
            self.game_over_screen_line1_image=engine.render_text('birthstone',30,f'{self.plates_merged}',(0,0,0))

        self.back_to_menu_button.update()
        self.play_again_button.update()
        
            

    def render(self):
       
        engine.render_image(self.game_over_screen_image,(self.x_game_over_screen,self.y_game_over_screen))
        x_line2=self.x_game_over_screen+0.66*self.width_game_over_screen_image
        y_line2=self.y_game_over_screen+0.36*self.length_game_over_screen_image
        engine.render_image(self.game_over_screen_line2_image,(x_line2,y_line2))
        x_line3=self.x_game_over_screen+0.56*self.width_game_over_screen_image
        y_line3=self.y_game_over_screen+0.425*self.length_game_over_screen_image
        engine.render_image(self.game_over_screen_line3_image,(x_line3,y_line3))
        x_line1=self.x_game_over_screen+0.6*self.width_game_over_screen_image
        y_line1=self.y_game_over_screen+0.32*self.length_game_over_screen_image
        engine.render_image(self.game_over_screen_line1_image,(x_line1,y_line1))
        # Robbe, use stats.total_money!
        self.back_to_menu_button.render()
        self.play_again_button.render()
        