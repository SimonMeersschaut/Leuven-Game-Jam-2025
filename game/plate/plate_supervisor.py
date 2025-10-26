from .fragment import Fragment
import pygame
from ..shatter import shatter_plate
import random
import time
from engine import engine

def is_within_distance(pos1, pos2, dist: int) -> bool:
    # Manhattan distance
    if abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) <= dist:
        # Euclidian
        return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 <= dist**2

def is_combineable(attendance_1: list[bool], attendance_2: list[bool]) -> bool:
    # fragments are combineable iff they dont intersect AND there edges align (so no void)
    intersect = any([(attendance_1[i] and attendance_2[i]) for i in range(8)])
    edges_align = True
    return (not intersect) and edges_align

class PlateSupervisor:
    def __init__(self, loading_bar):
        self.fragments = []
        self.held_fragment = None
        self.loading_bar = loading_bar

        self.time_until_next_spawn = 1

        # wave settings
        self.falling_multiplier = 1
        self.average_split = 1
        self.average_time_between_plates = 20

    def spawn_plate(self):
        self.time_until_next_spawn = max(0, random.normalvariate(self.average_time_between_plates, 5))

        # split_lines = [random.getrandbits(1) for _ in range(8)]
        split_lines = [True, False, False, False, True, False, False, False]
        # split_lines[0] = 1
        pieces = shatter_plate("resources/images/plate.png", split_lines)
        plates = []
        for piece in pieces:
            self.fragments.append(Fragment(
                *piece, # where this fragment exists (in the list of the entire plate)
                position=(random.randint(0, 1000), -400)
            ))
        return plates
    
    def update(self, delta_t: float, events: list):
        # Check for spawning
        self.time_until_next_spawn -= delta_t
        if self.time_until_next_spawn <= 0:
            self.spawn_plate()

        # Update Fragments
        self.hovered_plate = None

        if self.held_fragment and pygame.mouse.get_pressed()[0]:
            self.held_fragment.holding = True
            self.held_fragment.update(delta_t, events, self.falling_multiplier)
            # check if 'glueable'
            for fragment in self.fragments:
                fragment.update(delta_t, events, self.falling_multiplier)
                if is_combineable(self.held_fragment.attendance_list, fragment.attendance_list):
                    if is_within_distance(self.held_fragment.get_center_pos(), fragment.get_center_pos(), 70):
                        self.held_fragment.combine_with(fragment)
                        self.fragments.remove(fragment)
                        # Test full plate
                        if all(self.held_fragment.attendance_list) and not self.held_fragment.is_playing_finished_animation:
                            engine.spawn_particles(self.held_fragment.get_center_pos(), count=200, color=(255,200,60), spread=160, speed=200, lifetime=2, radius=2)
                            self.held_fragment.is_playing_finished_animation = True
                            self.held_fragment.finished_animation_start_time = time.time()
                if fragment.finished_animation_start_time is not None:
                    if time.time() - fragment.finished_animation_start_time > 2:
                        self.fragments.remove(fragment)
                        if len(self.fragments) == 0:
                            self.spawn_plate()
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

                fragment.update(delta_t, events, self.falling_multiplier)
                if fragment.finished_animation_start_time is not None:
                    if time.time() - fragment.finished_animation_start_time > 2:
                        self.fragments.remove(fragment)

    def render(self):
        for plate in reversed(self.fragments):
            plate.render()
