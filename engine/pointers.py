import pygame

class Pointers:
    def __init__(self):
        self.pointers = {}
        
    def handle_pointer_input(self, event, engine):
        if event.type == pygame.FINGERDOWN:
            self.add_pointer(event.finger_id, self.converted_relative_position((event.x, event.y)))
            
        elif event.type == pygame.FINGERUP:
            self.remove_pointer(event.finger_id)
            
        elif event.type == pygame.FINGERMOTION:
            self.pointers[event.finger_id] = self.converted_relative_position((event.x, event.y))
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:  # Left click
                self.add_pointer("__mouse__", engine.get_scaled_mouse_pos())
                print(engine.get_scaled_mouse_pos(), pygame.mouse.get_pos())
                print(engine.get_scaled_pointer_pos(pygame.mouse.get_pos()))
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.remove_pointer("__mouse__")
        
        elif event.type == pygame.MOUSEMOTION:
            if "__mouse__" in self.pointers:
                self.pointers["__mouse__"] = engine.get_scaled_mouse_pos()
        # print(self.pointers)
        
        
    def add_pointer(self, finger_id, position):
        self.pointers[finger_id] = position
        
    def remove_pointer(self, finger_id):
        self.pointers.pop(finger_id, None)
    
    def get_intersecting_pointers(self, rect):
        intersecting_pointers = []
        for pointer_id, pos in self.pointers.items():
            scaled_x = pos[0] * 1920
            scaled_y = pos[1] * 1080
            if rect.collidepoint((scaled_x, scaled_y)):
                intersecting_pointers.append(pointer_id)
        return intersecting_pointers
    
    def get_scaled_finger_position(self, finger_id, engine):
        if finger_id == "__mouse__":
            return engine.get_scaled_mouse_pos()
        pos = self.pointers.get(finger_id)
        return engine.get_scaled_pos(pos)

    def converted_relative_position(self, pos):
        scaled_x = pos[0] * 1920 // 1
        scaled_y = pos[1] * 1080 // 1
        return (scaled_x, scaled_y)

pointers = Pointers()