from .fragment import Fragment
import pygame
from ..shatter import shatter_plate
import random

class PlateSupervisor:
    def __init__(self):
        self.plates = []
        self.held_plate = None


    def create_plate_pieces(self, image_path="resources/images/plate.png", position=(100, 100), height=None, width=None):
        split_lines = [random.getrandbits(1) for _ in range(8)]
        pieces = shatter_plate("resources/images/plate.png", split_lines)
        plates = []
        for (left_gold_glue, piece_image, right_gold_glue) in pieces:
            self.plates.append(Fragment(
                left_gold_glue,
                piece_image,
                right_gold_glue,
            ))
        return plates
    
    def update(self):
        self.hovered_plate = None
        
        if self.held_plate is not None and pygame.mouse.get_pressed()[0]:
            self.held_plate.holding = True
        else:
            self.held_plate = None

        for plate in self.plates:
            plate.previously_holding = plate.holding
            plate.previously_hovering = plate.hovering

            if plate.is_clicked() and self.held_plate is None:
                plate.holding = True
                self.held_plate = plate
            elif not self.held_plate == plate:
                plate.holding = False

            if plate.is_hovered() and self.hovered_plate is None:
                plate.hovering = True
                self.hovered_plate = plate
            else:
                plate.hovering = False

            plate.update()

    def render(self):
        for plate in reversed(self.plates):
            plate.render()
