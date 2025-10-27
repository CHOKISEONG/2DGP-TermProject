from bird import Bird
from sample import *
from map import TileType
from enum import Enum
from state_machine import StateMachine

place_tile = lambda e : e[0] == 'PLACE_TILE'
idle = lambda e : e[0] == 'IDLE'
tile_event = lambda e : e[0] == 'TILE_EVENT'
fall = lambda e : e[0] == 'FALL'
resurrection = lambda e : e[0] == 'RESURRECTION'

# 게임의 6방향을 나타내는 Enum (오른쪽 = 1 부터 반시계 방향)
class DIRECTION(Enum):
    NONE = 0
    RIGHT = 1
    UP_RIGHT = 2
    UP_LEFT = 3
    LEFT = 4
    DOWN_LEFT = 5
    DOWN_RIGHT = 6

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

class PlaceTile:

    def __init__(self, bird):
        self.bird = bird
        self.start_time = 0
        self.elapsed_time = 0
        self.one_beat = 120 / self.bird.bpm
        self.dy = 0


    def enter(self, event):
        self.start_time = get_time()
        key_state = event[1]

        # 누른 방향을 바라보게
        if SDLK_w in key_state and SDLK_a in key_state:
            self.bird.img.change_type('up')
            self.bird.dir = DIRECTION.UP_LEFT
        elif SDLK_w in key_state and SDLK_d in key_state:
            self.bird.img.change_type('up')
            self.bird.dir = DIRECTION.UP_RIGHT
        elif SDLK_a in key_state and SDLK_s in key_state:
            self.bird.img.change_type('down')
            self.bird.dir = DIRECTION.DOWN_LEFT
        elif SDLK_s in key_state and SDLK_d in key_state:
            self.bird.img.change_type('down')
            self.bird.dir = DIRECTION.DOWN_RIGHT
        elif SDLK_a in key_state:
            self.bird.img.change_type('left')
            self.bird.dir = DIRECTION.LEFT
        elif SDLK_d in key_state:
            self.bird.img.change_type('right')
            self.bird.dir = DIRECTION.RIGHT

        # 땅 파기
        if SDLK_k in key_state:
            y, x = self.bird.pos_to_row_col(self.bird.pos)
            nx, ny = 0, 0
            if self.bird.dir == DIRECTION.UP_LEFT:
                if y % 2 == 1:
                    ny, nx = y + 1, x
                else:
                    ny, nx = y + 1, x - 1
            elif self.bird.dir == DIRECTION.UP_RIGHT:
                if y % 2 == 1:
                    ny, nx = y + 1, x + 1
                else:
                    ny, nx = y + 1, x
            elif self.bird.dir == DIRECTION.DOWN_LEFT:
                if y % 2 == 1:
                    ny, nx = y - 1, x
                else:
                    ny, nx = y - 1, x - 1
            elif self.bird.dir == DIRECTION.DOWN_RIGHT:
                if y % 2 == 1:
                    ny, nx = y - 1, x + 1
                else:
                    ny, nx = y - 1, x
            elif self.bird.dir == DIRECTION.RIGHT:
                ny, nx = y, x + 1
            elif self.bird.dir == DIRECTION.LEFT:
                ny, nx = y, x - 1
            if 0 <= ny < 18 and 0 <= nx < 17:
                self.bird.field.change_tile(ny, nx, TileType.FALL)
            return

        # 이동타일 깔기
        if SDLK_j in key_state:
            y, x = self.bird.pos_to_row_col(self.bird.pos)
            nx, ny = 0, 0
            if self.bird.dir == DIRECTION.UP_LEFT:
                if y % 2 == 1:
                    ny, nx = y + 1, x
                else:
                    ny, nx = y + 1, x - 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, TileType.UPLEFT)
            elif self.bird.dir == DIRECTION.UP_RIGHT:
                if y % 2 == 1:
                    ny, nx = y + 1, x + 1
                else:
                    ny, nx = y + 1, x
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, TileType.UPRIGHT)
            elif self.bird.dir == DIRECTION.DOWN_LEFT:
                if y % 2 == 1:
                    ny, nx = y - 1, x
                else:
                    ny, nx = y - 1, x - 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, TileType.DOWNLEFT)
            elif self.bird.dir == DIRECTION.DOWN_RIGHT:
                if y % 2 == 1:
                    ny, nx = y - 1, x + 1
                else:
                    ny, nx = y - 1, x
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, TileType.DOWNRIGHT)
            elif self.bird.dir == DIRECTION.RIGHT:
                ny, nx = y, x + 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, TileType.RIGHT)
            elif self.bird.dir == DIRECTION.LEFT:
                ny, nx = y, x - 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, TileType.LEFT)
            return


    def exit(self, event):
        pass


    def do(self):
        self.elapsed_time = get_time() - self.start_time
        if self.elapsed_time < self.one_beat/4:
            self.dy += 2
        elif self.elapsed_time < self.one_beat/2:
            self.dy -= 2
        else:
            self.bird.state_machine.handle_state_event(('IDLE', None))


    def draw(self):
        print(self.dy)
        self.bird.draw(0,self.dy)


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
        self.PLACE_TILE = PlaceTile(self)
        self.TILE_EVENT = TileEvent(self)
        self.FALL = Fall(self)
        self.state_machine = StateMachine(
            self.IDLE,
       {
                self.IDLE: {tile_event: self.TILE_EVENT, place_tile: self.PLACE_TILE},
                self.PLACE_TILE: {idle: self.IDLE, place_tile:self.PLACE_TILE},
                self.TILE_EVENT: {idle: self.IDLE, fall: self.FALL, tile_event: self.TILE_EVENT},
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

    def handle_key(self, key_state):
        if self.state_machine.cur_state == self.TILE_EVENT: return

        # 타일 놓기 처리
        if SDLK_j in key_state or SDLK_k in key_state:
            print('Putting tile')
            self.tile_sound.play()
            self.state_machine.handle_state_event(('PLACE_TILE', key_state))
            return

        # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
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

