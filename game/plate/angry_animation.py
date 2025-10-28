from engine import engine
import random
import pygame

def render_angry_animation(wave_number:int, progress: float):
    """
    Progress: getal van nul tot 1. ==> komt overeen met 3 seconden
    """
    elephant_sound = pygame.mixer.Sound('resources/sounds/elephant.mp3')
    pygame.mixer.Sound.play(elephant_sound)
    
    x_shake=random.randint(-2,2)
    y_shake=random.randint(-2,2)
    elephant_sound = pygame.mixer.Sound('resources/sounds/elephant.mp3')
    pygame.mixer.Sound.play(elephant_sound)
    # COLOR = (181, 201, 255)
    COLOR = (0, 0, 0)
    # POSITION = (
    #     engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,
    #     engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake
    # )
    
    TITLE = f"Wave {wave_number+1}"
    if wave_number%4==1:#Falling faster
        angry_animation1=engine.render_text('birthstone',100,TITLE,COLOR)
        angry_animation2=engine.render_text('birthstone',90,f'=plates will fall faster',COLOR)

    if wave_number%4==2:#More pieces
        angry_animation1=engine.render_text('birthstone',100,TITLE,COLOR)
        angry_animation2=engine.render_text('birthstone',90,f'=plates will break in more pieces',COLOR)

    if wave_number%4==3:#More_plates(more frequent)
        angry_animation1=engine.render_text('birthstone',100,TITLE,COLOR)
        angry_animation2=engine.render_text('birthstone',90,f'=plates will fall more frequent',COLOR)

    if wave_number%4==0:#More colors
        angry_animation1=engine.render_text('birthstone',100,TITLE,COLOR)
        angry_animation2=engine.render_text('birthstone',90,f'plates come in different colors',COLOR)
    
    width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
    POSITION = (
        engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,
        # engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake
        100
    )
    engine.render_image(angry_animation1, POSITION)
    width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
    POSITION = (
        engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,
        200
    )
    engine.render_image(angry_animation2,POSITION)
