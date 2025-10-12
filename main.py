from engine import engine, Engine

import pygame

# This function is called each frame
def render_new_frame(events: list, dt: float):
    engine.fill((0, 100, 0))

    txt = engine.render_text("pixel", 20, "Hello World!", (255, 255, 255))
    engine.render_image(txt, (50, 50))

if __name__ == "__main__":
    engine.run(render_new_frame)