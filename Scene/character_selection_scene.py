from pico2d import *
import framework
import game_world
from Scene import title_scene
from Scene import play_scene

character_select_scene = None

class characterSelectScene:
    def __init__(self):
        self.start_selected_music = load_wav('Sound/sample/character_select_start.wav')
        self.start_selected_music.play(1)

        self.title_sound_volume = 100


    def update(self, beat_idx):
        title_scene.title_sound.set_volume(self.title_sound_volume)
        if self.title_sound_volume > 0:
            self.title_sound_volume -= 1

    def draw(self):
        pass

def init():
    print('character_selection_scene init')
    global character_select_scene
    character_select_scene = characterSelectScene()
    game_world.add_object(character_select_scene)


def finish():
    pass


def handle_events():
    pass


def update():
    game_world.update(0)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()



def pause():
    print('hi')
def resume():
    print('bye')