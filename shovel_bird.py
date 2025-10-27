from bird import Bird
from sample import *
from state_machine import StateMachine
from myEnum import *

idle = lambda e : e[0] == 'IDLE'
move = lambda e : e[0] == 'MOVE'
place_tile = lambda e : e[0] == 'PLACE_TILE'
tile_event = lambda e : e[0] == 'TILE_EVENT'
fall = lambda e : e[0] == 'FALL'
resurrection = lambda e : e[0] == 'RESURRECTION'

# 가만히 있을 때
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

# 타일 놓는 행동을 할 때
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
            self.bird.look = DIRECTION.UP_LEFT
        elif SDLK_w in key_state and SDLK_d in key_state:
            self.bird.img.change_type('up')
            self.bird.look = DIRECTION.UP_RIGHT
        elif SDLK_a in key_state and SDLK_s in key_state:
            self.bird.img.change_type('down')
            self.bird.look = DIRECTION.DOWN_LEFT
        elif SDLK_s in key_state and SDLK_d in key_state:
            self.bird.img.change_type('down')
            self.bird.look = DIRECTION.DOWN_RIGHT
        elif SDLK_a in key_state:
            self.bird.img.change_type('left')
            self.bird.look = DIRECTION.LEFT
        elif SDLK_d in key_state:
            self.bird.img.change_type('right')
            self.bird.look = DIRECTION.RIGHT

        # 땅 파기
        if SDLK_k in key_state:
            y, x = self.bird.pos_to_row_col(self.bird.pos)
            nx, ny = 0, 0
            if self.bird.look == DIRECTION.UP_LEFT:
                if y % 2 == 1:
                    ny, nx = y + 1, x
                else:
                    ny, nx = y + 1, x - 1
            elif self.bird.look == DIRECTION.UP_RIGHT:
                if y % 2 == 1:
                    ny, nx = y + 1, x + 1
                else:
                    ny, nx = y + 1, x
            elif self.bird.look == DIRECTION.DOWN_LEFT:
                if y % 2 == 1:
                    ny, nx = y - 1, x
                else:
                    ny, nx = y - 1, x - 1
            elif self.bird.look == DIRECTION.DOWN_RIGHT:
                if y % 2 == 1:
                    ny, nx = y - 1, x + 1
                else:
                    ny, nx = y - 1, x
            elif self.bird.look == DIRECTION.RIGHT:
                ny, nx = y, x + 1
            elif self.bird.look == DIRECTION.LEFT:
                ny, nx = y, x - 1
            if 0 <= ny < 18 and 0 <= nx < 17:
                self.bird.field.change_tile(ny, nx, Tile.FALL)
            return

        # 이동타일 깔기
        if SDLK_j in key_state:
            y, x = self.bird.pos_to_row_col(self.bird.pos)
            nx, ny = 0, 0
            if self.bird.look == DIRECTION.UP_LEFT:
                if y % 2 == 1:
                    ny, nx = y + 1, x
                else:
                    ny, nx = y + 1, x - 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, Tile.UP_LEFT)
            elif self.bird.look == DIRECTION.UP_RIGHT:
                if y % 2 == 1:
                    ny, nx = y + 1, x + 1
                else:
                    ny, nx = y + 1, x
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, Tile.UP_RIGHT)
            elif self.bird.look == DIRECTION.DOWN_LEFT:
                if y % 2 == 1:
                    ny, nx = y - 1, x
                else:
                    ny, nx = y - 1, x - 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, Tile.DOWN_LEFT)
            elif self.bird.look == DIRECTION.DOWN_RIGHT:
                if y % 2 == 1:
                    ny, nx = y - 1, x + 1
                else:
                    ny, nx = y - 1, x
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, Tile.DOWN_RIGHT)
            elif self.bird.look == DIRECTION.RIGHT:
                ny, nx = y, x + 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, Tile.RIGHT)
            elif self.bird.look == DIRECTION.LEFT:
                ny, nx = y, x - 1
                if 0 <= ny < 18 and 0 <= nx < 17:
                    self.bird.field.change_tile(ny, nx, Tile.LEFT)
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

# 이동키 처리
class Move:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = get_time()

    def enter(self, event):
        self.start_time = get_time()
        key_state = event[1]
        # 누른 방향을 바라보게
        if SDLK_w in key_state and SDLK_a in key_state:
            self.bird.img.change_type('up')
            self.bird.look = DIRECTION.UP_LEFT
        elif SDLK_w in key_state and SDLK_d in key_state:
            self.bird.img.change_type('up')
            self.bird.look = DIRECTION.UP_RIGHT
        elif SDLK_a in key_state and SDLK_s in key_state:
            self.bird.img.change_type('down')
            self.bird.look = DIRECTION.DOWN_LEFT
        elif SDLK_s in key_state and SDLK_d in key_state:
            self.bird.img.change_type('down')
            self.bird.look = DIRECTION.DOWN_RIGHT
        elif SDLK_a in key_state:
            self.bird.img.change_type('left')
            self.bird.look = DIRECTION.LEFT
        elif SDLK_d in key_state:
            self.bird.img.change_type('right')
            self.bird.look = DIRECTION.RIGHT
        self.bird.move(self.bird.look)

    def exit(self, event):
        pass
    def do(self):
        self.bird.state_machine.handle_state_event(('IDLE', None))

    def draw(self):
        self.bird.img.draw()

# 특수타일을 밟을 때
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
        # event[1] = 밟은 타일의 타입, event[2] = 이동할 칸 수
        self.type = event[1]
        self.time_left = self.speed = event[2]
        self.speed += 1
        self.time_left = self.speed
        self.bird.look = tile_to_direction(self.type)

    def exit(self, event):
        pass

    def do(self):
        # time_left가 다 소비되면 다시 움직일 수 있는 상태로 전환
        if self.time_left == 0: self.bird.state_machine.handle_state_event(('IDLE', None))

        if get_time() - self.start_time > 1 / self.speed:
            self.start_time = get_time()
            self.bird.move(self.bird.look)
            self.dir_idx = (self.dir_idx + 1) % len(self.dir)
            new_direction = self.dir[self.dir_idx]
            self.bird.img.change_type(new_direction)
            self.time_left -= 1

        # 방향 타일을 밟은 경우 상태 재진입
        current_tile = self.bird.field.get_tile(*self.bird.get_pos())
        if current_tile in (Tile.LEFT, Tile.RIGHT, Tile.UP_LEFT, Tile.UP_RIGHT, Tile.DOWN_LEFT, Tile.DOWN_RIGHT):
            self.bird.state_machine.handle_state_event(('TILE_EVENT', current_tile, self.speed))

    def draw(self):
        self.bird.img.draw()

# 맵에서 떨어질 때
class Fall:

    def __init__(self, bird):
        self.bird = bird
        self.start_time = 0

    def enter(self, event):
        self.start_time = get_time()


    def exit(self, event):
        pass
    def do(self):
        if get_time() - self.start_time > 0.3:
            self.bird.img.update()
        self.bird.state_machine.handle_state_event(('IDLE',None))
    def draw(self):
        self.bird.img.draw()


class ShovelBird(Bird):
    def __init__(self, field):
        super().__init__('birdSheet/shovelBird.png', field)
        self.tile_sound = Sample('sound/tileSound.mp3')
        self.time_elapsed = -1
        self.speed = 3
        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.PLACE_TILE = PlaceTile(self)
        self.TILE_EVENT = TileEvent(self)
        self.FALL = Fall(self)
        self.state_machine = StateMachine(
            self.IDLE,
       {
                self.IDLE: {tile_event: self.TILE_EVENT, place_tile: self.PLACE_TILE, move: self.MOVE},
                self.MOVE: {move: self.MOVE, idle: self.IDLE, tile_event: self.TILE_EVENT, fall: self.FALL},
                self.PLACE_TILE: {idle: self.IDLE, place_tile:self.PLACE_TILE},
                self.TILE_EVENT: {idle: self.IDLE, fall: self.FALL, tile_event: self.TILE_EVENT},
                self.FALL: {resurrection: self.IDLE}
            }
        )

    def update(self, beat_idx):
        if self.target_pos != self.current_pos:
            self.current_pos = self.target_pos

        # 이동 타일 밟는거 처리
        if self.time_elapsed != beat_idx:
            current_tile = self.field.get_tile(*self.get_pos())
            if current_tile in (Tile.LEFT, Tile.RIGHT, Tile.UP_LEFT,
                            Tile.UP_RIGHT, Tile.DOWN_LEFT, Tile.DOWN_RIGHT):
                self.speed += 1
                self.state_machine.handle_state_event(('TILE_EVENT', current_tile, self.speed))
            self.time_elapsed = beat_idx

        self.state_machine.update()

    # 입력한 키 처리
    def handle_key(self, key_state):
        if (self.state_machine.cur_state == self.TILE_EVENT
            or self.state_machine.cur_state == self.FALL): return

        # 타일 놓기 처리
        if SDLK_j in key_state or SDLK_k in key_state:
            print('Putting tile')
            self.tile_sound.play()
            self.state_machine.handle_state_event(('PLACE_TILE', key_state))
            return

        # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
        if (SDLK_w in key_state or SDLK_a in key_state
            or SDLK_s in key_state or SDLK_d in key_state):
            print('Move')
            self.state_machine.handle_state_event(('MOVE', key_state))

