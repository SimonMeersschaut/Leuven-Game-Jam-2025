from engine import engine
from engine.draggable_sprite import DraggableSprite
import math
import random

def find_glue_side(attendance_1, attendance_2) -> tuple[bool, bool]:
    """
    Determine on which sides of attendance_1 glue must be applied relative to
    attendance_2. Both attendance lists represent presence at discrete radial
    indices around a circle. We consider a glue needed on the left side of a
    fragment when there exists a boundary where attendance_1 has a True cell
    whose previous index (counter-clockwise) is False in attendance_1 but True
    in attendance_2. Similarly for the right side using the next index
    (clockwise). This uses modulo indexing so the circular wrap-around is
    handled correctly.
    Returns (glue_left_for_1, glue_right_for_1).
    """
    n = len(attendance_1)
    if n == 0:
        return (False, False)

    glue_left = False
    glue_right = False

    for i in range(n):
        if not attendance_1[i]:
            continue

        prev_i = (i - 1) % n
        next_i = (i + 1) % n

        # left boundary: prev is empty on self but occupied on other
        if (not attendance_1[prev_i]) and attendance_2[prev_i]:
            glue_left = True

        # right boundary: next is empty on self but occupied on other
        if (not attendance_1[next_i]) and attendance_2[next_i]:
            glue_right = True

        # early exit if both found
        if glue_left and glue_right:
            break

    return (glue_left, glue_right)


class Fragment(DraggableSprite):
    def __init__(
            self,
            left_gold_glue,
            surface,
            right_gold_glue,
            attendance_list: list[bool],
            center_offset: tuple[int],
            angle_start,
            angle_stop,
            position: tuple[float, float],
            fragment_colors=None,
            fragment_symbols=None,
            height=None,
            width=None,
            is_loading = True
        ):
        assert fragment_colors is not None
        assert fragment_symbols is not None

        # self.exists = True # used to resolve the glitch of invisible plates

        self.ever_held = False
        self.fragment_colors = fragment_colors
        self.fragment_symbols = fragment_symbols
        self.left_gold_glue = left_gold_glue
        self.right_gold_glue = right_gold_glue
        self.attendance_list = attendance_list
        self.center_offset = center_offset
        self.angle_start = angle_start # radians
        self.angle_stop = angle_stop # radians
        self.radius = 500
        self.is_loading = is_loading
        self.is_playing_finished_animation = False
        self.finished_animation_start_time = None
        self.my_falling_speed = max(70, random.normalvariate(100, 40))
        super().__init__(surface, position, height, width)
        if self.is_loading:
            self.scale_factor(.25)

    def set_not_loading(self):
        if self.is_loading:
            self.scale_factor(4)
            self.is_loading = False
 
    def update(self, delta_t: float, events: list, falling_multiplier: float):
        if not self.is_playing_finished_animation:
            self.move(self.position[0], self.position[1] + delta_t*self.my_falling_speed*falling_multiplier)

            super().update()
    
    def get_center_pos(self):
        return (self.position[0] + self.center_offset[0], self.position[1] + self.center_offset[1])

    def render(self):
        super().render()
    
    def get_amount(self) -> float:
        return len([True for i in range(len(self.attendance_list)) if self.attendance_list[i]]) / len(self.attendance_list)
    
    def combine_with(self, fragment: object) -> None:
        self.ever_held = False
        glue_left_me, glue_right_me = find_glue_side(self.attendance_list, fragment.attendance_list)
        glue_left_other, glue_right_other = find_glue_side(fragment.attendance_list, self.attendance_list)
        # Note: we intentionally draw glue from both fragments so the seam
        # visually shows both sides. Do not suppress mirrored glue flags;
        # overlapping visuals are handled by the art (or can be adjusted
        # later if they look too intense).
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
        
        # Calculate symbols and colors
        self.fragment_colors = [
            self.fragment_colors[i] if self.attendance_list[i] else fragment.fragment_colors[i]
            for i in range(len(self.attendance_list))
        ]
        self.fragment_symbols = [
            self.fragment_symbols[i] if self.attendance_list[i] else fragment.fragment_symbols[i]
            for i in range(len(self.attendance_list))
        ]
        
        self.reset_scale()