import math
import sys
import pygame
import cv2
import numpy as np


def shatter_surface(surface, pieces=8):
    """Split a circular plate surface into `pieces` wedges (from center).

    Returns a list of pygame.Surface objects (each same size as input, with
    per-pixel alpha so only the wedge is visible). If `show` is True and OpenCV
    is available, the function will display a grid of pieces in a single
    OpenCV window.
    """
    # Allow passing a path
    if isinstance(surface, str):
        surface = pygame.image.load(surface)

    # Ensure pygame initialized
    if not pygame.get_init():
        pygame.init()

    # surface = surface.convert_alpha()
    w, h = surface.get_size()
    cx, cy = w // 2, h // 2
    radius = min(cx, cy)

    wedges = []
    for i in range(pieces):
        theta1 = math.radians(i * (360.0 / pieces))
        theta2 = math.radians((i + 1) * (360.0 / pieces))

        # Build polygon points: center + points along arc from theta1 to theta2
        pts = [(cx, cy)]
        steps = max(2, int(radius * (theta2 - theta1) / 8))
        for s in range(steps + 1):
            t = theta1 + (theta2 - theta1) * (s / steps)
            x = cx + radius * math.cos(t)
            y = cy + radius * math.sin(t)
            pts.append((int(x), int(y)))

        # Create mask for this wedge
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.polygon(mask, (255, 255, 255, 255), pts)

        # Copy original and multiply by mask so outside becomes transparent
        piece = pygame.Surface((w, h), pygame.SRCALPHA)
        piece.blit(surface, (0, 0))
        piece.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        wedges.append(piece)

    return wedges

