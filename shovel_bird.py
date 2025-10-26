from bird import Bird
from sample import *
from map import TileType
from state_machine import StateMachine

can_move = lambda e : e[0] == 'CAN_MOVE'
tile_event = lambda e : e[0] == 'TILE_EVENT'
fall = lambda e : e[0] == 'FALL'
resurrection = lambda e : e[0] == 'RESURRECTION'

class Idle:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = get_time()
        self.elapsed_time = 0
        self.one_beat = 120 / self.bird.bpm
    def enter(self, event):
        pass
    def exit(self, event):
        pass
    def do(self):
        self.elapsed_time = get_time() - self.start_time
        if self.elapsed_time > self.one_beat/4:
            self.start_time = get_time()
            self.bird.img.update()
    def draw(self):
        self.bird.img.draw()

class Move:
    def __init__(self, bird):
        self.bird = bird
    def enter(self, event):
        pass
    def exit(self, event):
        pass
    def do(self):
        self.bird.img.update()
    def draw(self):
        self.bird.img.draw()

class TileEvent:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = get_time()
        self.dir = ['down','left','up','right']
        self.dir_idx = 0
        self.speed = 0
        self.time_left = 0
        self.type = None
        self.tile_signal = None

    def enter(self, event):
        self.type = event[1]
        self.time_left = self.speed = event[2]

    def exit(self, event):
        pass

    def do(self):
        print(self.time_left)
        if self.time_left == 0: self.bird.state_machine.handle_state_event(('CAN_MOVE', None))

        current_tile = self.bird.field.get_tile(*self.bird.get_pos())
        if current_tile in (TileType.LEFT, TileType.RIGHT, TileType.UPLEFT,TileType.UPRIGHT, TileType.DOWNLEFT, TileType.DOWNRIGHT):
            if self.tile_signal:
                self.type = current_tile
                self.speed += 1
                self.time_left = self.speed
                self.tile_signal = False
        else:
            self.tile_signal = True

        if get_time() - self.start_time > 1 / self.speed:
            self.bird.move(self.type)
            self.dir_idx = (self.dir_idx + 1) % len(self.dir)
            new_direction = self.dir[self.dir_idx]
            self.bird.img.change_type(new_direction)
            self.start_time = get_time()
            self.time_left -= 1

    def draw(self):
        self.bird.img.draw()

class Fall:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = get_time()
    def enter(self, event):

        pass
    def exit(self, event):
        pass
    def do(self):
        if get_time() - self.start_time > 0.3:
            self.bird.img.update()
        self.bird.state_machine.handle_state_event(('CAN_MOVE',None))
    def draw(self):
        self.bird.img.draw()

class ShovelBird(Bird):
    def __init__(self, field):
        super().__init__('birdSheet/shovelBird.png', field)
        self.tile_sound = Sample('sound/tileSound.mp3')
        self.time_elapsed = -1
        self.speed = 3
        self.IDLE = Idle(self)
        self.TILE_EVENT = TileEvent(self)
        self.FALL = Fall(self)
        self.state_machine = StateMachine(
            self.IDLE,
       {
                self.IDLE: {tile_event: self.TILE_EVENT},
                self.TILE_EVENT: {can_move: self.IDLE, fall: self.FALL, tile_event: self.TILE_EVENT},
                self.FALL: {resurrection: self.IDLE}
            }
        )

    def update(self, beat_index):
        for i in range(2):
            diff = self.target_pos[i] - self.current_pos[i]
            if abs(diff) > 0.5:
                self.current_pos[i] += diff * self.move_speed
            else:
                self.current_pos[i] = self.target_pos[i]

        # 이동 타일 밟는거 처리
        if self.time_elapsed != beat_index:
            current_tile = self.field.get_tile(*self.get_pos())
            if current_tile in (TileType.LEFT, TileType.RIGHT, TileType.UPLEFT,
                            TileType.UPRIGHT, TileType.DOWNLEFT, TileType.DOWNRIGHT):
                self.speed += 1
                self.state_machine.handle_state_event(('TILE_EVENT', current_tile, self.speed))
            self.time_elapsed = beat_index

        self.state_machine.update()

    def handle_event(self, key_state):

        # 낭떠러지 타일 놓기 처리
        if SDLK_k in key_state:
            print('Putting fall tile')
            self.put_fall_tile()
            return

        # 방향 타일 놓기 처리
        if SDLK_j in key_state:
            print('Putting dir tile')
            self.tile_sound.play()
            # 왜 왼쪽 오른쪽 방향이 각도 반대인지 모르겠음 일단 작동 제대로 됨
            if self.dir == 180:
                self.tile_right()
            elif self.dir == 60:
                self.tile_up_right()
            elif self.dir == 120:
                self.tile_up_left()
            elif self.dir == 0:
                self.tile_left()
            elif self.dir == 240:
                self.tile_down_left()
            elif self.dir == 300:
                self.tile_down_right()
            return

        # 이동 처리
        if SDLK_w in key_state and SDLK_a in key_state:
            self.move_up_left()
        elif SDLK_w in key_state and SDLK_d in key_state:
            self.move_up_right()
        elif SDLK_a in key_state and SDLK_s in key_state:
            self.move_down_left()
        elif SDLK_s in key_state and SDLK_d in key_state:
            self.move_down_right()
        elif SDLK_a in key_state:
            self.move_left()
        elif SDLK_d in key_state:
            self.move_right()

    def put_fall_tile(self):
        y, x = self.pos_to_row_col(self.pos)
        nx, ny = 0, 0
        if self.dir == 120:
            if y % 2 == 1:
                ny, nx = y + 1, x
            else:
                ny, nx = y + 1, x - 1
        elif self.dir == 60:
            if y % 2 == 1:
                ny, nx = y + 1, x + 1
            else:
                ny, nx = y + 1, x
        elif self.dir == 240:
            if y % 2 == 1:
                ny, nx = y - 1, x
            else:
                ny, nx = y - 1, x - 1
        elif self.dir == 300:
            if y % 2 == 1:
                ny, nx = y - 1, x + 1
            else:
                ny, nx = y - 1, x
        elif self.dir == 180:
            ny, nx = y, x + 1
        elif self.dir == 0:
            ny, nx = y, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.FALL)
