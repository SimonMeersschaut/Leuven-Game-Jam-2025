import pygame

class Pointers:
    def __init__(self):
        self.pointers = {}
        
    def handle_pointer_input(self, event):
        if event.type == pygame.FINGERDOWN:
            self.add_pointer(event.finger_id, (event.x, event.y))
            
        elif event.type == pygame.FINGERUP:
            self.remove_pointer(event.finger_id)
            
        elif event.type == pygame.FINGERMOTION:
            self.pointers[event.finger_id] = (event.x, event.y)

    def add_pointer(self, finger_id, position):
        self.pointers[finger_id] = position
        
    def remove_pointer(self, finger_id):
        self.pointers.pop(finger_id, None)
    
    def get_intersecting_pointers(self, rect):
        intersecting_pointers = []
        for pointer_id, (pos) in self.pointers.items():
            scaled_x = pos[0] * 1920
            scaled_y = pos[1] * 1080
            if rect.collidepoint((scaled_x, scaled_y)):
                intersecting_pointers.append(pointer_id)
        return intersecting_pointers