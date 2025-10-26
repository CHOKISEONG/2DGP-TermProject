from bird import Bird
from pico2d import *

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class ShovelBird(Bird):
    def __init__(self, field):
        super().__init__('birdSheet/shovelBird.png', field)

    def handle_event(self, key_state):
        # 조작 불가능한 상태면 그냥 리턴
        if not self.can_control:
            return

        # 방향 타일 놓기 처리
        if SDLK_j in key_state:
            if SDLK_w in key_state and SDLK_a in key_state:
                self.tile_up_left()
            elif SDLK_w in key_state and SDLK_d in key_state:
                self.tile_up_right()
            elif SDLK_a in key_state and SDLK_s in key_state:
                self.tile_down_left()
            elif SDLK_s in key_state and SDLK_d in key_state:
                self.tile_down_right()
            elif SDLK_a in key_state:
                self.tile_left()
            elif SDLK_d in key_state:
                self.tile_right()

        # 이동 처리
        else:
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
