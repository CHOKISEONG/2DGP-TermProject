from map import *

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

    def draw(self, x, y):
        self.img.clip_draw(*self.types[self.current_type][self.frame], x, y)

class Bird:
    def __init__(self, img_path, field : Map):
        self.img = AnimationController('birdSheet/shovelBird.png')
        self.field: Map = field
        self.bpm = 120
        self.area = [
            ((40 + x * 42.7 + 21) if y % 2 == 1 else (40 + x * 42.7), 95 + y * 28)
            for y in range(18) for x in range(17)
        ]
        self.pos = 0
        self.current_pos = [self.area[self.pos][0], self.area[self.pos][1]]
        self.target_pos = list(self.current_pos)
        self.dir = 0 # 캐릭터가 이동한 방향쪽 각도를 나타냄 (ex: 왼쪽 위 이동하면 dir은 120)

        self.move_speed = 0.02
        self.last_beat_idx = -1

    def draw(self):
        x, y = self.current_pos
        self.img.draw(x,y)

    def get_pos(self):
        row, col = self.pos_to_row_col(self.pos)
        return row, col

    def pos_to_row_col(self, pos):
        return pos // 17, pos % 17

    def row_col_to_pos(self, row, col):
        return row * 17 + col

    def move(self, direction):
        if direction == TileType.UPLEFT:
            self.move_up_left()
        elif direction == TileType.UPRIGHT:
            self.move_up_right()
        elif direction == TileType.DOWNLEFT:
            self.move_down_left()
        elif direction == TileType.DOWNRIGHT:
            self.move_down_right()
        elif direction == TileType.LEFT:
            self.move_left()
        elif direction == TileType.RIGHT:
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

    def move_left(self):
        self.img.change_type('left')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 0
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])

    def move_right(self):
        self.img.change_type('right')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x + 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.dir = 180
            new_pos = self.row_col_to_pos(ny, nx)
            self.pos = new_pos
            self.target_pos = list(self.area[new_pos])

    def tile_up_left(self):
        self.img.change_type('up')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y + 1, x
        else:
            ny, nx = y + 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.UPLEFT)

    def tile_up_right(self):
        self.img.change_type('up')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y + 1, x + 1
        else:
            ny, nx = y + 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.UPRIGHT)

    def tile_down_left(self):
        self.img.change_type('down')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y - 1, x
        else:
            ny, nx = y - 1, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.DOWNLEFT)

    def tile_down_right(self):
        self.img.change_type('down')
        y, x = self.pos_to_row_col(self.pos)
        if y % 2 == 1:
            ny, nx = y - 1, x + 1
        else:
            ny, nx = y - 1, x
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.DOWNRIGHT)

    def tile_left(self):
        self.img.change_type('left')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x - 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.LEFT)

    def tile_right(self):
        self.img.change_type('right')
        y, x = self.pos_to_row_col(self.pos)
        ny, nx = y, x + 1
        if 0 <= ny < 18 and 0 <= nx < 17:
            self.field.change_tile(ny, nx, TileType.RIGHT)
