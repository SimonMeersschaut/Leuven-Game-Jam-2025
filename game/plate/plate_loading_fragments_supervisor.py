import math
from engine import engine
from engine.sprite import Sprite
import pygame

class PlateLoadingFragmentSupervisor():
    def __init__(self):
        self.trunk_image = pygame.transform.scale(pygame.image.load("resources/images/trunk.png").convert_alpha(), (94, 300))
        self.trunk = Sprite("resources/images/trunk.png", position=(-1, 0), align_x="center", height=300)

        self.origin = (640, 360)
        self.loading_fragments = []
        
        self.aim_trunk((0, 0))
        
        self.temp = 1
    
    def update(self):
        self.trunk.image = pygame.transform.rotate(self.trunk_image, self.temp)
        print(self.temp)
        self.temp += 1
    
    def render(self):
        self.trunk.render()
        
        # for fragment in self.loading_fragments:
        #     fragment.update()
        #     if fragment.get_center_pos()[1] < -100:
        #         # move to real fragment
        #         self.loading_fragments.remove(fragment)
        #         self.fragments.append(fragment)
        #         fragment.set_not_loading()
            
    def aim_trunk(self, position):
        theta = math.atan((position[1]-self.origin[1])/(position[0]-self.origin[0]))
        self.trunk.image = pygame.transform.rotate(self.trunk.image, -math.degrees(theta)-180)

    def prerender(self):
        # render trunk
        if len(self.loading_fragments) > 0:
            ... # TODO
        # render fragments
        for fragment in self.loading_fragments:
            fragment.render()
            
loading_supervisor = PlateLoadingFragmentSupervisor()