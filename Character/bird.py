from map.map import *
from state_machine import StateMachine

idle = lambda e : e[0] == 'IDLE'
move = lambda e : e[0] == 'MOVE'
place_tile = lambda e : e[0] == 'PLACE_TILE'
tile_event = lambda e : e[0] == 'TILE_EVENT'
fall = lambda e : e[0] == 'FALL'

class AnimationController:
    def __init__(self, img_path):
        self.img = load_image(img_path)         # 이미지
        self.frame = 0                          # 현재 프레임
        self.width, self.height = 60, 60        # 스프라이트의 가로,세로
        self.types = {
            'down': [(8, 240, self.width, self.height), (8, 160, self.width, self.height),
                     (88, 240, self.width, self.height), (88, 160, self.width, self.height)],
            'left': [(8, 0, self.width, self.height), (88, 0, self.width, self.height),
                     (8, 0, self.width, self.height), (88, 0, self.width, self.height)],
            'right': [(248, 240, self.width, self.height), (248, 160, self.width, self.height),
                      (248, 80, self.width, self.height), (248, 0, self.width, self.height)],
            'up': [(168, 240, self.width, self.height), (168, 160, self.width, self.height),
                   (8, 80, self.width, self.height), (88, 80, self.width, self.height)],
        }
        self.current_type = 'right'
        self.count = 0

    def update(self):
        self.count += 1
        self.frame = self.count % len(self.types[self.current_type])

    def change_type(self, direction):
        if direction in self.types:
            self.current_type = direction
            self.frame = 0

    def draw(self, x, y, w=50, h=50):
        self.img.clip_draw(*self.types[self.current_type][self.frame], x, y, w, h)

# 가만히 있을 때
class Idle:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = get_time()
        self.time_elapsed = 0
        self.one_beat = 120 / self.bird.bpm
        self.last_beat_idx = -1

    def enter(self, event):
        self.start_time = get_time()

    def exit(self, event):
        pass

    def do(self, beat_idx):
        if self.last_beat_idx != beat_idx:
            self.bird.img.update()
            current_tile = self.bird.field.get_tile(*self.bird.get_pos())
            if current_tile in (Tile.LEFT, Tile.RIGHT, Tile.UP_LEFT,
                                Tile.UP_RIGHT, Tile.DOWN_LEFT, Tile.DOWN_RIGHT):
                self.bird.tile_speed += 1
                self.bird.state_machine.handle_state_event(('TILE_EVENT', current_tile, self.bird.tile_speed))

            self.last_beat_idx = beat_idx

        current_tile = self.bird.field.get_tile(*self.bird.get_pos())
        if current_tile == Tile.FALL:
            self.bird.state_machine.handle_state_event(('FALL', None))

    def draw(self):
        self.bird.img.draw(*self.bird.current_pos)

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
        self.dy = 0
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


    def do(self, beat_idx):
        self.elapsed_time = get_time() - self.start_time
        if self.elapsed_time < 0.1:
            self.dy += 0.03
        elif self.elapsed_time < 0.2:
            self.dy -= 0.03
        else:
            self.bird.state_machine.handle_state_event(('IDLE', None))


    def draw(self):
        x,y = self.bird.current_pos
        self.bird.img.draw(x,y + self.dy)


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
    def do(self, beat_idx):
        self.bird.state_machine.handle_state_event(('IDLE', None))

    def draw(self):
        self.bird.img.draw(*self.bird.current_pos)


# 특수타일을 밟을 때
class TileEvent:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = get_time()

        # 캐릭터의 회전 애니메이션을 위한 변수
        self.rotate = ['down','left','up','right']
        self.rotate_idx = 0

        self.speed = 0          # 캐릭터의 애니메이션 속도
        self.time_left = 0      # 캐릭터가 움직일 남은 칸 수
        self.last_time_left = 0 # 이전에 이동했으면 그 때 남은 칸 수

    def enter(self, event):
        # event[1] = 밟은 타일의 타입, event[2] = 이동할 칸 수
        self.time_left = self.speed = event[2]
        self.speed += 1
        self.time_left = self.speed
        self.bird.look = tile_to_direction(event[1])

    def exit(self, event):
        pass

    def do(self, beat_idx):
        # time_left가 다 소비되면 다시 움직일 수 있는 상태로 전환
        if self.time_left == 0: self.bird.state_machine.handle_state_event(('IDLE', None))

        if get_time() - self.start_time > 1 / self.speed:
            self.start_time = get_time()
            self.bird.move(self.bird.look)
            self.rotate_idx = (self.rotate_idx + 1) % len(self.rotate)
            new_direction = self.rotate[self.rotate_idx]
            self.bird.img.change_type(new_direction)
            self.time_left -= 1

        # 방향 타일을 밟은 경우 상태 재진입
        current_tile = self.bird.field.get_tile(*self.bird.get_pos())
        if current_tile in (Tile.LEFT, Tile.RIGHT, Tile.UP_LEFT, Tile.UP_RIGHT, Tile.DOWN_LEFT, Tile.DOWN_RIGHT):
            self.bird.state_machine.handle_state_event(('TILE_EVENT', current_tile, self.speed))
        elif current_tile == Tile.FALL:
            self.bird.state_machine.handle_state_event(('FALL', None))

    def draw(self):
        self.bird.img.draw(*self.bird.current_pos)


# 맵에서 떨어질 때
class Fall:
    def __init__(self, bird):
        self.bird = bird
        self.start_time = 0
        self.dir = None
        self.w, self.h = 50, 50

    def enter(self, event):
        self.start_time = get_time()
        self.dir = event[1]
        self.w, self.h = 50, 50

    def exit(self, event):
        pass

    def do(self, beat_idx):
        # 3초동안 떨어지는 애니메이션 재생
        if get_time() - self.start_time < 3.0:
            self.fall_animation()
        else:
            self.bird.teleport(*self.bird.field.get_random_empty_tile())
            self.bird.state_machine.handle_state_event(('IDLE', None))

    def draw(self):
        self.bird.img.draw(*self.bird.current_pos, self.w, self.h )

    def fall_animation(self):
        self.w -= 1
        self.h -= 1
        pass


class Bird:
    def __init__(self, img_path, field : Map):
        self.img = AnimationController(img_path)
        self.field: Map = field
        self.bpm = 120
        self.area = [
            ((40 + x * 42.7 + 21) if y % 2 == 1 else (40 + x * 42.7), 95 + y * 28)
            for y in range(18) for x in range(17)
        ]
        self.pos = 0
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)
        self.look = DIRECTION.NONE

        self.move_speed = 0.05
        self.last_beat_idx = -1

        self.IDLE = Idle(self)
        self.MOVE = Move(self)
        self.PLACE_TILE = PlaceTile(self)
        self.TILE_EVENT = TileEvent(self)
        self.FALL = Fall(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.IDLE:
                    {
                        tile_event: self.TILE_EVENT,
                        place_tile: self.PLACE_TILE,
                        move: self.MOVE,
                        fall: self.FALL
                    },
                self.MOVE:
                    {
                        move: self.MOVE,
                        idle: self.IDLE,
                        tile_event: self.TILE_EVENT
                    },
                self.PLACE_TILE:
                    {
                        idle: self.IDLE,
                        place_tile: self.PLACE_TILE
                    },
                self.TILE_EVENT:
                    {
                        idle: self.IDLE,
                        fall: self.FALL,
                        tile_event: self.TILE_EVENT
                    },
                self.FALL:
                    {
                        idle: self.IDLE
                    }
            }
        )

    def handle_collide(self, name, pos):
        if name == 'bomb':
            distance = math.sqrt(math.pow(self.current_pos[0] - pos[0], 2) +math.pow(self.current_pos[1] - pos[1], 2))
            if distance < 10:
                print ('폭발')

    def get_bb(self):
        return self.current_pos[0] - 5, self.current_pos[1] - 24, self.current_pos[0] + 12, self.current_pos[1] - 4

    def get_pos(self):
        row, col = self.pos_to_row_col(self.pos)
        return row, col

    def pos_to_row_col(self, pos):
        return pos // 17, pos % 17

    def row_col_to_pos(self, row, col):
        return row * 17 + col

    def teleport(self, y, x):
        new_pos = self.row_col_to_pos(y,x)
        self.pos = new_pos
        self.target_pos = list(self.area[new_pos])

    def move(self, direction):
        if direction == DIRECTION.UP_LEFT:
            self.move_up_left()
        elif direction == DIRECTION.UP_RIGHT:
            self.move_up_right()
        elif direction == DIRECTION.DOWN_LEFT:
            self.move_down_left()
        elif direction == DIRECTION.DOWN_RIGHT:
            self.move_down_right()
        elif direction == DIRECTION.LEFT:
            self.move_left()
        elif direction == DIRECTION.RIGHT:
            self.move_right()

    def move_up_left(self):
        self.img.change_type('up')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y + 1, x
        else:
            ny, nx = y + 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 120
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])
        else:
            self.state_machine.handle_state_event(('FALL', DIRECTION.DOWN_RIGHT))

    def move_up_right(self):
        self.img.change_type('up')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y + 1, x + 1
        else:
            ny, nx = y + 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 60
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])
        else:
            self.state_machine.handle_state_event(('FALL', DIRECTION.DOWN_LEFT))

    def move_down_left(self):
        self.img.change_type('down')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y - 1, x
        else:
            ny, nx = y - 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 240
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])
        else:
            self.state_machine.handle_state_event(('FALL', DIRECTION.UP_RIGHT))

    def move_down_right(self):
        self.img.change_type('down')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y - 1, x + 1
        else:
            ny, nx = y - 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 300
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])
        else:
            self.state_machine.handle_state_event(('FALL', DIRECTION.UP_LEFT))

    def move_left(self):
        self.img.change_type('left')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 0
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])
        else:
            self.state_machine.handle_state_event(('FALL', DIRECTION.RIGHT))

    def move_right(self):
        self.img.change_type('right')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x + 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 180
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])
        else:
            self.state_machine.handle_state_event(('FALL', DIRECTION.LEFT))