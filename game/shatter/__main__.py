from shatter import shatter_surface
from display import show_pieces_cv2, show_surface
from image_handler import image_handler

if __name__ == "__main__":
    image_path = "plate.png"

    piece = image_handler.get_wedge(

    )
    # show_surface(pieces)
    # show_pieces_cv2([piece[1] for piece in pieces])
    show_surface(piece)