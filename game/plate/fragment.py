from engine import engine
from engine.draggable_sprite import DraggableSprite
import math
import random

def find_glue_side(attendance_1, attendance_2) -> tuple[bool, bool]:
    # Determine on which side(s) of attendance_1 glue must be applied
    # relative to attendance_2. Returns (glue_left_for_1, glue_right_for_1).
    def get_first_and_last_index(attendance: list[bool]):
        found = False
        start_index = None
        end_index = None
        for index in range(len(attendance)):
            if not found:
                if attendance[index]:
                    found = True
                    start_index = index
            else:
                if not attendance[index]:
                    end_index = index
                    break
        if start_index is None:
            return (None, None)
        if not end_index:
            # If we never found a False after the run, end_index is the last index
            end_index = index
        return (start_index, end_index)

    start_1, end_1 = get_first_and_last_index(attendance_1)
    start_2, end_2 = get_first_and_last_index(attendance_2)

    # If one of the fragments has no attendance, no glue is needed
    if start_1 is None or start_2 is None:
        return (False, False)

    # Normalize to indices modulo length (handles wrap-around)
    n = len(attendance_1)
    glue_left = False
    glue_right = False

    # If attendance_2's run ends exactly where attendance_1 starts, glue on left of 1
    if (end_2 % n) == (start_1 % n):
        glue_left = True

    # If attendance_2's run starts exactly where attendance_1 ends, glue on right of 1
    if (start_2 % n) == (end_1 % n):
        glue_right = True

    return (glue_left, glue_right)


class Fragment(DraggableSprite):
    def __init__(self, left_gold_glue, surface, right_gold_glue, attendance_list: list[bool], center_offset: tuple[int], angle_start, angle_stop, position, height=None, width=None):
        self.left_gold_glue = left_gold_glue
        self.right_gold_glue = right_gold_glue
        self.attendance_list = attendance_list
        self.center_offset = center_offset
        self.angle_start = angle_start # radians
        self.angle_stop = angle_stop # radians
        self.radius = 500
        self.is_playing_finished_animation = False
        self.finished_animation_start_time = None
        self.my_falling_speed = max(10, random.normalvariate(90, 40))
        super().__init__(surface, position, height, width)
    
    # def is_hovered(self):
    #     # First quick rectangle check to avoid expensive math when not necessary
    #     mouse_pos = engine.get_scaled_mouse_pos()
    #     if not self.rect.collidepoint(mouse_pos):
    #         return False

    #     # Detailed polar check relative to the fragment center
    #     cx, cy = self.get_center_pos()
    #     mx, my = mouse_pos
    #     dx = mx - cx
    #     dy = my - cy
    #     dist = math.hypot(dx, dy)
    #     if dist > self.radius:
    #         return False

    #     # Convert angles to [0, 2*pi) to make comparisons robust
    #     angle = math.atan2(dy, dx)
    #     two_pi = math.tau if hasattr(math, 'tau') else 2 * math.pi
    #     angle = angle % two_pi
    #     start = (self.angle_start) % two_pi
    #     stop = (self.angle_stop) % two_pi

    #     # handle wrap-around (e.g., start=5.2rad, stop=1.0rad)
    #     if start <= stop:
    #         inside = (start <= angle <= stop)
    #     else:
    #         inside = (angle >= start or angle <= stop)

    #     return inside
 
    def update(self, delta_t: float, events: list, falling_multiplier: float):
        if not self.is_playing_finished_animation:
            self.move(self.position[0], self.position[1] + delta_t*self.my_falling_speed*falling_multiplier)

            super().update()
    
    def get_center_pos(self):
        return (self.position[0] + self.center_offset[0], self.position[1] + self.center_offset[1])

    def render(self):
        super().render()
    
    def combine_with(self, fragment: object) -> None:
        glue_left_me, glue_right_me = find_glue_side(self.attendance_list, fragment.attendance_list)
        glue_left_other, glue_right_other = find_glue_side(fragment.attendance_list, self.attendance_list)
        self.attendance_list = [(self.attendance_list[i] or fragment.attendance_list[i]) for i in range(8)]
        # Combine images
        self.src_image.blit(fragment.src_image, (0, 0))
        if glue_left_me:
            self.src_image.blit(self.left_gold_glue, (0, 0))
        if glue_right_me:
            self.src_image.blit(self.right_gold_glue, (0, 0))
        if glue_left_other:
            self.src_image.blit(fragment.left_gold_glue, (0, 0))
        if glue_right_other:
            self.src_image.blit(fragment.right_gold_glue, (0, 0))
        
        self.reset_scale()