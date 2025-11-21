from pico2d import *
from Character.bird import Bird
from state_machine import StateMachine
from Global.myEnum import *
import game_world

class HatBird(Bird):
    def __init__(self, field, num):
        super().__init__('Character/image/hatBird.png', field, num)
        self.face_ui = load_image('Character/image/hatBird.png')
        self.pos = 80
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)
        self.img.current_type = 'left'

        self.time_elapsed = -1
        self.speed = 3
        self.tile_speed = 2

        self.skill1_img = load_image('Character/image/hatBird.png')
        self.skill1_cur_cooldown = 3
        self.skill1_max_cooldown = 3
        self.skill2_img = load_image('UI/image/blood_explosion.png')
        self.skill2_cur_cooldown = 3
        self.skill2_max_cooldown = 3
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
            # 스킬1 - 2칸 이동
            if SDLK_f in key_state and self.skill1_cur_cooldown >= self.skill1_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                self.move(self.look)
                self.move(self.look)
                self.skill1_cur_cooldown = 0
                return

            # 스킬2 - 범위 폭발
            elif SDLK_g in key_state and self.skill2_cur_cooldown >= self.skill2_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                from Scene.play_scene import sfx
                sfx.play('fire')
                make_hat_skill(self.current_pos, self.look)
                self.skill2_cur_cooldown = 0
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_w in key_state or SDLK_a in key_state
                or SDLK_s in key_state or SDLK_d in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

        elif self.player_num == 'player2':
            # 스킬1 - 2칸 이동
            if SDLK_PERIOD in key_state and self.skill1_cur_cooldown >= self.skill1_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                self.move(self.look)
                self.move(self.look)
                self.skill1_cur_cooldown = 0
                return

            # 스킬2 - 범위 폭발
            elif SDLK_SLASH in key_state and self.skill2_cur_cooldown >= self.skill2_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                from Scene.play_scene import sfx
                sfx.play('fire')
                make_hat_skill(self.current_pos, self.look)
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
            self.face_ui.clip_draw(32,263,15,15,50,650,100,100)

            if self.skill1_cur_cooldown == self.skill1_max_cooldown:
                self.skill1_img.clip_draw(8, 0, 60, 60, 60, 50, 100, 100)
            else:
                self.skill_font.draw(30, 40, str(self.skill1_max_cooldown - self.skill1_cur_cooldown), (255,255,255))

            if self.skill2_cur_cooldown == self.skill2_max_cooldown:
                self.skill2_img.clip_draw(608, 0, 152, 166, 150, 30, 100, 100)
            else:
                self.skill_font.draw(130, 40, str(self.skill2_max_cooldown - self.skill2_cur_cooldown), (255,255,255))
        else:
            self.face_ui.clip_draw(32,263,15,15,750,650,100,100)

            if self.skill1_cur_cooldown == self.skill1_max_cooldown:
                self.skill1_img.clip_draw(8, 0, 60, 60, 660, 50, 100, 100)
            else:
                self.skill_font.draw(630, 40, str(self.skill1_max_cooldown - self.skill1_cur_cooldown), (255, 255, 255))

            if self.skill2_cur_cooldown == self.skill2_max_cooldown:
                self.skill2_img.clip_draw(608, 0, 152, 166, 750, 30, 100, 100)
            else:
                self.skill_font.draw(730, 40, str(self.skill2_max_cooldown - self.skill2_cur_cooldown), (255, 255, 255))

        draw_rectangle(*self.get_bb())

def make_hat_skill(pos, look):
    if look == DIRECTION.LEFT:
        game_world.add_object(HatSkill((pos[0] - 40, pos[1] - 15)), 2)
        game_world.add_object(HatSkill((pos[0] - 20, pos[1] + 20)), 2)
        game_world.add_object(HatSkill((pos[0] - 20, pos[1] - 50)), 2)
    if look == DIRECTION.RIGHT:
        game_world.add_object(HatSkill((pos[0] + 50, pos[1] - 15)), 2)
        game_world.add_object(HatSkill((pos[0] + 30, pos[1] + 15)), 2)
        game_world.add_object(HatSkill((pos[0] + 30, pos[1] - 45)), 2)
    if look == DIRECTION.DOWN_LEFT:
        game_world.add_object(HatSkill((pos[0] - 40, pos[1] - 15)), 2)
        game_world.add_object(HatSkill((pos[0] - 20, pos[1] - 50)), 2)
        game_world.add_object(HatSkill((pos[0] + 30, pos[1] - 45)), 2)
    if look == DIRECTION.DOWN_RIGHT:
        game_world.add_object(HatSkill((pos[0] - 20, pos[1] - 50)), 2)
        game_world.add_object(HatSkill((pos[0] + 30, pos[1] - 45)), 2)
        game_world.add_object(HatSkill((pos[0] + 50, pos[1] - 15)), 2)
    if look == DIRECTION.UP_LEFT:
        game_world.add_object(HatSkill((pos[0] - 40, pos[1] - 15)), 2)
        game_world.add_object(HatSkill((pos[0] - 20, pos[1] + 20)), 2)
        game_world.add_object(HatSkill((pos[0] + 30, pos[1] + 15)), 2)
    if look == DIRECTION.UP_RIGHT:
        game_world.add_object(HatSkill((pos[0] - 20, pos[1] + 20)), 2)
        game_world.add_object(HatSkill((pos[0] + 50, pos[1] - 15)), 2)
        game_world.add_object(HatSkill((pos[0] + 30, pos[1] + 15)), 2)

class HatSkill:
    def __init__(self, pos):
        self.img = load_image('UI/image/blood_explosion.png')
        self.pos = pos
        self.size = 50, 50
        self.frame = 0
        self.frame_time = get_time()
        self.end_time = get_time()
        game_world.add_collision_pair('bird:explosion', None, self)

    def get_bb(self):
        return self.pos[0] - 3, self.pos[1] - 3, self.pos[0] + 3, self.pos[1] + 3

    def handle_collision(self, group, other):
        game_world.remove_object(self)

    def update(self, beat_idx):
        t = get_time()
        if t - self.end_time > 0.8:
            game_world.remove_object(self)
        if t - self.frame_time> 0.05:
            self.frame += 1
            self.frame_time = t

    def draw(self):
        self.img.clip_draw(self.frame * 152, 0, 152, 166, *self.pos, *self.size)
