import pygame
from enum import Enum, auto

class Modes(Enum):
    main_menu = auto()
    game = auto()

class Engine:
    """A single instance will controll the entire game rendering process."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Game Jam 2025")

        self.DISPLAY_W, self.DISPLAY_H = 1280, 720
        self._screen = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        # make the real window resizable so we can auto-scale the internal 1080p surface
        self.real_screen = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H), pygame.RESIZABLE) #, pygame.FULLSCREEN)
        # track real window size
        self.real_width, self.real_height = self.real_screen.get_size()
        # store canonical internal resolution for scaling computations
        self._base_width, self._base_height = self.DISPLAY_W, self.DISPLAY_H

        self.clock = pygame.time.Clock()
        pygame.mixer.init()
        pygame.font.init()

        self.fonts = {}
        self.images_cache = {}

        self.mode = Modes.main_menu

        self.width, self.height = 1920, 1080
    
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
        

        FRAME_RATE = 60 # FPS (Hz)
        FREQUENCY = 1/FRAME_RATE # seconds

        menu.shop.game = game
        
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
                elif event.type == pygame.VIDEORESIZE:
                    # update tracked real window size and recreate the display surface
                    self.real_width, self.real_height = event.size
                    self.real_screen = pygame.display.set_mode((self.real_width, self.real_height), pygame.RESIZABLE)

            # Update and draw active scene
            if self.mode == Modes.main_menu:
                menu.update(delta_t, events)
                menu.render()
            elif self.mode == Modes.game:
                game.update(delta_t, events)
                game.render()
            else:
                raise ValueError("EngineError: the type of mode was not registered in the engine.")

            # Send screen update: scale internal 1920x1080 surface to window while preserving 16:9
            # compute scale that fits the base surface into the real window
            scale_x = self.real_width / self._base_width
            scale_y = self.real_height / self._base_height
            scale = min(scale_x, scale_y)
            scaled_w = max(1, int(self._base_width * scale))
            scaled_h = max(1, int(self._base_height * scale))

            # create scaled surface and center it, fill background black for letter/pillar boxing
            scaled_surface = pygame.transform.smoothscale(self._screen, (scaled_w, scaled_h))
            self.real_screen.fill((0, 0, 0))
            dest_x = (self.real_width - scaled_w) // 2
            dest_y = (self.real_height - scaled_h) // 2
            self.real_screen.blit(scaled_surface, (dest_x, dest_y))
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
                    return self.images_cache[image_path][index]
                else:
                    return self.images_cache[image_path]
        
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

    def get_scaled_mouse_pos(self) -> tuple[int, int]:
        """Returns the mouse position scaled to the internal 1920x1080 resolution."""
        mx, my = pygame.mouse.get_pos()
        scale_x = self.real_width / self._base_width
        scale_y = self.real_height / self._base_height
        scale = min(scale_x, scale_y)

        # compute offsets due to letter/pillar boxing
        offset_x = (self.real_width - (self._base_width * scale)) / 2
        offset_y = (self.real_height - (self._base_height * scale)) / 2

        # scale mouse position back to internal resolution
        scaled_mx = (mx - offset_x) / scale
        scaled_my = (my - offset_y) / scale

        return int(scaled_mx), int(scaled_my)

engine = Engine()