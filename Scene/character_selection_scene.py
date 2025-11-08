from pico2d import *
import framework
import game_world
from Character.bird import AnimationController
from Character.shovel_bird import ShovelBird
from Character.black_bird import BlackBird
from Character.king_bird import KingBird
from Character.hat_bird import HatBird
from Scene import title_scene
from Scene import play_scene

character_select_scene = None

class characterSelectScene:
    def __init__(self):
        self.start_selected_music = load_wav('Sound/sample/character_select_start.wav')
        self.start_selected_music.play(1)

        self.title_sound_volume = 100

        self.bird1 = AnimationController('Character/image/shovelBird.png')
        self.bird1_pos = [400,0]
        self.bird2 = AnimationController('Character/image/blackBird.png')
        self.bird2_pos = [400, 0]
        self.bird3 = AnimationController('Character/image/kingBird.png')
        self.bird3_pos = [400, 0]
        self.bird4 = AnimationController('Character/image/hatBird.png')
        self.bird4_pos = [400, 0]

        self.rotate = ['down', 'left', 'up', 'right']
        self.rotate_idx = 0

    def update(self, beat_idx):
        title_scene.title_sound.set_volume(self.title_sound_volume)
        if self.title_sound_volume > 0:
            self.title_sound_volume -= 1

    def draw(self):
        self.bird1.draw(*self.bird1_pos)
        self.bird2.draw(*self.bird2_pos)
        self.bird3.draw(*self.bird3_pos)
        self.bird4.draw(*self.bird4_pos)
        if self.bird1_pos[1] < 350:
            self.bird1_pos[1] += 1
            self.bird1_pos[0] -= 0.5
        if self.bird2_pos[1] < 350:
            self.bird2_pos[1] += 1
            self.bird2_pos[0] -= 0.15
        if self.bird3_pos[1] < 350:
            self.bird3_pos[1] += 1
            self.bird3_pos[0] += 0.15
        if self.bird4_pos[1] < 350:
            self.bird4_pos[1] += 1
            self.bird4_pos[0] += 0.5

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