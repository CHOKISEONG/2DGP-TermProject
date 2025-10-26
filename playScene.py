from pico2d import *
from crowd import Crowd
from shovel_bird import ShovelBird
from map import Map
from musicManager import Music
import time

key_state = set()
miss_handled = False

def enter():
    global bg, player1, music, crowd
    music = Music('sound/120bpm_mainScene.wav', 120)
    music.play(repeat=True)
    bg = Map()
    player1 = ShovelBird(bg)
    crowd = Crowd()

def exit():
    pass

def update():
    beat_index = music.get_current_beat()
    player1.update(beat_index)
    pass

def draw():
    bg.draw()
    player1.draw()
    crowd.draw()

def handle_events():
    global miss_handled
    result, diff = music.check_input_timing()

    # 키 입력 처리
    if result == "Miss":
        if not miss_handled:
            player1.handle_event(key_state)
            key_state.clear()
            miss_handled = True
    else:
        miss_handled = False
        if result == "Good" or result == "Perfect":
            for event in get_events():
                if event.type == SDL_KEYDOWN:
                    key_state.add(event.key)
