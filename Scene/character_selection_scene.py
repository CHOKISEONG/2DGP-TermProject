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
        self.delay = 0.1
        self.time = 0.0
        self.delay_growth = 0.02
        self.max_delay = 0.9

    def update(self, beat_idx):
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

        self.time += 0.01
        if self.time < self.delay:
            return

        self.rotate_idx = (self.rotate_idx + 1) % len(self.rotate)
        new_direction = self.rotate[self.rotate_idx]
        self.bird1.change_type(new_direction)
        self.bird2.change_type(new_direction)
        self.bird3.change_type(new_direction) # kingBird 스프라이트 고치기
        self.bird4.change_type(new_direction)

        self.time = 0.0
        self.delay = min(self.max_delay, self.delay + self.delay_growth)

    def draw(self):
        self.bird1.draw(*self.bird1_pos)
        self.bird2.draw(*self.bird2_pos)
        self.bird3.draw(*self.bird3_pos)
        self.bird4.draw(*self.bird4_pos)

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