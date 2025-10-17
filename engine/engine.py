import pygame
from enum import Enum, auto

class Modes(Enum):
    main_menu = auto()
    game = auto()

class Engine:
    """A single instance will controll the entire game rendering process."""

    def __init__(self):
        self._screen = None

        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.font.init()

        self.fonts = {}
        self.images_cache = {}

        self.mode = Modes.main_menu

        self.width, self.height = 1000, 600
    
    def get_font(self, fontname, fontsize):
        path = f"resources/fonts/{fontname}.ttf"
        identifier = (path, fontsize)
        try:
            return self.fonts[identifier]
        except KeyError:
            font = pygame.font.Font(path, fontsize)
            self.fonts.update({identifier: font})
            return font
    
    def run(self, menu, game):
        pygame.init()
        pygame.display.set_caption("Game Jam 2025")

        
        self._screen = pygame.display.set_mode((self.width, self.height)) #, pygame.FULLSCREEN)

        FRAME_RATE = 60 # FPS (Hz)
        FREQUENCY = 1/FRAME_RATE # seconds
        
        running = True
        while running:
            self.clock.tick(FRAME_RATE)
            delta_t = FREQUENCY
            # audio_counter += 1
            # if audio_counter > 2100:
            #     audio_counter = 0
            #     audio.play('resources/audio/background.mp3')
            
            # Check player input
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            
            # Update and draw active scene
            if self.mode == Modes.main_menu:
                menu.update(delta_t, events)
                menu.render()
            elif self.mode == Modes.game:
                game.update(delta_t, events)
                game.render()
            else:
                raise ValueError("EngineError: the type of mode was not registered in the engine.")

            # Send screen update
            pygame.display.flip()
    
    def render_text(self, fontname: str, fontsize: int, text:str, color: tuple[int, int, int]):
        """Returns a text surface image."""
        font = self.get_font(fontname, fontsize)
        return font.render(text, False, color)

    def get_image(self, image_path: str, index = 0, tile_size = 128):
        if image_path in self.images_cache:
            # cache hit
            if self.images_cache[image_path]:
                if '.set.' in image_path:
                    return self.cache[image_path][index]
                else:
                    return self.cache[image_path]
        
        # load image
        if '.set.' in image_path:
            tile_size = (tile_size, tile_size)
            im = pygame.image.load(image_path).convert_alpha()
            tileset_width, tileset_height = im.get_size()
            tileset = [
                im.subsurface((x, 0, tile_size[0], tile_size[1]))
                for x in range(0, tileset_width, tile_size[0])
                # for y in range(0, tileset_height, tile_size[1])
            ]
            self.images_cache.update({image_path: tileset})
            return tileset[index]
        else:
            # default image
            im = pygame.image.load(image_path).convert_alpha()
            self.images_cache.update({image_path: im})
            return im
        
    def render_image(self, image, position):
        return self._screen.blit(image, position)
    
    def fill(self, color):
        return self._screen.fill(color)

    def get_pressed_keys(self) -> dict:
        return pygame.key.get_pressed()

    def is_pressed(self, key) -> bool:
        return self.get_pressed_keys()[key]


engine = Engine()