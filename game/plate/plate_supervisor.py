from .fragment import Fragment
import pygame
from ..shatter import shatter_plate
import random

def is_within_distance(pos1, pos2, dist: int) -> bool:
    # Manhattan distance
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) <= dist

def is_combineable(attendance_1: list[bool], attendance_2: list[bool]) -> bool:
    # fragments are combineable iff they dont intersect AND there edges align (so no void)
    intersect = any([(attendance_1[i] and attendance_2[i]) for i in range(8)])
    edges_align = True
    return (not intersect) and edges_align

class PlateSupervisor:
    def __init__(self):
        self.fragments = []
        self.held_fragment = None

    def create_plate_pieces(self, image_path="resources/images/plate.png", position=(100, 100), height=None, width=None):
        split_lines = [random.getrandbits(1) for _ in range(8)]
        pieces = shatter_plate("resources/images/plate.png", split_lines)
        plates = []
        for (left_gold_glue, piece_image, right_gold_glue, attendance_list) in pieces:
            self.fragments.append(Fragment(
                left_gold_glue,
                piece_image,
                right_gold_glue,
                attendance_list # where this fragment exists (in the list of the entire plate)
            ))
        return plates
    
    def update(self):
        self.hovered_plate = None

        if self.held_fragment and pygame.mouse.get_pressed()[0]:
            self.held_fragment.holding = True
            self.held_fragment.update()
            # check if 'glueable'
            for fragment in self.fragments:
                if is_combineable(self.held_fragment.attendance_list, fragment.attendance_list):
                    if is_within_distance(self.held_fragment.position, fragment.position, 50):
                        self.held_fragment.combine_with(fragment)
                        self.fragments.remove(fragment)
                        # Test full plate
                        if all(self.held_fragment.attendance_list):
                            print("Full plate")
        else:
            self.held_fragment = None
        
            for fragment in self.fragments:
                fragment.previously_holding = fragment.holding
                fragment.previously_hovering = fragment.hovering

                if fragment.is_clicked() and self.held_fragment is None:
                    fragment.holding = True
                    self.held_fragment = fragment
                elif not self.held_fragment == fragment:
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
