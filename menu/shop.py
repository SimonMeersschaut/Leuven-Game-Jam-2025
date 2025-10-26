from engine import Engine, engine, Modes
from engine.sprite import Button, Sprite
import pygame


class Shop:
    def __init__(self, main_menu):
        self.state = "main_menu"
        self.back_button = Button('resources/buttons/main_menu.png', (-1, 600), height=100, align_x="center")
        self.main_menu = main_menu

        self.buy_multiplier = Button('resources/buttons/multiplier.png', (-1, 300), height=100, align_x="center")
        self.multiplier_price = 30

        self.buy_kak = Button('resources/buttons/golden_poop.png', (engine.DISPLAY_W/6+5, 300), height=100)
        self.kak_price = 500
        self.kak_disabled = False

        self.buy_extra_leven = Button('resources/buttons/extra_life.png', (engine.DISPLAY_W*5/6 - 85, 300), height=100)
        self.extra_leven_price = 500

        self.shop_background = pygame.transform.scale(pygame.transform.rotate(engine.get_image('resources/images/splash_screen.jpg'),
                                                       -90),(engine.DISPLAY_W,engine.DISPLAY_H))

    def update(self):
        if self.back_button.update_and_check_clicked():
            self.main_menu.state = "main_menu"
        elif self.buy_multiplier.update_and_check_clicked():
            if self.game.stats.total_money >= self.multiplier_price:
                self.game.stats.total_money -= self.multiplier_price
                self.game.stats.multiplier *= 2
                self.multiplier_price *= 3
        elif self.buy_kak.update_and_check_clicked():
            if self.game.stats.total_money >= self.kak_price:
                if not self.kak_disabled:
                    self.game.stats.total_money -= self.kak_price
                    self.game.stats.gouden_kak_bought = True
                    self.kak_disabled = True
        elif self.buy_extra_leven.update_and_check_clicked():
            if self.game.stats.total_money >= self.extra_leven_price:
                self.game.stats.total_money -= self.extra_leven_price
                self.game.stats.max_lives += 1

    def render(self):
        engine.fill((60, 60, 60))

        engine.render_image(self.shop_background, (0, 0))

        self.back_button.render()

        self.buy_multiplier.render()
        self.buy_kak.render()
        self.buy_extra_leven.render()


        self.money_image=engine.render_text('birthstone',80,f'€{self.game.stats.total_money}',(0,255,0))
        self.width_money_image,self.length_money_image=self.money_image.get_size()
        engine.render_image(self.money_image,(engine.DISPLAY_W-self.width_money_image-30,30))

        self.multiplier_image=engine.render_text('birthstone',60,f'x{self.game.stats.multiplier*2} MULTIPLIER',(50,50,150))
        self.width_multiplier_image,self.length_multiplier_image=self.multiplier_image.get_size()
        engine.render_image(self.multiplier_image,((engine.DISPLAY_W - self.width_multiplier_image)/2,225))

        if self.game.stats.total_money >= self.multiplier_price:
            self.multiplier_price_image=engine.render_text('birthstone',40,f'€{self.multiplier_price}',(50,200,50))
        else:
            self.multiplier_price_image=engine.render_text('birthstone',40,f'€{self.multiplier_price}',(200,50,50))
        self.width_multiplier_price_image,self.length_multiplier_price_image=self.multiplier_price_image.get_size()
        engine.render_image(self.multiplier_price_image,((engine.DISPLAY_W - self.width_multiplier_price_image)/2,400))


        self.kak_image=engine.render_text('birthstone',60,f'GOUDEN KAK',(50,50,150))
        self.width_kak_image,self.length_kak_image=self.kak_image.get_size()
        engine.render_image(self.kak_image,(engine.DISPLAY_W/5 - self.width_kak_image/2,225))

        if self.kak_disabled:
            self.kak_price_image=engine.render_text('birthstone',40,f'out of stock',(50,50,150))
        elif self.game.stats.total_money >= self.kak_price:
            self.kak_price_image=engine.render_text('birthstone',40,f'€{self.kak_price}',(50,200,50))
        else:
            self.kak_price_image=engine.render_text('birthstone',40,f'€{self.kak_price}',(200,50,50))
        self.width_kak_price_image,self.length_kak_price_image=self.kak_price_image.get_size()
        engine.render_image(self.kak_price_image,(engine.DISPLAY_W/5 - self.width_kak_price_image/2,400))


        self.extra_leven_image=engine.render_text('birthstone',60,f'EXTRA LEVEN',(50,50,150))
        self.width_extra_leven_image,self.length_extra_leven_image=self.extra_leven_image.get_size()
        engine.render_image(self.extra_leven_image,(engine.DISPLAY_W*4/5 - self.width_extra_leven_image/2,225))

        self.extra_leven_price_image=engine.render_text('birthstone',40,f'out of stock',(50,50,150))
        if self.game.stats.total_money >= self.extra_leven_price:
            self.extra_leven_price_image=engine.render_text('birthstone',40,f'€{self.extra_leven_price}',(50,200,50))
        else:
            self.extra_leven_price_image=engine.render_text('birthstone',40,f'€{self.extra_leven_price}',(200,50,50))
        self.width_extra_leven_price_image,self.length_extra_leven_price_image=self.extra_leven_price_image.get_size()
        engine.render_image(self.extra_leven_price_image,(engine.DISPLAY_W*4/5 - self.width_extra_leven_price_image/2,400))