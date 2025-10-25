from engine import engine 
import pygame


class Hond:
    def __init__(self):
        self.hond_image = engine.get_image('resources/images/test2.png')
        self.hond_image = pygame.transform.scale_by(self.hond_image,0.2)
        self.x=0
        self.y=0
        self.move_left=False
        self.move_right=False

    def update(self, delta_t: float, events: list):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.move_right=True
                if event.key == pygame.K_LEFT:
                    self.move_left=True

            if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.move_right=False
                    if event.key == pygame.K_LEFT:
                        self.move_left=False

        if self.move_right:
            self.x+=1
        if self.move_left:
            self.x-=1

    def render(self):        
        engine.render_image(self.hond_image,(self.x,self.y))

    
