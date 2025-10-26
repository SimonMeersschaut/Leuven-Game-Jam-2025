from engine import engine
import random

def render_angry_animation(wave_number:int, progress: float):
    """
    Progress: getal van nul tot 1. ==> komt overeen met 3 seconden
    """
    x_shake=random.randint(-2,2)
    y_shake=random.randint(-2,2)
    COLOR = (0, 0 , 0)
    if wave_number%4==1:#Falling faster
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',COLOR)
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates will fall faster',COLOR)
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))

    if wave_number%4==2:#More pieces
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',COLOR)
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates will break in more pieces',COLOR)
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))

    if wave_number%4==3:#More_plates(more frequent)
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',COLOR)
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates will fall more frequent',COLOR)
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))

    if wave_number%4==0:#More colors
        angry_animation1=engine.render_text('birthstone',100,'Elephant is getting angry!',COLOR)
        width_angry_animation1,length_angry_animation1=angry_animation1.get_size()
        engine.render_image(angry_animation1,(engine.DISPLAY_W/2-width_angry_animation1/2+x_shake,engine.DISPLAY_H/2-0.7*length_angry_animation1+y_shake))
        angry_animation2=engine.render_text('birthstone',90,f'Wave level {wave_number}, plates come in different colors',COLOR)
        width_angry_animation2,length_angry_animation2=angry_animation2.get_size()
        engine.render_image(angry_animation2,(engine.DISPLAY_W/2-width_angry_animation2/2+x_shake,engine.DISPLAY_H/2+0.7*length_angry_animation1+y_shake))
