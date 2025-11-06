import random, math
from pico2d import *

def get_random_pos():
    points = [(5, 20), (790, 20), (790, 595), (5, 595)]
    edges = [
        (points[1], points[2]),
        (points[2], points[3]),
        (points[3], points[0]),
    ]
    edge = random.choice(edges)
    (x1, y1), (x2, y2) = edge
    t = random.random()
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t
    return x, y

def get_random_pos_title():
    points = [(5, 60),(200, 30),(400, 20),(600, 30), (795, 60)]
    edges = [ (points[0], points[1])
              , (points[1], points[2])
              ,(points[2], points[3])
              ,(points[3], points[4])]
    edge = random.choice(edges)
    (x1, y1), (x2, y2) = edge
    t = random.random()
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t
    return x, y

class Crowd:
    bird_names = ["budgie", "cockatiel", "duck", "parrot", "robin", "sparrow", "toucan"]

    def __init__(self, str):
        self.images = {name: load_image(f"Character/image/{name.capitalize()}.png") for name in self.bird_names}
        self.positions = {name: [get_random_pos() for _ in range(15)] for name in self.bird_names}
        if str == 'title':
            self.positions = {name: [get_random_pos_title() for _ in range(15)] for name in self.bird_names}
        self.w, self.h = 48, 48
        self.cx, self.cy = 400, 300  # 중앙 좌표
        self.last_beat_idx = -1
        self.size = 1

    def update(self, beat_idx):
        if self.last_beat_idx != beat_idx:
            self.size = 1.1 if self.size == 1 else 1
            self.last_beat_idx = beat_idx

    def draw(self):
        for i in range(15):
            for name in self.bird_names:
                img = self.images[name]
                x, y = self.positions[name][i]
                dx = self.cx - x
                dy = self.cy - y
                rad = math.atan2(dy, dx) + math.pi

                if x < 400:
                    flip = 'v'
                else:
                    flip = 'none'

                img.clip_composite_draw(
                    0, 0, self.w, self.h,
                    rad, flip,
                    x, y,
                    self.w * self.size, self.h * self.size
                )

    def draw_title(self, cx = 400, cy = 300):
        for i in range(15):
            for name in self.bird_names:
                img = self.images[name]
                x, y = self.positions[name][i]

                dx = cx - x
                dy = cy - y
                rad = math.atan2(dy, dx) + math.pi

                if x < 400:
                    flip = 'v'
                else:
                    flip = 'none'

                img.clip_composite_draw(
                    0, 0, self.w, self.h,
                    rad, flip,
                    x, y,
                    140 * self.size, 140 * self.size
                )
