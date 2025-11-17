import game_world
from Character.bird import *
from Global.myEnum import *


class KingBird(Bird):
    def __init__(self, field, num):
        super().__init__('Character/image/kingBird.png', field, num)
        self.face_ui = load_image('Character/image/kingBird.png')
        self.pos = 232
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)
        self.img.current_type = 'left'

        self.time_elapsed = -1
        self.speed = 3
        self.tile_speed = 2

        self.skill1_img = load_image('Character/image/Robin.png')
        self.skill1_cur_cooldown = 4
        self.skill1_max_cooldown = 4
        self.skill2_img = load_image('Character/image/Toucan.png')
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
            print('킹버드 플레이어1')
            # 스킬1 - 폭발하는 새 발사
            if SDLK_f in key_state and self.skill1_cur_cooldown >= self.skill1_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                ghost = Ghost(self.look, self.current_pos)
                game_world.add_object(ghost, 2)
                self.skill1_cur_cooldown = 0
                return

            # 스킬2
            elif SDLK_g in key_state and self.skill2_cur_cooldown >= self.skill2_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                # 이름 미정
                skill2 = Skill2(self.look, self.current_pos)
                game_world.add_object(skill2, 2)
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
                ghost = Ghost(self.look, self.current_pos)
                game_world.add_object(ghost, 2)
                self.skill1_cur_cooldown = 0
                return

            # 스킬2
            elif SDLK_SLASH in key_state and self.skill2_cur_cooldown >= self.skill2_max_cooldown:
                self.state_machine.handle_state_event(('SKILL', key_state))
                # 이름 미정
                skill2 = Skill2(self.look, self.current_pos)
                game_world.add_object(skill2, 2)
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
        else:
            self.face_ui.clip_draw(32,263,15,15,750,650,100,100)
        draw_rectangle(*self.get_bb())

class Ghost:
    def __init__(self, look, pos):
        self.img = load_image('Character/image/Robin.png')
        self.look = 0
        self.base_dir = 0
        self.dir = 1
        self.flip = 'none'
        self.size = 30, 30
        self.pos = [pos[0], pos[1]]
        self.speed = 5.0
        self.time = get_time()
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

    def update(self, beat_idx):
        if get_time() - self.time > 5:
            game_world.remove_object(self)

        if get_time() - self.time > 0.5:
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
                game_world.add_object(Explosion(self.pos))
                self.dir = 0

            self.dir += 13

    def draw(self):
        self.img.clip_composite_draw(48,0,48,48,self.look, self.flip, *self.pos, *self.size)

class Explosion:
    def __init__(self, pos):
        self.img = load_image('UI/image/explosion.png')
        self.frame = 0
        self.x, self.y = pos[0], pos[1]
        self.time = get_time()
        game_world.add_collision_pair('bird:explosion', None, self)
        from Scene.play_scene import sfx
        sfx.play('explosion')

    def handle_collision(self, group, other):
        game_world.remove_object(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def update(self, beat_idx):
        if get_time() - self.time > 0.1:
            self.frame += 1
            self.time = get_time()
        if self.frame > 7:
            game_world.remove_object(self)

    def draw(self):
        self.img.clip_draw(self.frame * 32,0, 32, 32,self.x, self.y)
        draw_rectangle(*self.get_bb())

class Skill2:
    def __init__(self, look, pos):
        self.img = load_image('Character/image/Parrot.png')
        self.pos = [pos[0], pos[1]]
        self.size = 45, 45
        self.look = 0
        self.t = 1
        self.length = 1
        self.flip = 'none'
        self.time = get_time()
        game_world.add_collision_pair('bird:explosion', None, self)
        if look == DIRECTION.UP_LEFT:
            self.base_dir = 30
            self.look = -120
            self.flip = 'h'
            self.pos[0] -= 60
        elif look == DIRECTION.UP_RIGHT:
            self.base_dir = -30
            self.look = 120
            self.pos[0] += 60
        elif look == DIRECTION.RIGHT:
            self.base_dir = -90
            self.look = 0
            self.pos[0] += 60
        elif look == DIRECTION.DOWN_RIGHT:
            self.base_dir = -150
            self.look = -120
            self.pos[0] += 60
        elif look == DIRECTION.DOWN_LEFT:
            self.base_dir = -210
            self.look = 120
            self.flip = 'h'
            self.pos[0] -= 60
        else:
            self.base_dir = 90
            self.flip = 'h'
            self.pos[0] -= 60

    def get_bb(self):
        return self.pos[0] - 3, self.pos[1] - 3, self.pos[0] + 3, self.pos[1] + 3

    def handle_collision(self, group, other):
        game_world.remove_object(self)

    def update(self, beat_idx):
        if self.t > 80:
            game_world.remove_object(self)

        self.look -= 0.04
        self.pos = self.get_skill2_line(*self.pos)

    def draw(self):
        self.img.clip_composite_draw(48, 0, 48, 48, self.look, self.flip, *self.pos, *self.size)
        draw_rectangle(*self.get_bb())

    def get_skill2_line(self, x, y):
        a = 1.3
        b = 1
        x += (a - b) * math.cos(self.t) + b * math.cos(self.t * (a/b - 1)) * self.length
        y += (a - b) * math.sin(self.t) - b * math.sin(self.t * (a / b - 1)) * self.length
        self.t += 0.1
        self.length += 0.005
        return x, y