import pygame

class Pointers:
    def __init__(self):
        self.all_pointers = {}
        
    def handle_pointer_input(self, event, engine):
        if event.type == pygame.FINGERDOWN:
            self.add_pointer(event.finger_id, self.converted_relative_position((event.x, event.y)))
            
        elif event.type == pygame.FINGERUP:
            self.remove_pointer(event.finger_id)
            
        elif event.type == pygame.FINGERMOTION:
            self.all_pointers[event.finger_id] = self.converted_relative_position((event.x, event.y))
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if event.button == 1:  # Left click
                self.add_pointer("__mouse__", engine.scale_position(pygame.mouse.get_pos()))
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left click
                self.remove_pointer("__mouse__")
        
        elif event.type == pygame.MOUSEMOTION:
            if "__mouse__" in self.all_pointers:
                self.all_pointers["__mouse__"] = engine.scale_position(pygame.mouse.get_pos())        
        
    def add_pointer(self, finger_id, position):
        self.all_pointers[finger_id] = position
        
    def remove_pointer(self, finger_id):
        self.all_pointers.pop(finger_id, None)
    
    def get_intersecting_pointers(self, rect):
        output = []
        
        for pointer in self.all_pointers:
            if self.all_pointers[pointer][0] in range(rect[0], rect[0]+rect[2])  and self.all_pointers[pointer][1] in range(rect[1], rect[1]+rect[3]):
                output.append(pointer)
        
        return output

    def get_scaled_finger_position(self, finger_id, engine):
        if finger_id == "__mouse__":
            return engine.get_scaled_mouse_pos()
        pos = self.all_pointers.get(finger_id)
        return engine.get_scaled_pos(pos)

    def converted_relative_position(self, pos):
        scaled_x = pos[0] * 1920 // 1
        scaled_y = pos[1] * 1080 // 1
        return (scaled_x, scaled_y)

pointers = Pointers()