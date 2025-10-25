from shatter import shatter_surface
from display import show_pieces_cv2, show_surface

if __name__ == "__main__":
    image_path = "plate.png"

    pieces = shatter_surface(image_path, pieces=8)
    show_surface(pieces)