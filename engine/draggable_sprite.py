import resources
from engine import Engine, engine, Modes
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

    def update(self):
        # Holding logic is in plate_supervisor
        if self.holding:
            if not self.previously_holding:
                self.scale_factor(1.1)
            self.move(engine.get_scaled_mouse_pos()[0] - self.true_width*1.1 // 2, engine.get_scaled_mouse_pos()[1] - self.true_height*1.1 // 2)
        elif self.previously_holding:
            self.reset_scale()
            self.move(engine.get_scaled_mouse_pos()[0] - self.true_width // 2, engine.get_scaled_mouse_pos()[1] - self.true_height // 2)
            
            
            
    def render(self):
        if self.holding and not self.previously_holding:
            pygame.mouse.set_cursor(*pygame.cursors.diamond)
        elif not self.holding and self.hovering and (not self.previously_hovering or self.previously_holding):
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        elif not self.holding and not self.hovering and (self.previously_hovering or self.previously_holding):
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
        
        super().render()