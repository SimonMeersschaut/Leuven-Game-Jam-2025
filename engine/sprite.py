from engine import Engine, engine, Modes
import pygame

class Sprite():
    """
    A class representing a sprite.
    """
    def __init__(self, image_path, position=(0, 0), height=None, width=None, align_x=None, align_y=None):
        """
        Give either height or width to scale the image proportionally, or both to stretch to exact size
        center_x and center_y will override position and center the sprite
        
        align options: center, left, right for x
        and center, top, bottom for y
        """ 
        image = engine.get_image(image_path)
        if height and width:
            pass
        elif height:
            width = int(image.get_width() * (height / image.get_height()))
        elif width:
            height = int(image.get_height() * (width / image.get_width()))
        else:
            height = image.get_height()
            width = image.get_width()
        
        self.image = pygame.transform.scale(image, (width, height))   

        if align_x:
            if align_x == "left":
                position = (0, position[1])
            elif align_x == "center":
                position = (500 - (width // 2), position[1])
            elif align_x == "right":
                position = (1000 - width, position[1])

        if align_y:
            if align_y == "top":
                position = (position[0], 0)
            elif align_y == "center":
                position = (position[0], 300 - (height // 2))
            elif align_y == "bottom":
                position = (position[0], 600 - height)
        
            
        self.position = position

        self.rect = self.image.get_rect(topleft=position)


    def render(self):
        """Renders the sprite on the screen at its position."""
        engine.render_image(self.image, self.position)

    def is_hovered(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())  # check if mouse is over the button
    
    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed()[0]  # left mouse button

class Button(Sprite):
    def __init__(self, image_path, position=(0, 0), height=None, width=None, align_x=None, align_y=None):
        super().__init__(image_path, position, height, width, align_x, align_y)