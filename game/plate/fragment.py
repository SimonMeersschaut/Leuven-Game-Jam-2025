from engine.draggable_sprite import DraggableSprite


class Fragment(DraggableSprite):
    def __init__(self, left_gold_glue, surface, right_gold_glue, attendance_list: list[bool], position=(100, 100), height=None, width=None):
        self.attendance_list = attendance_list
        super().__init__(surface, position, height, width)
 
    def update(self):
        super().update()

    def render(self):
        super().render()
    
    def combine_with(self, fragment: object) -> None:
        self.attendance_list = [(self.attendance_list[i] or fragment.attendance_list[i]) for i in range(8)]
        # Combine images
        self.src_image.blit(fragment.src_image, (0, 0))
        self.reset_scale()