from .fragment import Fragment
import pygame
from ..shatter import shatter_plate
import random

class PlateSupervisor:
    def __init__(self):
        self.fragments = []
        self.held_plate = None


    def create_plate_pieces(self, image_path="resources/images/plate.png", position=(100, 100), height=None, width=None):
        split_lines = [random.getrandbits(1) for _ in range(8)]
        pieces = shatter_plate("resources/images/plate.png", split_lines)
        plates = []
        for (left_gold_glue, piece_image, right_gold_glue) in pieces:
            self.fragments.append(Fragment(
                left_gold_glue,
                piece_image,
                right_gold_glue,
            ))
        return plates
    
    def update(self):
        self.hovered_plate = None

        if self.held_plate and pygame.mouse.get_pressed()[0]:
            self.held_plate.holding = True
            self.held_plate.update()
        else:
            self.held_plate = None
        
            for fragment in self.fragments:
                fragment.previously_holding = fragment.holding
                fragment.previously_hovering = fragment.hovering

                if fragment.is_clicked() and self.held_plate is None:
                    fragment.holding = True
                    self.held_plate = fragment
                elif not self.held_plate == fragment:
                    fragment.holding = False

                if fragment.is_hovered() and self.hovered_plate is None:
                    fragment.hovering = True
                    self.hovered_plate = fragment
                else:
                    fragment.hovering = False

                fragment.update()

    def render(self):
        for plate in reversed(self.fragments):
            plate.render()
