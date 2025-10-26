from engine.pointers import pointers
from .fragment import Fragment
import pygame

class PlateSupervisor:
    def __init__(self):
        self.plates = []
        self.held_plates = {}


    def create_plate(self, image_path="resources/images/plate.png", position=(100, 100), height=None, width=None):
        plate = Fragment(image_path, position, height, width)
        self.plates.append(plate)
        return plate
    
    def update(self):
        self.hovered_plate = None
        
        for plate in self.plates:
            plate.previously_holding = plate.holding
            plate.previously_hovering = plate.hovering

            intersecting_pointers = plate.get_intersecting_pointers()
            if plate.holding: 
                holding_pointer_ids = [pid for pid, p in self.held_plates.items() if p == plate]
                print(holding_pointer_ids)
                still_holding = False
                for pointer_id in holding_pointer_ids:
                    if pointer_id in intersecting_pointers:
                        still_holding = True
                    else:
                        del self.held_plates[pointer_id]
                if not still_holding:
                    plate.holding = False
                    plate.holding_index = -1
                
            else:
                if intersecting_pointers != []:
                    for pointer_id in intersecting_pointers:
                        if pointer_id not in self.held_plates:
                            self.held_plates[pointer_id] = plate
                            plate.holding = True
                            plate.holding_index = pointer_id


            if plate.is_hovered() and self.hovered_plate is None:
                plate.hovering = True
                self.hovered_plate = plate
            else:
                plate.hovering = False

            plate.update()

    def render(self):
        for plate in reversed(self.plates):
            plate.render()
