from pico2d import *
from Character.bird import *
from Global.myEnum import *

class ShovelBird(Bird):
    def __init__(self, field, num):
        super().__init__('Character/image/shovelBird.png', field, num)
        self.face_ui = load_image('Character/image/shovelBird.png')
        self.pos = 72
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)
        self.time_elapsed = -1
        self.speed = 3
        self.tile_speed = 2

    def update(self, beat_idx):
        self.state_machine.update(beat_idx)
        if self.target_pos != self.current_pos:
            self.current_pos = self.target_pos

    # 입력한 키 처리
    def handle_key(self, key_state):
        # 밟은 타일 이벤트 처리중 or 떨어지는 중에는 키 입력 무시하고 리턴
        if (self.state_machine.cur_state == self.TILE_EVENT
            or self.state_machine.cur_state == self.FALL): return

        if self.player_num == 'player1':
            # 스킬1 - 이동타일 놓기
            if SDLK_f in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                y, x = self.pos_to_row_col(self.pos)
                make_fall_tile(y, x, key_state, self.field)
                return


            # 스킬2 - 낭떠러지 타일 깔기
            if SDLK_g in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                y, x = self.pos_to_row_col(self.pos)
                make_direction_tile(y, x, key_state, self.field)
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_w in key_state or SDLK_a in key_state
                or SDLK_s in key_state or SDLK_d in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

        elif self.player_num == 'player2':
            # 스킬1 - 이동타일 놓기
            if SDLK_PERIOD in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                y, x = self.pos_to_row_col(self.pos)
                make_fall_tile(y, x, key_state, self.field)
                return

            # 스킬2 - 낭떠러지 타일 깔기
            elif SDLK_SLASH in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                y, x = self.pos_to_row_col(self.pos)
                make_direction_tile(y, x, key_state, self.field)
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

def make_direction_tile(y, x, key_state, field):
    look = key_to_direction(key_state)

    nx, ny = 0, 0
    if look == DIRECTION.UP_LEFT:
        if y % 2 == 1:
            ny, nx = y + 1, x
        else:
            ny, nx = y + 1, x - 1
    elif look == DIRECTION.UP_RIGHT:
        if y % 2 == 1:
            ny, nx = y + 1, x + 1
        else:
            ny, nx = y + 1, x
    elif look == DIRECTION.DOWN_LEFT:
        if y % 2 == 1:
            ny, nx = y - 1, x
        else:
            ny, nx = y - 1, x - 1
    elif look == DIRECTION.DOWN_RIGHT:
        if y % 2 == 1:
            ny, nx = y - 1, x + 1
        else:
            ny, nx = y - 1, x
    elif look == DIRECTION.RIGHT:
        ny, nx = y, x + 1
    elif look == DIRECTION.LEFT:
        ny, nx = y, x - 1
    if 0 <= ny < 18 and 0 <= nx < 17:
        field.change_tile(ny, nx, Tile.FALL)

def make_fall_tile(y, x, key_state, field):
    look = key_to_direction(key_state)

    if look == DIRECTION.UP_LEFT:
        if y % 2 == 1:
            ny, nx = y + 1, x
        else:
            ny, nx = y + 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            field.change_tile(ny, nx, Tile.UP_LEFT)
    elif look == DIRECTION.UP_RIGHT:
        if y % 2 == 1:
            ny, nx = y + 1, x + 1
        else:
            ny, nx = y + 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            field.change_tile(ny, nx, Tile.UP_RIGHT)
    elif look == DIRECTION.DOWN_LEFT:
        if y % 2 == 1:
            ny, nx = y - 1, x
        else:
            ny, nx = y - 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            field.change_tile(ny, nx, Tile.DOWN_LEFT)
    elif look == DIRECTION.DOWN_RIGHT:
        if y % 2 == 1:
            ny, nx = y - 1, x + 1
        else:
            ny, nx = y - 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            field.change_tile(ny, nx, Tile.DOWN_RIGHT)
    elif look == DIRECTION.RIGHT:
        ny, nx = y, x + 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            field.change_tile(ny, nx, Tile.RIGHT)
    elif look == DIRECTION.LEFT:
        ny, nx = y, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            field.change_tile(ny, nx, Tile.LEFT)