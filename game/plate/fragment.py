from engine.draggable_sprite import DraggableSprite
import time


class Fragment(DraggableSprite):
    def __init__(self, left_gold_glue, surface, right_gold_glue, attendance_list: list[bool], center_offset: tuple[int], angle_start, angle_stop, position, height=None, width=None):
        self.attendance_list = attendance_list
        self.center_offset = center_offset
        self.angle_start = angle_start
        self.angle_stop = angle_stop
        self.is_playing_finished_animation = False
        self.finished_animation_start_time = None
        super().__init__(surface, position, height, width)
 
    def update(self, delta_t: float, events: list, falling_multiplier: float):
        if not self.is_playing_finished_animation:
            self.move(self.position[0], self.position[1] + delta_t*50*falling_multiplier)

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