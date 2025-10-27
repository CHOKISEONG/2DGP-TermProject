from pico2d import *
from myEnum import *
import math

class Map:
    def __init__(self):
        self.map = load_image('map/desert.png')
        self.img_direction = load_image('UI/PS4_swipes.png')
        self.img_fall = load_image('UI/fall_tile.png')
        self.map_types = [
            [Tile.EMPTY for _ in range(17)]
            for _ in range(18)
        ]
        self.map_pos = [
            ((30 + x * 42.7 + 21) if y % 2 == 1 else (30 + x * 42.7), 75 + y * 28)
            for y in range(18) for x in range(17)
        ]

    def draw(self):
        self.map.draw(400,300,1000,800)
        for y in range(18):
            for x in range(17):
                self.tile_draw(x,y,self.map_types[y][x])

    def tile_draw(self, x, y, tile_type):
        tile_w, tile_h = 32, 16
        draw_w, draw_h = 60,30
        pos_x, pos_y = self.map_pos[y * 17 + x]
        pos_x += draw_w / 2 - tile_w / 2
        pos_y += draw_h / 2 - tile_h / 2
        if tile_type == Tile.EMPTY:
            return
        if tile_type == Tile.UP_LEFT:
            self.img_direction.clip_composite_draw(0, 0, tile_w, tile_h, 2 * math.pi / 3, 'None', pos_x, pos_y, draw_w, draw_h)
        elif tile_type == Tile.UP_RIGHT:
            self.img_direction.clip_composite_draw(0, 0, tile_w, tile_h, math.pi / 4, 'None', pos_x, pos_y, draw_w, draw_h)
        elif tile_type == Tile.DOWN_LEFT:
            self.img_direction.clip_composite_draw(0, 0, tile_w, tile_h, -2 * math.pi / 3, 'None', pos_x, pos_y, draw_w, draw_h)
        elif tile_type == Tile.DOWN_RIGHT:
            self.img_direction.clip_composite_draw(0, 0, tile_w, tile_h, -math.pi / 4, 'None', pos_x, pos_y, draw_w, draw_h)
        elif tile_type == Tile.LEFT:
            self.img_direction.clip_composite_draw(0, 0, tile_w, tile_h, math.pi, 'None', pos_x, pos_y, draw_w, draw_h)
        elif tile_type == Tile.RIGHT:
            self.img_direction.clip_composite_draw(0, 0, tile_w, tile_h, 0, 'None', pos_x, pos_y, draw_w, draw_h)
        elif tile_type == Tile.FALL:
            self.img_fall.clip_composite_draw(0, 0, 108, 108, 0, 'None', pos_x, pos_y, 50, 50)

    def get_tile(self, x, y):
        return self.map_types[x][y]

    def change_tile(self, x, y, tile_type):
        self.map_types[x][y] = tile_type

    def update(self, beat_idx):
        pass
