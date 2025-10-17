from engine import Engine, engine, Modes
import pygame

class Button:
    def __init__(self, image_path, position, height=None):
        self.position = position
                
        if height:
            image = engine.get_image(image_path)
            scale_factor = height / image.get_height()
            self.image = pygame.transform.scale(image, (int(image.get_width() * scale_factor), height))
        else:
            self.image = engine.get_image(image_path)

        self.rect = self.image.get_rect(topleft=position)

    def render(self):
        engine.render_image(self.image, self.position)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())  # check if mouse is over the button
    
    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed()[0]  # left mouse button