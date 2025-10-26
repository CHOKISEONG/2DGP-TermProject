from bird import Bird
from sample import *
from map import TileType

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class ShovelBird(Bird):
    def __init__(self, field):
        super().__init__('birdSheet/shovelBird.png', field)
        self.tile_sound = Sample('sound/tileSound.mp3')

    def handle_event(self, key_state):
        # 조작 불가능한 상태면 그냥 리턴
        if not self.can_control:
            key_state.clear()
            return

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
