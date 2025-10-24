import random
from pico2d import *

def get_random_pos():
    points = [(5, 20), (790, 20), (790, 595), (5, 595)]
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
    bird_names = ["budgie", "cockatiel", "duck", "parrot", "robin", "sparrow", "toucan"]
    def __init__(self):
        self.images = {name: load_image(f"birdSheet/{name.capitalize()}.png") for name in self.bird_names}
        self.positions = {name: [get_random_pos() for _ in range(15)] for name in self.bird_names}
        self.directions = {name: [] for name in self.bird_names}

        self.look_left = (0, 0, 48, 48)
        self.look_right = (48, 0, 48, 48)

        for name in self.bird_names:
            for pos in self.positions[name]:
                if pos[0] > 400:
                    self.directions[name].append(self.look_left)
                else:
                    self.directions[name].append(self.look_right)

    def draw(self):
        for i in range(15):
            for name in self.bird_names:
                image = self.images[name]
                look = self.directions[name][i]
                pos = self.positions[name][i]
                image.clip_draw(*look, *pos)