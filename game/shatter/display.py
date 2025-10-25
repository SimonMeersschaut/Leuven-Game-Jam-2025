import cv2
import numpy as np
import pygame
import math

def show_pieces_cv2(pieces: list, cols=4, window_name='pieces'):
    """Arrange pieces in a grid and display using OpenCV.

    Each piece is a pygame.Surface (with alpha). We convert to BGR numpy
    arrays and place them into a grid image.
    """
    if cv2 is None or np is None:
        raise RuntimeError("OpenCV (cv2) and numpy are required to show pieces")

    if not pieces:
        return

    w, h = pieces[0].get_size()

    # Make a canvas large enough to place pieces around the center
    canvas_w = max(w * 3, int(w * 2.5))
    canvas_h = max(h * 3, int(h * 2.5))

    # Start with a red background (BGR for OpenCV: (0,0,255))
    canvas = np.zeros((canvas_h, canvas_w, 3), dtype=np.uint8)
    canvas[:, :] = (0, 0, 255)

    center_x = canvas_w // 2
    center_y = canvas_h // 2
    offset = 20  # pixels away from center

    for idx, surf in enumerate(pieces):
        # RGB array from pygame surface
        arr = pygame.surfarray.array3d(surf)
        arr = np.transpose(arr, (1, 0, 2))

        # Try to read alpha channel so we only copy opaque pixels
        try:
            alpha = pygame.surfarray.array_alpha(surf)
            alpha = np.transpose(alpha, (1, 0))
        except Exception:
            # If alpha not available, treat entire surface as opaque
            alpha = np.full((h, w), 255, dtype=np.uint8)

        # Convert RGB->BGR for OpenCV
        bgr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)

        # Compute radial placement: angle depends on index
        angle = 2 * math.pi * (idx / len(pieces))
        dx = int(math.cos(angle) * offset)
        dy = int(math.sin(angle) * offset)

        x = center_x - (w // 2) + dx
        y = center_y - (h // 2) + dy

        # Clip to canvas bounds and compute source slices
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(canvas_w, x + w)
        y1 = min(canvas_h, y + h)

        if x0 >= x1 or y0 >= y1:
            continue

        sx0 = x0 - x
        sy0 = y0 - y
        sx1 = sx0 + (x1 - x0)
        sy1 = sy0 + (y1 - y0)

        region = canvas[y0:y1, x0:x1]
        src_bgr = bgr[sy0:sy1, sx0:sx1]
        src_alpha = alpha[sy0:sy1, sx0:sx1]

        mask = src_alpha > 0
        if mask.all():
            region[:, :] = src_bgr
        else:
            region[mask] = src_bgr[mask]

    cv2.imshow(window_name, canvas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_surface(surface):
    """Show a single pygame.Surface in an OpenCV window (keeps backward compat)."""
    if cv2 is None or np is None:
        raise RuntimeError("OpenCV (cv2) and numpy are required to show the surface")

    if not pygame.get_init():
        pygame.init()

    arr = pygame.surfarray.array3d(surface)
    arr = np.transpose(arr, (1, 0, 2))
    cv_img = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
    cv2.imshow('loaded image', cv_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
