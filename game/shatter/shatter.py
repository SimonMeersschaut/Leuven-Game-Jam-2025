import math
import pygame
import random

def draw_points(points, surf):
    for point in points:
        pygame.draw.circle(surf, (0, 255, 0), point, 5)

def create_polygon_points(theta, center, radius, w, h, direction: int):
    MIN_VERTICES = 20
    MAX_VERTICES = 30

    MIN_MOVE = 5
    MAX_MOVE = 15

    # Create split points (points on the line of the split).
    cx, cy = center
    create_split_points = lambda theta, points_radii : [(cx + r * math.cos(theta), cy + r * math.sin(theta)) for r in points_radii]

    points_radii = sorted([random.random()*w/2 for _ in range(random.randint(MIN_VERTICES, MAX_VERTICES))])
    split_points_1 = create_split_points(theta, points_radii)
    split_points_2 = create_split_points(theta, points_radii)

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

def shatter_surface(surface, pieces=8):
    """Split a circular plate surface into `pieces` wedges (from center).

    Returns a list of pygame.Surface objects (each same size as input, with
    per-pixel alpha so only the wedge is visible). If `show` is True and OpenCV
    is available, the function will display a grid of pieces in a single
    OpenCV window.
    """


    if isinstance(surface, str):
        surface = pygame.transform.scale(pygame.image.load(surface),(400, 400))

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
        center = (cx, cy)

        # Create arc
        arc = []
        steps = max(2, int(radius * (theta2 - theta1) / 8))
        for s in range(steps + 1):
            t = theta1 + (theta2 - theta1) * (s / steps)
            x = cx + radius * math.cos(t)
            y = cy + radius * math.sin(t)
            arc.append((int(x), int(y)))
        
        polygon_points_1 = create_polygon_points(theta1, center, radius, w, h, 1)
        polygon_points_2 = create_polygon_points(theta2, center, radius, w, h, -1)

        golden_mask = pygame.Surface((w, h), pygame.SRCALPHA)
        golden_mask.fill((0, 0, 0, 0))
        inverse_golden_mask = pygame.Surface((w, h), pygame.SRCALPHA)
        inverse_golden_mask.fill((255, 255, 255, 255))

        for polygon_points in [polygon_points_1, polygon_points_2]:
            pygame.draw.polygon(golden_mask, (255, 255, 255, 255), polygon_points)
            pygame.draw.polygon(inverse_golden_mask, (0, 0, 0, 0), polygon_points)

        plate_minus_golden = surface.copy()
        # Multiply RGB/alpha by mask; polygon area becomes transparent
        plate_minus_golden.blit(inverse_golden_mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # draw_points(polygon_points, plate_minus_golden)

        return plate_minus_golden

    #     mask_points = [center] + arc

    #     # Create mask for this wedge
    #     mask = pygame.Surface((w, h), pygame.SRCALPHA)
    #     pygame.draw.polygon(mask, (255, 255, 255, 255), mask_points)

    #     # Copy original and multiply by mask so outside becomes transparent
    #     piece = pygame.Surface((w, h), pygame.SRCALPHA)
    #     piece.blit(surface, (0, 0))
    #     piece.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    #     wedges.append(piece)

    # return wedges

