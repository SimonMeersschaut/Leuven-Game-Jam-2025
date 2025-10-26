from engine import engine
import random
import pygame

def render_angry_animation(wave_number:int, progress: float):
    x_shake=random.randint(-2,2)
    y_shake=random.randint(-2,2)
    elephant_sound = pygame.mixer.Sound('resources/sounds/elephant.mp3')
    pygame.mixer.Sound.play(elephant_sound)
    if wave_number%4==1:#Falling faster
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',(255,255,255))
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates will fall faster',(255,255,255))
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))

    if wave_number%4==2:#More pieces
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',(255,255,255))
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates will break in more pieces',(255,255,255))
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))

    if wave_number%4==3:#More_plates(more frequent)
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',(255,255,255))
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates will fall more frequent',(255,255,255))
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))

    if wave_number%4==0:#More colors
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',(255,255,255))
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates come in different colors',(255,255,255))
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))


    """
    Progress: getal van nul tot 1. ==> komt overeen met 3 seconden
    """
    # print(wave_number)
    ...