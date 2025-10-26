from shatter import shatter_plate
from display import show_pieces_cv2, show_surface

if __name__ == "__main__":
    image_path = "plate.png"

    pieces = shatter_plate("../../resources/images/plate.png", [True, False, False, False, True, False, False, False])

    # show_surface(pieces)
    show_pieces_cv2([piece[1] for piece in pieces])
    # show_surface(piece)
