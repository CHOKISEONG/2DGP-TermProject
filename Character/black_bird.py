from pico2d import *
from Character.bird import Bird
from state_machine import StateMachine
from Global.myEnum import *

class BlackBird(Bird):
    def __init__(self, field, num):
        super().__init__('Character/image/blackBird.png', field, num)
        self.pos = 208
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
            # 스킬1 - 폭발하는 새 발사
            if SDLK_f in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                # 아직 미구현
                return

            # 스킬2
            elif SDLK_g in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                # 아직 미구현
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_w in key_state or SDLK_a in key_state
                or SDLK_s in key_state or SDLK_d in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

        elif self.player_num == 'player2':
            # 스킬1
            if SDLK_PERIOD in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                # 아직 미구현
                return

            # 스킬2
            elif SDLK_SLASH in key_state:
                self.state_machine.handle_state_event(('SKILL', key_state))
                # 아직 미구현
                return

            # 이동 처리 (마지막에 둬서 다른 키 말고 이동키만 눌렀는지 확인함)
            if (SDLK_LEFT in key_state or SDLK_RIGHT in key_state
                    or SDLK_DOWN in key_state or SDLK_UP in key_state):
                self.state_machine.handle_state_event(('MOVE', key_state))

    def draw(self):
        self.state_machine.draw()
        self.hp.draw()
        draw_rectangle(*self.get_bb())