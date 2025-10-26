import resources
from engine import Engine, engine, Modes
from engine.pointers import pointers
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
        
        self.previously_hovered = False
        self.previously_clicked = False
        
        if isinstance(image_path, str): 
            image = engine.get_image(image_path)
        else:
            image = image_path # can be a surface already
        
        if height and width:
            pass
        elif height:
            width = int(image.get_width() * (height / image.get_height()))
        elif width:
            height = int(image.get_height() * (width / image.get_width()))
        else:
            height = image.get_height()
            width = image.get_width()
        
        self.src_image = image
        self.image = pygame.transform.scale(image, (width, height))   
        
        self.true_width = width
        self.true_height = height

        if align_x:
            if align_x == "left":
                position = (0, position[1])
            elif align_x == "center":
                position = (engine.DISPLAY_W/2 - (width // 2), position[1])
            elif align_x == "right":
                position = (engine.DISPLAY_W - width, position[1])

        if align_y:
            if align_y == "top":
                position = (position[0], 0)
            elif align_y == "center":
                position = (position[0], engine.DISPLAY_H/2 - (height // 2))
            elif align_y == "bottom":
                position = (position[0], engine.DISPLAY_H - height)
        
            
        self.position = position
        self.true_position = position

        self.rect = self.image.get_rect(topleft=position)

    def move(self, x, y):
        """Moves the sprite to a new position."""
        self.position = (x, y)
        self.true_position = (x, y)
        # Does this cause problems when changing position while scaled?
        self.rect.topleft = self.position

    def scale(self, width, height):
        """Scales the sprite by the given factors."""
        self.image = pygame.transform.scale(self.src_image, (int(width), int(height)))
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
        
        # image = engine.get_image(self.image_path)
        self.image = pygame.transform.scale(self.src_image, (self.true_width,  self.true_height))
        
    def render(self):
        """Renders the sprite on the screen at its position."""
        engine.render_image(self.image, self.position)

    def is_hovered(self):
        return self.rect.collidepoint(engine.scale_position(pygame.mouse.get_pos()))  # check if mouse is over the button
    
    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed()[0]  # left mouse button

    def just_unclicked(self):
        return (not self.is_clicked()) and self.previously_clicked
            
    def get_intersecting_pointers(self):
        return pointers.get_intersecting_pointers(self.rect)
    
class Button(Sprite):
    def __init__(self, image_path, position=(0, 0), height=None, width=None, align_x=None, align_y=None):
        super().__init__(image_path, position, height, width, align_x, align_y)
    
    def update(self):
        if self.is_hovered() and not self.is_clicked():
            if self.just_unclicked():
                click_sound = pygame.mixer.Sound('resources/sounds/paper_twist_short_loud.wav')
                pygame.mixer.Sound.play(click_sound)
            
            self.scale_factor(1.1)
            
            self.previously_hovered = True
            self.previously_clicked = False         
        elif self.is_hovered() and not self.previously_hovered:
            self.scale_factor(1.1)
            self.previously_hovered = True
            self.previously_clicked = False
    
        elif self.is_clicked() and self.previously_hovered:
            if self.previously_clicked == False:
                self.scale_factor(0.9)
                
                self.previously_hovered = True
                self.previously_clicked = True
        else:
            self.reset_scale()
            self.previously_hovered = False
            self.previously_clicked = False
    
    def update_and_check_clicked(self):
        just_unclicked = self.just_unclicked()
        self.update()
        
        return just_unclicked