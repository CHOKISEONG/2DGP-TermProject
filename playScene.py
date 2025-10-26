from pico2d import *
from crowd import Crowd
from shovel_bird import ShovelBird
from map import Map
from musicManager import Music

key_state = set()

def enter():
    global bg, player1, music, crowd
    music = Music('sound/120bpm_mainScene.mp3', 120)
    music.play(repeat=True)
    bg = Map()
    player1 = ShovelBird()
    crowd = Crowd()

def exit():
    pass

def update():
    beat_index = music.get_current_beat() % 4
    player1.update(beat_index)
    pass

def draw():
    bg.draw()
    player1.draw()
    crowd.draw()

def handle_events():
    global bg, player1, music, crowd
    result, diff = music.check_input_timing()

    if result == "Miss":
        player1.handle_event(key_state)
        key_state.clear()
    elif result == "Good" or result == "Perfect":
        for event in get_events():
            if event.type == SDL_KEYDOWN:
                key_state.add(event.key)