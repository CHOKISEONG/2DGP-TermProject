from pico2d import *
from Character.crowd import Crowd
from Character.shovel_bird import ShovelBird
from Character.black_bird import BlackBird
from Character.king_bird import KingBird
from Character.hat_bird import HatBird
from map.map import Map
from Sound.musicManager import MusicManager, SfxManager
from Scene import character_selection_scene
from UI.UI_Heart import UI_Heart
import game_world

key_state1 = set()
key_state2 = set()
process_miss = False
is_miss = False

player1 = None
player2 = None

def init():
    global music, player1, player2, bg, crowd, heart_ui, sfx

    bg = Map()
    game_world.add_object(bg, 0)

    if character_selection_scene.player1_character == 'shovelBird':
        player1 = ShovelBird(bg)
    elif character_selection_scene.player1_character == 'blackBird':
        player1 = BlackBird(bg)
    elif character_selection_scene.player1_character == 'kingBird':
        player1 = KingBird(bg)
    elif character_selection_scene.player1_character == 'hatBird':
        player1 = HatBird(bg)

    if character_selection_scene.player2_character == 'shovelBird':
        player2 = ShovelBird(bg)
    elif character_selection_scene.player2_character == 'blackBird':
        player2 = BlackBird(bg)
    elif character_selection_scene.player2_character == 'kingBird':
        player2 = KingBird(bg)
    elif character_selection_scene.player2_character == 'hatBird':
        player2 = HatBird(bg)

    game_world.add_object(player1, 1)
    game_world.add_object(player2, 1)

    crowd = Crowd('play_scene')
    game_world.add_object(crowd, 1)

    heart_ui = UI_Heart()
    game_world.add_object(heart_ui, 2)


    sfx = SfxManager()
    music = MusicManager(120)
    music.play(repeat=True)


def finish():
    pass

def update():
    global process_miss, key_state1, key_state2

    result, diff = music.check_input_timing()

    if result == "Miss":
        if not process_miss:
            player1.handle_key(key_state1, 'player1')
            player2.handle_key(key_state2, 'player2')
            key_state1.clear()
            key_state2.clear()
        process_miss = True
    else:
        process_miss = False

    game_world.update(music.get_current_beat())

def draw():
    game_world.render()

player1_key = [SDLK_w, SDLK_a, SDLK_s, SDLK_d, SDLK_f, SDLK_g]
player2_key = [SDLK_LEFT, SDLK_UP, SDLK_DOWN, SDLK_RIGHT, SDLK_PERIOD, SDLK_SLASH]
def handle_events():
    global sfx, key_state1, key_state2
    for event in get_events():
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                exit()
            elif event.key in player1_key:
                key_state1.add(event.key)
            elif event.key in player2_key:
                key_state2.add(event.key)


def pause():
    pass
def resume():
    pass