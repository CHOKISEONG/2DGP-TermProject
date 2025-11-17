import random

from pico2d import *
from Character.bird import Bird
from state_machine import StateMachine
from Global.myEnum import *
import game_world

class BlackBird(Bird):
    def __init__(self, field, num):
        super().__init__('Character/image/blackBird.png', field, num)
        self.face_ui = load_image('Character/image/blackBird.png')
        self.pos = 208
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)

        self.time_elapsed = -1
        self.speed = 3
        self.tile_speed = 2

        self.skill1 = []
        self.skill1_img = load_image('UI/image/black_skill1.png')
        self.skill1_cur_cooldown = 2
        self.skill1_max_cooldown = 2
        self.skill2_img = load_image('UI/image/speed_up.png')
        self.skill2_cur_cooldown = 6
        self.skill2_max_cooldown = 6
        self.beat_idx = -1

    def update(self, beat_idx):
        self.state_machine.update(beat_idx)

        if self.target_pos != self.current_pos:
            self.current_pos = self.target_pos

        # 스킬 쿨타임 회복용 코드
        if self.beat_idx < beat_idx:
            self.beat_idx = beat_idx
            if self.skill1_cur_cooldown < self.skill1_max_cooldown:
                self.skill1_cur_cooldown += 1
            if self.skill2_cur_cooldown < self.skill2_max_cooldown:
                self.skill2_cur_cooldown += 1

    # 입력한 키 처리
    def handle_key(self, key_state):
        # 밟은 타일 이벤트 처리중 or 떨어지는 중에는 키 입력 무시하고 리턴
        if (self.state_machine.cur_state == self.TILE_EVENT
            or self.state_machine.cur_state == self.FALL): return

        if self.player_num == 'player1':
            # 스킬1
            if SDLK_f in key_state and self.skill1_cur_cooldown >= self.skill1_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                skill = Skill1(self.look, self.current_pos)
                self.skill1.append(skill)
                game_world.add_object(skill, 2)
                self.skill1_cur_cooldown = 0
                return

            # 스킬2
            elif SDLK_g in key_state and self.skill2_cur_cooldown >= self.skill2_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                for skill in self.skill1:
                    skill.increase_speed(self.look)
                self.skill2_cur_cooldown = 0
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_w in key_state or SDLK_a in key_state
                or SDLK_s in key_state or SDLK_d in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

        elif self.player_num == 'player2':
            # 스킬1
            if SDLK_PERIOD in key_state and self.skill1_cur_cooldown >= self.skill1_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                skill = Skill1(self.look, self.current_pos)
                self.skill1.append(skill)
                game_world.add_object(skill, 2)
                self.skill1_cur_cooldown = 0
                return

            # 스킬2
            elif SDLK_SLASH in key_state and self.skill2_cur_cooldown >= self.skill2_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                for skill in self.skill1:
                    skill.increase_speed(self.look)
                self.skill2_cur_cooldown = 0
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_LEFT in key_state or SDLK_RIGHT in key_state
                    or SDLK_DOWN in key_state or SDLK_UP in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

    def draw(self):
        self.state_machine.draw()
        self.hp.draw()
        if self.player_num == 'player1':
            self.face_ui.clip_draw(32, 263, 15, 15, 50, 650, 100, 100)
            if self.skill1_cur_cooldown == self.skill1_max_cooldown:
                self.skill1_img.clip_draw(0, 0, 32, 32, 80, 30, 100, 100)
            else:
                self.skill_font.draw(60, 20, str(self.skill1_max_cooldown - self.skill1_cur_cooldown), (255,255,255))
            if self.skill2_cur_cooldown == self.skill2_max_cooldown:
                self.skill1_img.clip_draw(0, 0, 32, 32, 150, 30, 100, 100)
                self.skill2_img.clip_draw(0, 0, 32, 32, 150, 30, 60, 60)
            else:
                self.skill_font.draw(130, 20, str(self.skill2_max_cooldown - self.skill2_cur_cooldown), (255,255,255))
        else:
            self.face_ui.clip_draw(32,263,15,15,750,650,100,100)
            if self.skill1_cur_cooldown == self.skill1_max_cooldown:
                self.skill1_img.clip_draw(0, 0, 32, 32, 650, 30, 100, 100)
            else:
                self.skill_font.draw(630, 20, str(self.skill1_max_cooldown - self.skill1_cur_cooldown), (255,255,255))
            if self.skill2_cur_cooldown == self.skill2_max_cooldown:
                self.skill1_img.clip_draw(0, 0, 32, 32, 730, 30, 100, 100)
                self.skill2_img.clip_draw(0, 0, 32, 32, 740, 30, 60, 60)
            else:
                self.skill_font.draw(700, 20, str(self.skill2_max_cooldown - self.skill2_cur_cooldown), (255,255,255))

        draw_rectangle(*self.get_bb())

class Skill1:
    def __init__(self, look, pos):
        self.img = load_image('UI/image/black_skill1.png')
        self.pos = [pos[0], pos[1]]
        self.angle = 0
        self.speed = 0
        self.dir = [0,0]
        self.time = get_time()

        game_world.add_collision_pair('bird:explosion', None, self)

        if look == DIRECTION.UP_LEFT:
            self.pos[0] += -17
            self.pos[1] += 15
        elif look == DIRECTION.UP_RIGHT:
            self.pos[0] += 25
            self.pos[1] += 15
        elif look == DIRECTION.RIGHT:
            self.pos[0] += 45
            self.pos[1] += -15
        elif look == DIRECTION.DOWN_RIGHT:
            self.pos[0] += 30
            self.pos[1] += -40
        elif look == DIRECTION.DOWN_LEFT:
            self.pos[0] += -17
            self.pos[1] += -40
        else:
            self.pos[0] += -40
            self.pos[1] += -15

    def get_bb(self):
        return self.pos[0] - 3, self.pos[1] - 3, self.pos[0] + 3, self.pos[1] + 3

    def handle_collision(self, group, other):
        game_world.remove_object(self)

    def update(self, beat_idx):
        self.angle += 1 * self.speed
        self.pos[0] += self.dir[0] * self.speed
        self.pos[1] += self.dir[1] * self.speed
        if self.pos[0] < 0 or self.pos[0] > 800:
            self.dir[0] = -self.dir[0]
        if self.pos[1] < 0 or self.pos[1] > 700:
            self.dir[1] = -self.dir[1]

    def draw(self):
        self.img.clip_composite_draw(0, 0, 32, 32, self.angle, 'not flip', *self.pos, 32, 32)
        draw_rectangle(*self.get_bb())

    def increase_speed(self, look):
        self.speed += 0.1
        if look == DIRECTION.UP_LEFT:
            self.dir = [-5, 5]
        elif look == DIRECTION.UP_RIGHT:
            self.dir = [5,5]
        elif look == DIRECTION.RIGHT:
            self.dir = [5, 0]
        elif look == DIRECTION.DOWN_RIGHT:
            self.dir = [5, -5]
        elif look == DIRECTION.DOWN_LEFT:
            self.dir = [-5, -5]
        else:
            self.dir = [-5, 0]