import pygame
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
    global bg, player1, music, crowd
    result, diff = music.check_input_timing()
    if result == "Miss":
        key_state.clear()

    for event in get_events():
        if event.type == SDL_KEYDOWN:
                key_state.add(event.key)

    player1.handle_event(key_state)