from engine.pointers import pointers
from .fragment import Fragment
import pygame
from ..shatter import shatter_plate
import math
import random
import time
from engine import engine
from .angry_animation import render_angry_animation
from .plate_settings import PLATE_IMAGES, COLOR_PRICES, COLOR_ORDER, calculate_price_of_plate

def is_within_distance(pos1, pos2, dist: int) -> bool:
    # Manhattan distance
    if abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]) <= dist:
        # Euclidian
        return (pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2 <= dist**2

def is_combineable(attendance_1: list[bool], attendance_2: list[bool]) -> bool:
    def get_first_and_last_index(attendance):
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
        if not end_index:
            end_index = index
        return (start_index, end_index)

    # fragments are combineable iff they dont intersect AND there edges align (so no void)
    intersect = any([(attendance_1[i] and attendance_2[i]) for i in range(8)])
    start_1, end_1 = get_first_and_last_index(attendance_1)
    start_2, end_2 = get_first_and_last_index(attendance_2)
    edges_align = (end_1 - start_2 == 1) or (end_2 - start_1 == 1)
    return (not intersect) and edges_align

def create_split_lines(n: int, split_lines = None, start_index = 0, end_index = 7):
    """
    start_index: inclusive
    end_index: inclusive
    """
    if split_lines is None:
        split_lines = [False for _ in range(8)]
        # Create vertical split line
        split_lines[0] = True
        n = max(2, n)

    if n > 1:
        # apply new split
        split_index = round((start_index + end_index + 1)/2)
        split_lines[round((start_index + end_index + 1)/2)] = True
        n -= 1
        if n <= 1:
            pass
        else:
            # distribute splits over left and right
            left = random.randint(1, n)
            if left > 1:
                create_split_lines(left, split_lines, split_index, end_index)

            right = n - left
            if right > 1:
                create_split_lines(right, split_lines, start_index, split_index)
    return split_lines
    

class PlateSupervisor:
    ANGRY_ANIMATION_DURATION = 3

    def __init__(self, game, loading_bar, stats):
        self.trunk = engine.get_image("resources/images/trunk.png")

        self.loading_fragments = []
        self.plates = []
        self.held_plates = {}
   
        self.fragments = []
        self.held_fragment = None
        
        self.game = game
        self.loading_bar = loading_bar
        self.stats = stats

        self.time_until_next_spawn:float = None
        self.angry_animation_start_t: float = None

        self.is_frozen = True

        # wave settings
        self.falling_multiplier = 1
        self.average_pieces = 1 # will still cut in 2 pieces on average
        self.average_time_between_plates = 10
        self.color_index = 0 # which indices of COLOR_ORDER are unlocked

        # Spawn first frozen plates
        self.falling_multiplier = 0
        split_lines = [True, False, False, False, True, False, False, False]

        pieces = shatter_plate("resources/images/plate.png", split_lines)
        for position, piece in zip([(800, 300), (200, 50)], pieces):
            self.fragments.append(Fragment(
                *piece, # where this fragment exists (in the list of the entire plate)
                position=position,
                is_loading=False
            ))

    def spawn_plate(self):
        self.time_until_next_spawn = max(0, random.normalvariate(self.average_time_between_plates, 3))

        pieces_to_split = round(random.normalvariate(self.average_pieces, 1))
        split_lines = create_split_lines(n=pieces_to_split)

        # Choose color
        plate_settings = self.choose_random_plate()
        
        pieces = shatter_plate("resources/images/plates/"+plate_settings["image"], split_lines)
        for piece in pieces:
            fragment = Fragment(
                *piece, # where this fragment exists (in the list of the entire plate)
                fragment_colors=plate_settings["color"],
                fragment_symbols=plate_settings["symbol"],
                position=(random.randint(0, 1000),  -random.randint(200, 800)),
                is_loading=True
            )
            self.fragments.append(fragment)
    
    def unfreeze(self):
        self.is_frozen = False
        self.falling_multiplier = 1
        self.time_until_next_spawn = 1
        self.loading_bar.start_wave(self.game.wave_number)
    
    def apply_next_wave(self):
        # apply special
        if self.game.wave_number % 4 == 0:
            # More colors
            self.color_index += 1
        elif self.game.wave_number % 4 == 1:
            # Falling Faster
            self.falling_multiplier += 0.5
        elif self.game.wave_number % 4 == 2:
            # more pieces
            self.average_pieces += 1
        elif self.game.wave_number % 4 == 3:
            # More plates (more frequent)
            self.average_time_between_plates /= .25

        # go to next
        self.game.wave_number += 1
        self.loading_bar.start_wave(self.game.wave_number)
    
    def choose_random_plate(self) -> dict:
        color_index = random.randint(0, min(self.color_index, len(COLOR_ORDER)))
        return random.choice([setting for setting in PLATE_IMAGES if setting["color"] == COLOR_ORDER[color_index]])
    
    def update(self, delta_t: float, events: list):
        # preLoading fragments
        for fragment in self.loading_fragments:
            fragment.update()
            if fragment.get_center_pos()[1] < -100:
                # move to real fragment
                self.loading_fragments.remove(fragment)
                self.fragments.append(fragment)
                fragment.set_not_loading()
        
        # Update Fragments
        for fragment in self.fragments:
            fragment.previously_holding = fragment.holding
            fragment.previously_hovering = fragment.hovering

            intersecting_pointers = fragment.get_intersecting_pointers()
            if fragment.holding: 
                holding_pointer_ids = [pid for pid, p in self.held_plates.items() if p == fragment]
                still_holding = False
                for pointer_id in holding_pointer_ids:
                    if pointer_id in intersecting_pointers:
                        still_holding = True
                    else:
                        del self.held_plates[pointer_id]
                if not still_holding:
                    fragment.holding = False
                    fragment.holding_index = -1

            else:
                if intersecting_pointers != []:
                    for pointer_id in intersecting_pointers:
                        if pointer_id not in self.held_plates:
                            self.held_plates[pointer_id] = fragment
                            fragment.holding = True
                            fragment.holding_index = pointer_id
                            
            fragment.update(delta_t, events, self.falling_multiplier)
            
        # Check for spawning
        if self.time_until_next_spawn is not None and not self.time_until_next_spawn is None:
            self.time_until_next_spawn -= delta_t
            if self.time_until_next_spawn <= 0 and not self.loading_bar.wave_is_done():
                self.spawn_plate()

        self.hovered_plate = None


        if False: # self.held_fragment and pygame.mouse.get_pressed()[0]:
            # Complete plate, remove after 2 seconds
            self.held_fragment.holding = True
            self.held_fragment.update(delta_t, events, self.falling_multiplier)
            
            if fragment.finished_animation_start_time is not None:
                if time.time() - fragment.finished_animation_start_time > 2:
                    self.fragments.remove(fragment)
        else:
            # check if 'glueable'
            if self.held_fragment:
                for fragment in self.fragments:
                    if is_combineable(self.held_fragment.attendance_list, fragment.attendance_list):
                        if is_within_distance(self.held_fragment.get_center_pos(), fragment.get_center_pos(), 70):
                            self.held_fragment.combine_with(fragment)
                            self.fragments.remove(fragment)
                            engine.spawn_particles(self.held_fragment.get_center_pos(), count=100, color=(255,200,60), spread=2, speed=50, lifetime=2, radius=2)
                            # Test full plate
                            if all(self.held_fragment.attendance_list) and not self.held_fragment.is_playing_finished_animation:
                                # Success!
                                engine.spawn_particles(self.held_fragment.get_center_pos(), count=400, color=(255,200,60), spread=10, speed=500, lifetime=4, radius=4)
                                self.held_fragment.is_playing_finished_animation = True
                                if self.is_frozen: # was frozen
                                    self.unfreeze()
                                self.held_fragment.finished_animation_start_time = time.time()
                                if len(self.fragments) == 1 and not self.loading_bar.wave_is_done() and self.time_until_next_spawn is not None:
                                    self.spawn_plate()
                                # Give money
                                # self.stats.add_money(calculate_price_of_plate(self.held_fragment))

    def prerender(self):
        # render trunk
        if len(self.loading_fragments) > 0:
            ... # TODO
        # render fragments
        for fragment in self.loading_fragments:
            fragment.render()

    def render(self):
        for fragment in reversed(self.fragments):
            fragment.render()
