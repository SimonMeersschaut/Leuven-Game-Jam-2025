from .fragment import Fragment
import pygame
from ..shatter import shatter_plate
import math
import random
import time
from engine import engine
from .angry_animation import render_angry_animation

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
    ANGRY_ANIMATION_DURATION = 1
    def __init__(self, game, loading_bar, stats):
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

        # Spawn first frozen plates
        self.falling_multiplier = 0
        split_lines = [True, False, False, False, True, False, False, False]

        pieces = shatter_plate("resources/images/plate.png", split_lines)
        plates = []
        for position, piece in zip([(800, 300), (200, 50)], pieces):
            self.fragments.append(Fragment(
                *piece, # where this fragment exists (in the list of the entire plate)
                position=position
            ))

    def spawn_plate(self):
        self.time_until_next_spawn = max(0, random.normalvariate(self.average_time_between_plates, 3))

        pieces_to_split = round(random.normalvariate(self.average_pieces, 1))
        split_lines = create_split_lines(n=pieces_to_split)

        pieces = shatter_plate("resources/images/plate.png", split_lines)
        plates = []
        for piece in pieces:
            self.fragments.append(Fragment(
                *piece, # where this fragment exists (in the list of the entire plate)
                position=(random.randint(0, 1000),  -random.randint(400, 800))
            ))
    
    def unfreeze(self):
        self.is_frozen = False
        self.falling_multiplier = 1
        self.time_until_next_spawn = 1
        self.loading_bar.start_wave(self.game.wave_number)
    
    def apply_next_wave(self):
        # apply special
        if self.game.wave_number % 4 == 0:
            # More colors
            ...
        elif self.game.wave_number % 4 == 1:
            # Falling Faster
            self.falling_multiplier += 0.25
        elif self.game.wave_number % 4 == 2:
            # more pieces
            self.average_pieces += 1
        elif self.game.wave_number % 4 == 3:
            # More plates (more frequent)
            self.average_time_between_plates /= .25

        # go to next
        self.game.wave_number += 1
        self.loading_bar.start_wave(self.game.wave_number)
    
    def update(self, delta_t: float, events: list):
        # Update Fragments
        for fragment in self.fragments:
            fragment.update(delta_t, events, self.falling_multiplier)

        if self.loading_bar.wave_is_done():
            # wait for all fragments to dissappear
            if len(self.fragments) == 0:
                # Show angry animation, then go to next wave
                if self.angry_animation_start_t is not None:
                    # animation is playing
                    render_angry_animation(self.game.wave_number, (time.time() - self.angry_animation_start_t) / PlateSupervisor.ANGRY_ANIMATION_DURATION)
                    if time.time() - self.angry_animation_start_t >= PlateSupervisor.ANGRY_ANIMATION_DURATION:
                        # go to next wave
                        self.apply_next_wave()
                else:
                    self.angry_animation_start_t = time.time()
            
        # Check for spawning
        if self.time_until_next_spawn is not None and not self.time_until_next_spawn is None:
            self.time_until_next_spawn -= delta_t
            if self.time_until_next_spawn <= 0 and not self.loading_bar.wave_is_done():
                self.spawn_plate()

        self.hovered_plate = None

        if self.held_fragment and pygame.mouse.get_pressed()[0]:
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

                if fragment.finished_animation_start_time is not None:
                    if time.time() - fragment.finished_animation_start_time > 2:
                        self.fragments.remove(fragment)
                
                if fragment.get_center_pos()[1] >= 600:
                    # break on ground
                    # spawn an upward splash of particles to emphasise the breaking
                    engine.spawn_particles(fragment.get_center_pos(), count=50, color=(220, 220, 220), spread=30, speed=200, lifetime=1.2, radius=5, angle_min=-math.pi, angle_max=-math.tau)
                    self.fragments.remove(fragment)
                    self.stats.lose_life()

    def render(self):
        for plate in reversed(self.fragments):
            plate.render()
