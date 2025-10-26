from engine import engine 
import pygame

def get_partial_live_im(part: float):
    """Return a Surface showing a partial life plate.

    part: float between 0.0 and 1.0 inclusive.
    0.0 -> empty plate (lost_life.png)
    1.0 -> full plate (life.png)
    intermediate values -> left-to-right filled portion of the life image over the lost image
    """
    # clamp
    try:
        part = float(part)
    except Exception:
        part = 0.0
    part = max(0.0, min(1.0, part))

    # Load both images
    life = engine.get_image('resources/images/life.png')
    lost = engine.get_image('resources/images/lost_life.png')

    # Scale to the same display size used elsewhere in Stats (approx 3%)
    # Use transform.scale_by if available, otherwise fallback to smoothscale
    try:
        life = pygame.transform.scale_by(life, 0.03)
        lost = pygame.transform.scale_by(lost, 0.03)
    except Exception:
        # fallback: scale by 3% of original size
        lw, lh = life.get_size()
        sw, sh = max(1, int(lw * 0.03)), max(1, int(lh * 0.03))
        life = pygame.transform.smoothscale(life, (sw, sh))
        lw2, lh2 = lost.get_size()
        sw2, sh2 = max(1, int(lw2 * 0.03)), max(1, int(lh2 * 0.03))
        lost = pygame.transform.smoothscale(lost, (sw2, sh2))

    w, h = life.get_size()

    # Edge cases
    if part <= 0.0:
        return lost.copy() if hasattr(lost, 'copy') else lost
    if part >= 1.0:
        return life.copy() if hasattr(life, 'copy') else life

    # Create a new surface with alpha and compose: base is lost, then overlay left portion of life
    res = pygame.Surface((w, h), flags=pygame.SRCALPHA)
    # draw the empty/lost plate first
    res.blit(lost, (0, 0))

    # width of filled area (left-to-right)
    fill_w = max(1, int(round(part * w)))

    # copy filled portion from the life image
    try:
        filled = life.subsurface((0, 0, fill_w, h)).copy()
    except Exception:
        # if subsurface failed for any reason, scale full life to a temporary surface and blit clipped
        filled = pygame.Surface((fill_w, h), flags=pygame.SRCALPHA)
        filled.blit(life, (0, 0), (0, 0, fill_w, h))

    res.blit(filled, (0, 0))
    return res

class Stats:
    def __init__(self):
        self.lives_image = engine.get_image('resources/images/life.png')
        self.lives_image = pygame.transform.scale_by(self.lives_image,0.03)
        self.width_lives_image, self.length_lives_image=self.lives_image.get_size()

        self.lost_lives_image=engine.get_image('resources/images/lost_life.png')
        self.lost_lives_image=pygame.transform.scale_by(self.lost_lives_image,0.03)
        self.width_lost_lives_image, self.length_lost_lives_image=self.lost_lives_image.get_size()

        self.lifes_background=pygame.transform.scale(engine.get_image('resources/images/lifes_background.png'),(430,100))

        self.total_money = 50
        self.money=0
        self.multiplier=1
        self.money_image=engine.render_text('birthstone',60,f'€{self.money}',(255,255,255))
        self.width_money_image,self.length_money_image=self.money_image.get_size()

        self.lives=1
        self.max_lives = 1

        self.gouden_kak_bought = False # Set by shop
        self.plates_merged = 0
    
    def play_again(self):
        self.money=0
        self.multiplier=1
        self.money_image=engine.render_text('birthstone',60,f'€{self.money}',(255,255,255))
        self.width_money_image,self.length_money_image=self.money_image.get_size()

        self.lives=self.max_lives

        self.plates_merged = 0

    def lose_life(self, amount:float):
        if self.lives>0:
            self.lives-=amount
    
    def add_money(self,amount):
        self.money += amount*self.multiplier
        self.total_money += amount*self.multiplier

        self.money_image=engine.render_text('birthstone',80,f'€{self.money}',(0,255,0))
        self.width_money_image,self.length_money_image=self.money_image.get_size()
    
    def update(self, delta_t: float, events: list):
        self.money_image=engine.render_text('birthstone',60,f'€{self.money}',(255,255,255))

    def render(self):
        engine.render_image(self.lifes_background,(10,10))

        for lost_live in range(self.max_lives):
            engine.render_image(self.lost_lives_image,(50+1.5*(self.lives*self.width_lives_image)+self.width_lost_lives_image*lost_live*1.5,50))

        for live in range(int(self.lives)):
            engine.render_image(self.lives_image,(25+1.3*live*self.width_lives_image,30))
        
        # draw last partial live
        pos_x = 25+1.3*(live+1)*self.width_lives_image
        part = self.lives - int(self.lives)
        im = get_partial_live_im(part)

        engine.render_image(self.money_image,(engine.DISPLAY_W-self.width_money_image-30,30))
