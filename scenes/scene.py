from engine import Engine

class Scene:
    """Each instance is a renderable game-scene."""

    def __init__(self):
        pass
    
    def load(self, engine: object):
        pass
    
    def render(self, engine: Engine, events: list, dt: float):
        pass