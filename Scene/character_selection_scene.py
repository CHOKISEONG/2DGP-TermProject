from statistics import stdev

from encodings.punycode import selective_find

from pico2d import *
import framework
import game_world
from Character.bird import AnimationController
from Scene import title_scene
from Scene import play_scene

character_select_scene = None
player1_character = None
player2_character = None

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

        self.size = [50,50]
        self.ds = [1.0,1.0,1.0,1.0]

    # i가 0~3 까지 4개의 캐릭터가 마우스랑 겹치는지 확인해서 사이즈 증가
    def isSelected(self, mouse_x, mouse_y, x, y, i):
        half_w = self.size[0] * self.ds[i] / 3.0
        half_h = self.size[1] * self.ds[i] / 3.0
        bx, by = x, y
        if (bx - half_w) <= mouse_x <= (bx + half_w) and (by - half_h) <= mouse_y <= (by + half_h):
            self.ds[i] = 1.2
            return True
        else:
            self.ds[i] = 1.0
            return False

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
            self.size[0] += 0.3
            self.size[1] += 0.3

        self.time += 0.01
        if self.time < self.delay:
            return

        if self.bird4_pos[1] < 350:
            self.rotate_idx = (self.rotate_idx + 1) % len(self.rotate)
            new_direction = self.rotate[self.rotate_idx]
            self.bird1.change_type(new_direction)
            self.bird2.change_type(new_direction)
            self.bird3.change_type(new_direction) # kingBird 스프라이트 고치기
            self.bird4.change_type(new_direction)
        else:
            self.bird1.change_type('down')
            self.bird2.change_type('down')
            self.bird3.change_type('down')
            self.bird4.change_type('down')

        self.time = 0.0
        self.delay = min(self.max_delay, self.delay + self.delay_growth)

    def draw(self):
        self.bird1.draw(*self.bird1_pos, self.size[0] * self.ds[0], self.size[1] * self.ds[0])
        self.bird2.draw(*self.bird2_pos, self.size[0] * self.ds[1], self.size[1] * self.ds[1])
        self.bird3.draw(*self.bird3_pos, self.size[0] * self.ds[2], self.size[1] * self.ds[2])
        self.bird4.draw(*self.bird4_pos, self.size[0] * self.ds[3], self.size[1] * self.ds[3])

    def finish(self):
        del self.start_selected_music

def init():
    print('character_selection_scene init')
    global character_select_scene, select_sound, select_sound2
    select_sound = load_wav('Sound/sample/select_sound.wav')
    select_sound2 = load_wav('Sound/sample/select_sound2.wav')
    character_select_scene = characterSelectScene()
    game_world.add_object(character_select_scene)


def finish():
    character_select_scene.finish()
    pass

def handle_events():
    global character_select_scene, player1_character, player2_character
    if character_select_scene.bird1_pos[1] < 350:
        return
    # 둘 다 캐릭터 고르기 완료하면 마우스 입력 안 받게
    if player1_character is not None and player2_character is not None:
        framework.change_mode(play_scene)
        return

    event_list = get_events()
    for event in event_list:
        mouse_x, mouse_y = event.x, get_canvas_height() - event.y
        scene = character_select_scene
        if event.type == SDL_QUIT:
            framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            scene.isSelected(mouse_x, mouse_y, *scene.bird1_pos, 0)
            scene.isSelected(mouse_x, mouse_y, *scene.bird2_pos, 1)
            scene.isSelected(mouse_x, mouse_y, *scene.bird3_pos, 2)
            scene.isSelected(mouse_x, mouse_y, *scene.bird4_pos, 3)
        elif event.type == SDL_MOUSEBUTTONDOWN:
            scene = character_select_scene
            if scene.isSelected(mouse_x, mouse_y, *scene.bird1_pos, 0):
                if player1_character is None:
                    player1_character = 'shovelBird'
                    select_sound.play(1)
                elif player1_character == 'shovelBird':
                    return
                else:
                    player2_character = 'shovelBird'
                    select_sound2.play(1)
            elif scene.isSelected(mouse_x, mouse_y, *scene.bird2_pos, 1):
                if player1_character is None:
                    player1_character = 'blackBird'
                    select_sound.play(1)
                elif player1_character == 'blackBird':
                    return
                else:
                    player2_character = 'blackBird'
                    select_sound2.play(1)
            elif scene.isSelected(mouse_x, mouse_y, *scene.bird3_pos, 2):
                if player1_character is None:
                    player1_character = 'kingBird'
                    select_sound.play(1)
                elif player1_character == 'kingBird':
                    return
                else:
                    player2_character = 'kingBird'
                    select_sound2.play(1)
            elif scene.isSelected(mouse_x, mouse_y, *scene.bird4_pos, 3):
                if player1_character is None:
                    player1_character = 'hatBird'
                    select_sound.play(1)
                elif player1_character == 'hatBird':
                    return
                else:
                    player2_character = 'hatBird'
                    select_sound2.play(1)



def update():
    game_world.update(0)

def draw():
    clear_canvas()
    game_world.render()
    print(f'ch1: {player1_character}, ch2: {player2_character}')
    update_canvas()

def pause():
    print('hi')
def resume():
    print('bye')