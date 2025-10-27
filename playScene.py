from pico2d import *
from crowd import Crowd
from shovel_bird import ShovelBird
from map import Map
from musicManager import Music
import game_world
import time

key_state = set()
miss_handled = False

def enter():
    global music, player1, bg, crowd
    music = Music('sound/120bpm_GerudoValley.wav', 120)
    music.play(repeat=True)
    bg = Map()
    player1 = ShovelBird(bg)
    crowd = Crowd()
    game_world.add_object(bg, 0)
    game_world.add_object(player1, 1)
    game_world.add_object(crowd, 1)
    play_time = time.time()

def exit():
    pass

def update():
    beat_index = music.get_current_beat()
    player1.update(beat_index)

def draw():
    game_world.render()

def handle_events():
    global miss_handled
    result, diff = music.check_input_timing()

    # 키 입력 처리
    if result == "Miss":
        if not miss_handled:
            player1.handle_key(key_state)
            key_state.clear()
            miss_handled = True
    else:
        miss_handled = False
        if result == "Good" or result == "Perfect":
            for event in get_events():
                if event.type == SDL_KEYDOWN:
                    key_state.add(event.key)
