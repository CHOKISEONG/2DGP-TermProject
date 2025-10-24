import bird
from pico2d import *

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class ShovelBird(bird.Bird):
    def __init__(self, stage):
        bird.Bird.__init__(self, stage)
        self.img = load_image('birdSheet/shovelBird.png')

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.stage.pos[self.pos])

    def move_up_left(self):
        pass
    def move_up_right(self):
        pass
    def move_down_left(self):
        pass
    def move_down_right(self):
        pass
    def move_left(self):
        pass
    def move_right(self):
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
