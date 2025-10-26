from engine import engine
from engine.sprite import Sprite
import pygame

class PlateLoadingFragmentSupervisor():
    def __init__(self):
        self.trunk = Sprite("resources/images/trunk.png", position=(-1, 0), align_x="center", height=300)

        self.loading_fragments = []
        self.aim_trunk((0, 0))
        self.origin = ()
    def update(self):
        pass
    
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
        pygame.transform.rotate(self.trunk.image, -20)

    def prerender(self):
        # render trunk
        if len(self.loading_fragments) > 0:
            ... # TODO
        # render fragments
        for fragment in self.loading_fragments:
            fragment.render()