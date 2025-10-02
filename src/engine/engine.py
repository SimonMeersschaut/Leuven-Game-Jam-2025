import pygame

from scenes.menu import MenuScene
from scenes.game import GameScene
from scenes.loading import LoadingScene


class Engine:
    """One instance will controll the entire game rendering process."""

    def __init__(self):
        self.clock = pygame.time.Clock()
        pygame.mixer.init()

        self.scenes = {
            "MENU": MenuScene(),
            "GAME": GameScene(),
            "LOADING": LoadingScene(),
        }
        self.current_scene = self.scenes["MENU"]

    def switch_scene(self, scene_name: str):
        self.current_scene = self.scenes[scene_name]
        self.current_scene.load(self)

    def start(self):
        pygame.init()
        # DISPLAY_W, DISPLAY_H = 1920, 1080
        pygame.display.set_caption("Game Jam")

        self.screen = pygame.display.set_mode((1000, 1000))#, pygame.FULLSCREEN)
        self.current_scene.load(self)
        
        running = True
        while running:
            self.clock.tick(60)
            # audio_counter += 1
            # if audio_counter > 2100:
            #     audio_counter = 0
            #     audio.play('resources/audio/background.mp3')
            
            ################################# CHECK PLAYER INPUT #################################
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
            
            ################################# UPDATE/ Animate SPRITE #################################
            self.current_scene.render(self)

            ################################# UPDATE WINDOW AND DISPLAY #################################
            pygame.display.flip()