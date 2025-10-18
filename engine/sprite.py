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
        self.image_path = image_path
        
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

        self.true_width = width
        self.true_height = height

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
        self.true_position = position

        self.rect = self.image.get_rect(topleft=position)

    def move(self, x, y):
        """Moves the sprite to a new position."""
        self.position = (x, y)
        self.rect.topleft = self.position

    def scale(self, width, height):
        """Scales the sprite by the given factors."""
        self.image = pygame.transform.scale(self.image, (int(width), int(height)))
        self.position = (self.true_position[0] - ((width - self.true_width) / 2), self.true_position[1] - ((height - self.true_height) / 2))

        self.rect = self.image.get_rect(topleft=self.position)

    def scale_factor(self, factor):
        """Scales the sprite by the given factor."""
        new_width = self.true_width * factor
        new_height = self.true_height * factor
        self.scale(new_width, new_height)
    
    def reset_scale(self):
        """Resets the sprite to its original size."""
        self.scale(self.true_width, self.true_height)
        self.position = self.true_position
        self.rect = self.image.get_rect(topleft=self.position)
        
        image = engine.get_image(self.image_path)
        self.image = pygame.transform.scale(image, (self.true_width,  self.true_height))
        
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
    
    def render(self):
        """Renders the sprite on the screen at its position."""
        if self.is_hovered():
            self.scale_factor(1.1)
        else:
            self.reset_scale()

        super().render()