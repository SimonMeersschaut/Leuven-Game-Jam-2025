from engine import engine 
import pygame
import time

class Loading_bar:
    def __init__(self):
        self.loading_bar_image=engine.get_image('resources/images/loading_bar.jpg')
        self.loading_bar_image=pygame.transform.scale_by(self.loading_bar_image,0.2)
        self.width_loading_bar_image, self.length_loading_bar_image=self.loading_bar_image.get_size()

        self.falling_faster_image=engine.get_image('resources/images/falling_faster.jpg')
        self.falling_faster_image=pygame.transform.scale_by(self.falling_faster_image,0.2)
        self.width_falling_faster_image, self.length_falling_faster_image=self.falling_faster_image.get_size()

        self.more_pieces_image=engine.get_image('resources/images/more_broken_pieces.jpg')
        self.more_pieces_image=pygame.transform.scale_by(self.more_pieces_image,0.2)
        self.width_more_pieces_image, self.length_more_pieces_image=self.more_pieces_image.get_size()

        self.different_pieces_image=engine.get_image('resources/images/different_pieces.jpg')
        self.different_pieces_image=pygame.transform.scale_by(self.different_pieces_image,0.2)
        self.width_different_pieces_image, self.length_different_pieces_image=self.different_pieces_image.get_size()

        self.current_icon=None
        self.width_current_icon=None
        self.length_current_icon=None
        self.width_progression_bar=0
        self.wave_started=False
        self.start_wave_time=0
        

    def start_wave(self,level_wave):
        self.wave_started=True
        self.start_wave_time=time.time()
        if level_wave%3 == 1:
            self.current_icon=self.falling_faster_image
            self.width_current_icon,self.length_current_icon=self.width_falling_faster_image, self.length_falling_faster_image
        if level_wave%3 == 2:
            self.current_icon=self.more_pieces_image
            self.width_current_icon,self.length_current_icon=self.width_more_pieces_image, self.length_more_pieces_image
        if level_wave%3 == 0:
            self.current_icon=self.different_pieces_image
            self.width_current_icon,self.length_current_icon=self.width_different_pieces_image, self.length_different_pieces_image

        
        

    def update(self, delta_t: float, events: list):
        if self.wave_started and self.width_progression_bar<self.width_loading_bar_image:
            self.width_progression_bar=self.width_loading_bar_image*((time.time()-self.start_wave_time)/60)
        else:
            self.wave_started=False
        
    def render(self):
        x_loading_bar_image=engine.DISPLAY_W/2-self.width_loading_bar_image/2
        y_loading_bar_image=engine.DISPLAY_H-5*self.length_loading_bar_image
        engine.render_image(self.loading_bar_image,(x_loading_bar_image,y_loading_bar_image))
        x_rectangle=engine.DISPLAY_W/2-self.width_loading_bar_image/2
        y_rectangle=engine.DISPLAY_H-4.75*self.length_loading_bar_image
        pygame.draw.rect(engine._screen,(255,0,0),(x_rectangle,y_rectangle,self.width_progression_bar,self.length_loading_bar_image/2))
        
        x_current_icon=x_loading_bar_image+self.width_loading_bar_image
        y_current_icon=y_rectangle-self.length_falling_faster_image
        if self.wave_started and self.current_icon is not None:
            engine.render_image(self.current_icon,(x_current_icon,y_current_icon))