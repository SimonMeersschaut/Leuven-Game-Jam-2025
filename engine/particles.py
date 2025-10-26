import random
import math
import pygame
from typing import Tuple, List


class Particle:
    """Simple particle: position, velocity, color, radius, lifetime.

    Rendered to a small per-particle surface with per-pixel alpha so it fades out.
    """

    def __init__(self, pos: Tuple[float, float], vel: Tuple[float, float], color: Tuple[int, int, int] = (255, 215, 0), radius: float = 4.0, lifetime: float = 1.0, gravity: float = 700.0):
        self.x = float(pos[0])
        self.y = float(pos[1])
        self.vx = float(vel[0])
        self.vy = float(vel[1])
        self.color = color
        self.radius = float(max(1.0, radius))
        self.lifetime = float(max(0.001, lifetime))
        self.age = 0.0
        # gravity in pixels per second squared (positive = downward)
        self.gravity = float(gravity)

    def update(self, dt: float) -> bool:
        """Advance particle. Returns True if still alive."""
        self.age += dt
        # apply gravity to vertical velocity
        self.vy += self.gravity * dt
        # integrate position
        self.x += self.vx * dt
        self.y += self.vy * dt
        return self.age < self.lifetime

    def render(self, surface: pygame.Surface) -> None:
        # alpha fades from 255 to 0 over lifetime
        t = 1.0 - (self.age / self.lifetime)
        t = max(0.0, min(1.0, t))
        alpha = int(255 * t)
        r = max(1, int(self.radius))

        # draw into a small temporary surface with per-pixel alpha
        surf = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
        col = (self.color[0], self.color[1], self.color[2], alpha)
        pygame.draw.circle(surf, col, (r, r), r)
        surface.blit(surf, (int(self.x - r), int(self.y - r)))


class ParticleSystem:
    """Manages many particles: spawn, update, render."""

    def __init__(self):
        self.particles: List[Particle] = []

    def spawn(self, pos: Tuple[float, float], count: int = 20, color: Tuple[int, int, int] = (255, 215, 0), spread: float = 60.0, speed: float = 200.0, lifetime: float = 1.0, radius: float = 4.0, angle_min: float | None = None, angle_max: float | None = None, gravity: float = 700.0) -> None:
        """Spawn `count` particles around `pos`.

        - pos: center position (internal resolution coordinates)
        - spread: random position jitter around pos
        - speed: base speed (pixels per second)
        - lifetime: seconds
        """
        for _ in range(max(0, int(count))):
            # If an angle range is provided, sample within that range so callers can bias direction
            if angle_min is None or angle_max is None:
                angle = random.uniform(0.0, math.tau)
            else:
                angle = random.uniform(angle_min, angle_max)
            speed_i = random.uniform(0.5 * speed, 1.0 * speed)
            vx = math.cos(angle) * speed_i
            vy = math.sin(angle) * speed_i
            px = pos[0] + random.uniform(-spread, spread)
            py = pos[1] + random.uniform(-spread, spread)
            life = random.uniform(0.7 * lifetime, 1.3 * lifetime)
            p = Particle((px, py), (vx, vy), color=color, radius=radius, lifetime=life, gravity=gravity)
            self.particles.append(p)

    def update(self, dt: float) -> None:
        if not self.particles:
            return
        alive = []
        for p in self.particles:
            if p.update(dt):
                alive.append(p)
        self.particles = alive

    def render(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.render(surface)
