import random
from pico2d import *
import game_world
from Character.bird import Bird
from state_machine import StateMachine
from Global.myEnum import *

class KingBird(Bird):
    def __init__(self, field):
        super().__init__('Character/image/kingBird.png', field)
        self.pos = 232
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)
        self.img.current_type = 'left'

        self.time_elapsed = -1
        self.speed = 3
        self.tile_speed = 2

    def update(self, beat_idx):
        self.state_machine.update(beat_idx)

        if self.target_pos != self.current_pos:
            self.current_pos = self.target_pos

    # 입력한 키 처리
    def handle_key(self, key_state, who):
        # 밟은 타일 이벤트 처리중 or 떨어지는 중에는 키 입력 무시하고 리턴
        if (self.state_machine.cur_state == self.TILE_EVENT
            or self.state_machine.cur_state == self.FALL): return

        if who == 'player1':
            # 타일 놓기 처리
            if SDLK_f in key_state or SDLK_g in key_state:
                ghost = Ghost(self.look, self.current_pos)
                game_world.add_object(ghost, 2)
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_w in key_state or SDLK_a in key_state
                or SDLK_s in key_state or SDLK_d in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

        elif who == 'player2':
            # 타일 놓기 처리
            if SDLK_PERIOD in key_state or SDLK_SLASH in key_state:
                self.state_machine.handle_state_event(('PLACE_TILE', key_state))
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_LEFT in key_state or SDLK_RIGHT in key_state
                    or SDLK_DOWN in key_state or SDLK_UP in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())



class Ghost:
    def __init__(self, look, pos):
        self.img = load_image('Character/image/Robin.png')
        self.look = 0
        self.base_dir = 0
        self.dir = 1
        self.flip = 'none'
        self.size = 30, 30
        if look == DIRECTION.UP_LEFT:
            self.base_dir = 30
            self.look = -120
            self.flip = 'h'
        elif look == DIRECTION.UP_RIGHT:
            self.base_dir = -30
            self.look = 120
        elif look == DIRECTION.RIGHT:
            self.base_dir = -90
            self.look = 0
        elif look == DIRECTION.DOWN_RIGHT:
            self.base_dir = -150
            self.look = -120
        elif look == DIRECTION.DOWN_LEFT:
            self.base_dir = -210
            self.look = 120
            self.flip = 'h'
        else:
            self.base_dir = 90
            self.flip = 'h'
        self.pos = [pos[0], pos[1]]
        self.speed = 2.0

    def update(self, beat_idx):
        base_angle = math.radians(self.base_dir)
        local_angle = math.radians(self.dir)

        dx = math.cos(local_angle) * self.speed
        dy = math.sin(local_angle) * self.speed

        rotated_dx = dx * math.cos(base_angle) - dy * math.sin(base_angle)
        rotated_dy = dx * math.sin(base_angle) + dy * math.cos(base_angle)

        if 0 < self.dir <= 180:
            self.pos[0] += rotated_dx
            self.pos[1] += rotated_dy
        else:
            from Scene.play_scene import player1, player2
            bomb = Explosion(self.pos)
            game_world.add_object(bomb, 2)
            player1.handle_collide('bomb', self.pos)
            player2.handle_collide('bomb', self.pos)
            self.dir = 0

        self.dir += 3

    def draw(self):
        self.img.clip_composite_draw(48,0,48,48,self.look, self.flip, *self.pos, *self.size)


class Explosion:
    def __init__(self, pos):
        self.img = load_image('UI/image/explosion.png')
        self.frame = 0
        self.idx = 0
        self.pos = [pos[0], pos[1]]

    def update(self, beat_idx):
        if self.idx != beat_idx:
            self.idx = beat_idx
            self.frame += 1
        if self.frame > 7:
            game_world.remove_object(self)

    def draw(self):
        self.img.clip_draw(self.frame * 32,0, 32, 32,*self.pos)
