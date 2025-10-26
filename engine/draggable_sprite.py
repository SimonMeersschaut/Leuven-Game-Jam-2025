import resources
from engine import Engine, engine, Modes
from engine.pointers import pointers
from engine.sprite import Sprite
import pygame

class DraggableSprite(Sprite):
    def __init__(self, image_path, position=(100, 100), height=None, width=None):
        super().__init__(image_path, position, height, width)
        
        self.holding = False
        self.holding_index = -1
        self.hovering = False
        self.previously_holding = False
        self.previously_hovering = False
        self.dragging_offset = (0, 0)
        
    def update(self):
        # Holding logic is in plate_supervisor
        if self.holding and self.holding_index != -1:
            if not self.previously_holding:
                self.scale_factor(1.1)
                self.dragging_offset = (pointers.all_pointers[self.holding_index][0] - self.position[0],
                                        pointers.all_pointers[self.holding_index][1] - self.position[1])
            self.move(pointers.all_pointers[self.holding_index][0] - self.dragging_offset[0], pointers.all_pointers[self.holding_index][1] - self.dragging_offset[1])
        elif self.previously_holding and self.holding_index != -1:
            self.reset_scale()
            
    def render(self):
        if self.holding and not self.previously_holding:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        elif not self.holding and self.hovering and (not self.previously_hovering or self.previously_holding):
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        elif not self.holding and not self.hovering and (self.previously_hovering or self.previously_holding):
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
        super().render()