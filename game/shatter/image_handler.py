import pygame
from shatter import shatter_surface

class ImageHandler:
    def __init__(self):
        ...
    
    def get_wedge(self) -> pygame.Surface:
        pieces = shatter_surface("plate.png", [True, True, False, False, True, False, False, False])
        pieces[0][1].blit(pieces[0][0], (0, 0))
        return pieces[0][1]

image_handler = ImageHandler()