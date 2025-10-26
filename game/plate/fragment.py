from engine import engine
from engine.draggable_sprite import DraggableSprite
import math
import random


class Fragment(DraggableSprite):
    def __init__(self, left_gold_glue, surface, right_gold_glue, attendance_list: list[bool], center_offset: tuple[int], angle_start, angle_stop, position, height=None, width=None):
        self.attendance_list = attendance_list
        self.center_offset = center_offset
        self.angle_start = angle_start # radians
        self.angle_stop = angle_stop # radians
        self.radius = 500
        self.is_playing_finished_animation = False
        self.finished_animation_start_time = None
        self.my_falling_speed = max(10, random.normalvariate(90, 40))
        super().__init__(surface, position, height, width)
    
    def is_hovered(self):
        # First quick rectangle check to avoid expensive math when not necessary
        mouse_pos = engine.get_scaled_mouse_pos()
        if not self.rect.collidepoint(mouse_pos):
            return False

        # Detailed polar check relative to the fragment center
        cx, cy = self.get_center_pos()
        mx, my = mouse_pos
        dx = mx - cx
        dy = my - cy
        dist = math.hypot(dx, dy)
        if dist > self.radius:
            return False

        # Convert angles to [0, 2*pi) to make comparisons robust
        angle = math.atan2(dy, dx)
        two_pi = math.tau if hasattr(math, 'tau') else 2 * math.pi
        angle = angle % two_pi
        start = (self.angle_start) % two_pi
        stop = (self.angle_stop) % two_pi

        # handle wrap-around (e.g., start=5.2rad, stop=1.0rad)
        if start <= stop:
            inside = (start <= angle <= stop)
        else:
            inside = (angle >= start or angle <= stop)

        return inside
 
    def update(self, delta_t: float, events: list, falling_multiplier: float):
        if not self.is_playing_finished_animation:
            self.move(self.position[0], self.position[1] + delta_t*self.my_falling_speed*falling_multiplier)

            super().update()
    
    def get_center_pos(self):
        return (self.position[0] + self.center_offset[0], self.position[1] + self.center_offset[1])

    def render(self):
        super().render()
    
    def combine_with(self, fragment: object) -> None:
        self.attendance_list = [(self.attendance_list[i] or fragment.attendance_list[i]) for i in range(8)]
        # Combine images
        self.src_image.blit(fragment.src_image, (0, 0))
        self.reset_scale()