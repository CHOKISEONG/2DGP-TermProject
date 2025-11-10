from pico2d import *
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
    def handle_key(self, key_state):
        # 밟은 타일 이벤트 처리중 or 떨어지는 중에는 키 입력 무시하고 리턴
        if (self.state_machine.cur_state == self.TILE_EVENT
            or self.state_machine.cur_state == self.FALL): return

        # 타일 놓기 처리
        if SDLK_j in key_state or SDLK_k in key_state:
            self.state_machine.handle_state_event(('PLACE_TILE', key_state))
            return

        if SDLK_c in key_state:
            pass

        # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
        if (SDLK_w in key_state or SDLK_a in key_state
            or SDLK_s in key_state or SDLK_d in key_state):
            self.state_machine.handle_state_event(('MOVE', key_state))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())