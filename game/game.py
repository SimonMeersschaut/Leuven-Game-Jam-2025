from engine import engine

class Game:
    def __init__(self):
        ...

    def update(self, delta_t: float, events: list):
        ...

    def render(self):
        engine.fill((0, 0, 0))
    
game = Game()