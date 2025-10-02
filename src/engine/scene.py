
class Scene:
    """Each instance is a renderable game-scene."""

    def __init__(self):
        ...
    
    def load(self, engine: object):
        ...
    
    def render(self, engine: object):
        ...