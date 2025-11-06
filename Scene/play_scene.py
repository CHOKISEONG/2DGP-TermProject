from pico2d import *
from Character.crowd import Crowd
from Character.shovel_bird import ShovelBird
from map.map import Map
from Sound.musicManager import MusicManager, SfxManager
from UI.UI_Heart import UI_Heart
import game_world

key_state = set()
is_miss = False

def init():
    global music, player1, bg, crowd, heart_ui, sfx
    music = MusicManager(120)
    sfx = SfxManager()
    music.play(repeat=True)
    bg = Map()
    heart_ui = UI_Heart()
    player1 = ShovelBird(bg)
    crowd = Crowd()

    game_world.add_object(bg, 0)
    game_world.add_object(player1, 1)
    game_world.add_object(crowd, 1)
    game_world.add_object(heart_ui, 2)

def finish():
    del music, player1, bg, crowd, heart_ui

def update():
    game_world.update(music.get_current_beat())

def draw():
    game_world.render()

def handle_events():
    global is_miss, sfx
    result, diff = music.check_input_timing()

    # 키 입력 처리
    if result == "Miss":
        if not is_miss:
            player1.handle_key(key_state)
            key_state.clear()
            is_miss = True
    else:
        is_miss = False
        if result == "Good" or result == "Perfect":
            for event in get_events():
                if event.key == SDLK_ESCAPE:
                    exit()
                if event.type == SDL_KEYDOWN:
                    if event.key == SDLK_j or event.key == SDLK_k:
                        sfx.play('direction_tile_sound')
                    key_state.add(event.key)



def pause():
    pass
def resume():
    pass