from engine import Engine, engine, Modes
import pygame

class Menu:
    def __init__(self):
        self.state = "main_menu"
    
    def update(self, delta_t, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == "main_menu":
                    if pygame.mouse.get_pos()[0] in range(400, 600) and pygame.mouse.get_pos()[1] in range(160, 260):
                        engine.mode = Modes.game
                    elif pygame.mouse.get_pos()[0] in range(400, 600) and pygame.mouse.get_pos()[1] in range(300, 400):
                        self.state = "credits"
                elif self.state == "credits":
                    if pygame.mouse.get_pos()[0] in range(400, 600) and pygame.mouse.get_pos()[1] in range(400, 500):
                        self.state = "main_menu"

    def render(self):
        engine.fill((60, 60, 60))
        
        paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1000, 600))
        engine.render_image(paper_background, (0, 0))
        
        

        if self.state == "main_menu":
            title = engine.render_text("pixel", 48, "KUL Game Jam 2025", (255, 255, 255))
            engine.render_image(title, (250, 20))
            
            play_button = pygame.transform.scale(engine.get_image('resources/buttons/play_paper.jpeg'), (200, 100))
            engine.render_image(play_button, (400, 160))

            credits_button = pygame.transform.scale(engine.get_image('resources/buttons/credits_paper.jpeg'), (200, 100))
            engine.render_image(credits_button, (400, 300))

        elif self.state == "credits":
            
            credits_text = pygame.transform.scale(engine.get_image('resources/buttons/credits_list_paper.png'), (2448/6, 3262/6))
            engine.render_image(credits_text, (500 - credits_text.get_width()/2, -100))

            back_button = pygame.transform.scale(engine.get_image('resources/buttons/back_paper.jpeg'), (200, 100))
            engine.render_image(back_button, (400, 400))


menu = Menu() # singleton