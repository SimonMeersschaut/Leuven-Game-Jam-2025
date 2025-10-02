import pygame

class Engine:
    """One instance will controll the entire game rendering process."""

    def __init__(self):
        ...
    
    # def load(self):
    #     ################################# LOAD UP A BASIC WINDOW AND CLOCK #################################
    #     pygame.init()
    #     # DISPLAY_W, DISPLAY_H = 1920, 1080
    #     pygame.display.set_caption("Anna's Ants")
    #     
    #     running = True
    #     clock = pygame.time.Clock()
    #     pygame.mixer.init()
    #     mode = 'menu'

        ################################# LOAD PLAYER AND SPRITESHEET ###################################
        #################################### LOAD THE LEVEL #######################################
        # world.preload('', screen)
        # menu.initialize()

        # audio.preload('resources/audio/background.mp3')
        # audio.play('resources/audio/background.mp3')
        # audio_counter = 0

    def start(self):
        screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
        running = True
        while running:
            # clock.tick(60)
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

            ################################# UPDATE WINDOW AND DISPLAY #################################
            screen.fill((0, 180, 240)) # Fills the entire screen with light blue

            pygame.display.flip()