from engine import engine 
import pygame
import time

class Loadingbar:
    def __init__(self):
        self.wave_time_duration=20

        loading_bar_image_scalar=0.08
        self.loading_bar_image=engine.get_image('resources/images/loading_bar.png')
        self.loading_bar_image=pygame.transform.scale_by(self.loading_bar_image,loading_bar_image_scalar)
        self.width_loading_bar_image, self.length_loading_bar_image=self.loading_bar_image.get_size()

        falling_faster_image_scalar=0.28*loading_bar_image_scalar
        self.falling_faster_image=engine.get_image('resources/images/falling_faster.png')
        self.falling_faster_image=pygame.transform.scale_by(self.falling_faster_image,falling_faster_image_scalar)
        self.width_falling_faster_image, self.length_falling_faster_image=self.falling_faster_image.get_size()

        more_pieces_image_scalar=0.25*loading_bar_image_scalar
        self.more_pieces_image=engine.get_image('resources/images/more_broken_pieces.png')
        self.more_pieces_image=pygame.transform.scale_by(self.more_pieces_image,more_pieces_image_scalar)
        self.width_more_pieces_image, self.length_more_pieces_image=self.more_pieces_image.get_size()

        more_colors_image_scalar=0.28*loading_bar_image_scalar
        self.more_colors_image=engine.get_image('resources/images/more_colors.png')
        self.more_colors_image=pygame.transform.scale_by(self.more_colors_image,more_colors_image_scalar)
        self.width_more_colors_image, self.length_more_colors_image=self.more_colors_image.get_size()

        self.current_icon=None
        self.width_current_icon=None
        self.length_current_icon=None
        self.width_progression_bar=0
        self.length_progression_bar=0.6*self.length_loading_bar_image
        self.wave_started=False
        self.start_wave_time=0
        self.wave_level=0

        elephant_head_image_scalar=0.0012*self.length_progression_bar
        self.elephant_head_image=engine.get_image('resources/images/elephant_head.png')
        self.elephant_head_image=pygame.transform.scale_by(self.elephant_head_image,elephant_head_image_scalar)
        self.width_elephant_head_image, self.length_elephant_head_image=self.elephant_head_image.get_size()

    def start_wave(self,wave_level):
        self.wave_level=wave_level
        self.wave_started=True
        self.start_wave_time=time.time()
        if wave_level % 4 == 0:
            self.current_icon=self.more_colors_image
            self.width_current_icon,self.length_current_icon=self.width_more_colors_image, self.length_more_colors_image
        elif wave_level % 4 == 1:
            self.current_icon=self.falling_faster_image
            self.width_current_icon,self.length_current_icon=self.width_falling_faster_image, self.length_falling_faster_image
        elif wave_level % 4 == 2:
            self.current_icon=self.more_pieces_image
            self.width_current_icon,self.length_current_icon=self.width_more_pieces_image, self.length_more_pieces_image
        elif wave_level % 4 == 3:
            ...
        self.width_progression_bar=0   

    def wave_is_done(self) -> bool:
        return time.time()-self.start_wave_time > self.wave_time_duration
  
    def update(self, delta_t: float, events: list):
        if self.wave_started and self.width_progression_bar<0.76*self.width_loading_bar_image:
            self.width_progression_bar=self.width_loading_bar_image*((time.time()-self.start_wave_time)/self.wave_time_duration)
        
    def render(self):
        x_loading_bar_image=engine.DISPLAY_W/2-self.width_loading_bar_image/2
        y_loading_bar_image=30
        #engine.render_image(self.loading_bar_image,(x_loading_bar_image,y_loading_bar_image))

        if self.wave_started and self.current_icon is not None:
            x_rectangle=x_loading_bar_image+0.03*self.width_loading_bar_image
            y_rectangle=y_loading_bar_image+0.25*self.length_loading_bar_image
            pygame.draw.rect(engine._screen,(255,0,0),(x_rectangle,y_rectangle,self.width_progression_bar,self.length_progression_bar))

        engine.render_image(self.loading_bar_image,(x_loading_bar_image,y_loading_bar_image))

        if self.wave_started and self.current_icon is not None:
            x_current_icon=x_loading_bar_image+0.865*self.width_loading_bar_image
            y_current_icon=y_rectangle+0.5*self.length_progression_bar-0.53*self.length_current_icon
            engine.render_image(self.current_icon,(x_current_icon,y_current_icon))
            x_elephant_head=x_rectangle+self.width_progression_bar-0.55*self.width_elephant_head_image
            y_elephant_head=y_rectangle+0.5*self.length_progression_bar-0.35*self.length_elephant_head_image
            engine.render_image(self.elephant_head_image,(x_elephant_head,y_elephant_head))
