from pico2d import *
from crowd import Crowd
from black_bird import BlackBird
from shovel_bird import ShovelBird
from map import Map
from musicManager import Music

key_state = set()

def enter():
    global bg, player1, music, crowd
    music = Music('sound/120bpm_mainScene.mp3', 120)
    music.play(repeat=True)
    bg = Map()
    player1 = ShovelBird(bg)
    crowd = Crowd()

def exit():
    pass

def update():
    pass

def draw():
    bg.draw()
    player1.draw()
    crowd.draw()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_MOUSEBUTTONDOWN:
            mx, my = event.x, event.y
            print(f"x : {mx} y : {my}")