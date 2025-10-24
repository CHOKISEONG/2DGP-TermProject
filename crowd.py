import random
from pico2d import *

def get_random_pos():
    points = [(5, 15), (790, 15), (790, 560), (5, 560)]
    edges = [
        (points[0], points[1]),
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

class Crowd:

    def __init__(self):
        self.budgie = load_image("birdSheet/Budgie.png")
        self.cockatiel = load_image("birdSheet/Cockatiel.png")
        self.duck = load_image("birdSheet/Duck.png")
        self.parrot = load_image("birdSheet/Parrot.png")
        self.robin = load_image("birdSheet/Robin.png")
        self.sparrow = load_image("birdSheet/Sparrow.png")
        self.toucan = load_image("birdSheet/Toucan.png")

        self.look_left = (0,0,48,48)
        self.look_right = (48,0,48,48)

        self.budgie_pos = [get_random_pos() for _ in range(20)]
        self.cockatiel_pos = [get_random_pos() for _ in range(20)]
        self.duck_pos = [get_random_pos() for _ in range(20)]
        self.parrot_pos = [get_random_pos() for _ in range(20)]
        self.robin_pos = [get_random_pos() for _ in range(20)]
        self.sparrow_pos = [get_random_pos() for _ in range(20)]
        self.toucan_pos = [get_random_pos() for _ in range(20)]

    def draw(self):
        for i in range(0, 20):
            self.budgie.clip_draw(*self.look_left, *self.budgie_pos[i])
            self.cockatiel.clip_draw(*self.look_left, *self.cockatiel_pos[i])
            self.duck.clip_draw(*self.look_left, *self.duck_pos[i])
            self.parrot.clip_draw(*self.look_left, *self.parrot_pos[i])
            self.robin.clip_draw(*self.look_left, *self.robin_pos[i])
            self.sparrow.clip_draw(*self.look_left, *self.sparrow_pos[i])
            self.toucan.clip_draw(*self.look_left, *self.toucan_pos[i])