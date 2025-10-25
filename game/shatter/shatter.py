import math
import pygame
import random

def draw_points(points, surf):
    for point in points:
        pygame.draw.circle(surf, (0, 255, 0), point, 5)

def index_to_radians(index, pieces: int) -> float:
    return math.radians(index * (360.0 / pieces) - 90)

def create_polygon_points(theta, center, radius, w, h, direction: int):
    MIN_VERTICES = 20
    MAX_VERTICES = 30

    MIN_MOVE = 0
    MAX_MOVE = 7

    # Create split points (points on the line of the split).
    cx, cy = center
    create_split_points = lambda theta, points_radii : [(cx + r * math.cos(theta), cy + r * math.sin(theta)) for r in points_radii]

    points_radii = [0] + sorted([random.random()*w/2 for _ in range(random.randint(MIN_VERTICES, MAX_VERTICES))]) + [w/2]
    split_points_1 = create_split_points(theta, points_radii)

    # move the split points perpendicular to the split line
    move_split_points = lambda theta, split_points, direction: [
        (
            split_point_x + random.randint(MIN_MOVE, MAX_MOVE)*(-math.sin(theta))*direction, # x coordinate
            split_point_y + random.randint(MIN_MOVE, MAX_MOVE)*(math.cos(theta))*direction,  # y coordinate
            # Note that we move it perpendicular to theta, so that sin(theta + pi/2) = cos(theta)
        )
            for (split_point_x, split_point_y) in split_points
    ]
    moved_split_points = move_split_points(theta, split_points_1, direction)

    # draw the golden polygon (debug visualization)
    end_point = (cx + radius * math.cos(theta), cy + radius * math.sin(theta))
    polygon_points = [center] + moved_split_points + [end_point] + [center]
    return polygon_points

LEFT = False
RIGHT = True

def do_break(i, split_lines: list[bool], side:bool):
    return split_lines[(i + (1 if side==RIGHT else 0)) % 8]

def shatter_plate(surface, split_lines: list[bool], pieces=8):
    """Split a circular plate surface into `pieces` wedges (from center).

    Returns a list of pygame.Surface objects (each same size as input, with
    per-pixel alpha so only the wedge is visible). If `show` is True and OpenCV
    is available, the function will display a grid of pieces in a single
    OpenCV window.
    """

    if len([split_line for split_line in split_lines if split_line]) < 2:
        raise ValueError("A plate splits in at least two pieces.")

    if isinstance(surface, str):
        surface = pygame.transform.scale(pygame.image.load(surface),(400, 400))

    # Ensure pygame initialized
    if not pygame.get_init():
        pygame.init()

    # surface = surface.convert_alpha()
    w, h = surface.get_size()
    cx, cy = w // 2, h // 2
    radius = min(cx, cy)

    thetas = []
    for split_index in range(pieces):
        if split_lines[split_index]:
            # find next break line
            end_split_line_index = split_index + 1
            while end_split_line_index <= 7 and (not split_lines[end_split_line_index]):
                end_split_line_index += 1

            # Create attendance list
            attendance_list = [False for _ in range(8)]
            for i in range(split_index, end_split_line_index):
                attendance_list[i] = True

            thetas.append((
                index_to_radians(split_index, pieces), 
                index_to_radians(end_split_line_index, pieces), 
                attendance_list
            ))


    wedges = []
    for (theta_start, theta_end, attendance_list) in thetas:

        # Build polygon points: center + points along arc from theta1 to theta2
        center = (cx, cy)

        # Create arc
        arc = []
        steps = max(2, int(radius * (theta_end - theta_start) / 8))
        for s in range(steps + 1):
            t = theta_start + (theta_end - theta_start) * (s / steps)
            x = cx + radius * math.cos(t)
            y = cy + radius * math.sin(t)
            arc.append((int(x), int(y)))

        # Create broken break line
        gold_glues = []
        for side, theta in [(LEFT, theta_start), (RIGHT, theta_end)]:
            direction = 1 if side == LEFT else -1

            golden_mask = pygame.Surface((w, h), pygame.SRCALPHA)
            golden_mask.fill((0, 0, 0, 0))
            inverse_golden_mask = pygame.Surface((w, h), pygame.SRCALPHA)
            inverse_golden_mask.fill((255, 255, 255, 255))

            polygon_points = create_polygon_points(theta, center, radius, w, h, direction)

            pygame.draw.polygon(golden_mask, (255, 255, 255, 255), polygon_points)
            pygame.draw.polygon(inverse_golden_mask, (0, 0, 0, 0), polygon_points)

            # Multiply RGB/alpha by mask; polygon area becomes transparent
            surface.blit(inverse_golden_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Create gold glue
            golden_glue = pygame.Surface((w, h), pygame.SRCALPHA)
            golden_glue.fill((255, 215, 0, 255)) # Gold Color
            golden_glue.blit(golden_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            gold_glues.append(golden_glue)

        mask_points = [center] + arc

        # Create mask for this wedge
        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.polygon(mask, (255, 255, 255, 255), mask_points)

        # Copy original and multiply by mask so outside becomes transparent
        piece = pygame.Surface((w, h), pygame.SRCALPHA)
        piece.blit(surface, (0, 0))
        piece.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        wedges.append((gold_glues[0], piece, gold_glues[1], attendance_list, (cx, cy), theta_start, theta_end))
        # attendance_list: where this fragment exists (in the list of the entire plate)
        
    return wedges