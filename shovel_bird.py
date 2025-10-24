from bird import Bird
from pico2d import *

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class ShovelBird(Bird):
    def __init__(self):
        super().__init__()
        self.img = load_image('birdSheet/shovelBird.png')
        self.area = [
            ((35 + x * 42.7 + 21) if y % 2 == 1 else (35 + x * 42.7), 95 + y * 28)
            for y in range(18) for x in range(17)
        ]
        self.pos = 0

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.area[self.pos])

    def move_up_left(self):
        print('Move up left')
        pass
    def move_up_right(self):
        print('Move up right')
        pass
    def move_down_left(self):
        print('Move down left')
        pass
    def move_down_right(self):
        print('Move down right')
        pass
    def move_left(self):
        print('Move left')
        pass
    def move_right(self):
        print('Move right')
        pass

    def handle_event(self, key_state):
        # 예시: SDLK_w, SDLK_a 등은 pico2d에서 정의되어 있음
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
