from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
from .credits import Credits
from .shop import Shop
import pygame

class Menu:
    def __init__(self):
        self.state = "main_menu"

        self.play_button = Button('resources/buttons/play.png', (-1, 160), height=100, align_x="center")
        self.shop_button = Button('resources/buttons/shop.png', (-1, 300), height=100, align_x="center")
        self.credits_button = Button('resources/buttons/credits.png', (-1, 440), height=100, align_x="center")

        self.title=pygame.transform.scale_by(engine.get_image('resources/images/title.png',),0.4)
        self.width_title, self.length_title=self.title.get_size()

        self.title_backup=engine.render_text('birthstone',100,'Porcelain Panic',(25,50,118)) #Dit is backup als getekende titel niet klaargeraakt
        self.width_title_backup, self.length_title_backup=self.title_backup.get_size()

        self.shop = Shop(self)
        self.credits = Credits(self)

        self.paper_background = pygame.transform.scale(engine.get_image('resources/buttons/paper_background.jpeg'), (1920, 1080))

    def update(self, delta_t, events):

        if self.state == "shop":
            self.shop.update()
        elif self.state == "credits":
            self.credits.update()
        else:
            if self.play_button.update_and_check_clicked():
                engine.mode = Modes.game
                engine.start_game()
            elif self.shop_button.update_and_check_clicked():
                self.state = "shop"
            elif self.credits_button.update_and_check_clicked():
                self.state = "credits"

    def render(self):
        
        if self.state == "shop":
            self.shop.render()
        elif self.state == "credits":
            self.credits.render()
        
        else:
            engine.fill((60, 60, 60))
            
            start_screen_background = engine.get_image('resources/images/splash_screen.jpg')
            start_screen_background = pygame.transform.rotate(start_screen_background, -90)
            start_screen_background = pygame.transform.scale(start_screen_background,(1280,720))
            engine.render_image(start_screen_background, (0, 0))

            self.play_button.render()
            self.shop_button.render()
            self.credits_button.render()

            #engine.render_image(self.title,(50,10)) #Hier komt de afbeelding indien die gefixt geraakt
            engine.render_image(self.title_backup,(engine.DISPLAY_W/2-self.width_title_backup/2,0))
            #title = engine.render_text("pixel", 48, "KUL Game Jam 2025", (0, 255, 255))
            #engine.render_image(title, (250, 20))


menu = Menu() # singleton