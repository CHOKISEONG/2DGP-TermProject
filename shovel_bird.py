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
            ((40 + x * 42.7 + 21) if y % 2 == 1 else (40 + x * 42.7), 95 + y * 28)
            for y in range(18) for x in range(17)
        ]
        self.pos = 0

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.area[self.pos])

    def pos_to_row_col(self, pos):
        return pos // 17, pos % 17

    def row_col_to_pos(self, row, col):
        return row * 17 + col

    def move_down_left(self):
        self.img_type.change_type('down')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y - 1, x
        else:
            ny, nx = y - 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.pos = self.row_col_to_pos(ny, nx)

    def move_down_right(self):
        self.img_type.change_type('down')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y - 1, x + 1
        else:
            ny, nx = y - 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.pos = self.row_col_to_pos(ny, nx)

    def move_up_left(self):
        self.img_type.change_type('up')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y + 1, x
        else:
            ny, nx = y + 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.pos = self.row_col_to_pos(ny, nx)

    def move_up_right(self):
        self.img_type.change_type('up')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y + 1, x + 1
        else:
            ny, nx = y + 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.pos = self.row_col_to_pos(ny, nx)

    def move_left(self):
        self.img_type.change_type('left')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.pos = self.row_col_to_pos(ny, nx)

    def move_right(self):
        self.img_type.change_type('right')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x + 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.pos = self.row_col_to_pos(ny, nx)

    def handle_event(self, key_state):
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
