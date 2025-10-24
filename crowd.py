from random import randint
from pico2d import *

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
        self.budgie_pos = [randint(0, 600) for _ in range(20)]
        self.cockatiel_pos = [randint(0, 600) for _ in range(20)]
        self.duck_pos = [randint(0, 600) for _ in range(20)]
        self.parrot_pos = [randint(0, 600) for _ in range(20)]
        self.robin_pos = [randint(0, 600) for _ in range(20)]
        self.sparrow_pos = [randint(0, 600) for _ in range(20)]
        self.toucan_pos = [randint(0, 600) for _ in range(20)]

    def draw(self):
        for i in range(0, 10):
            self.budgie.clip_draw(*self.look_left,800 - i, self.budgie_pos[i])
            self.cockatiel.clip_draw(*self.look_left,800 - i, self.cockatiel_pos[i])
            self.duck.clip_draw(*self.look_left, 800 - i, self.duck_pos[i])
            self.parrot.clip_draw(*self.look_left, 800 - i, self.parrot_pos[i])
            self.robin.clip_draw(*self.look_left, 800 - i, self.robin_pos[i])
            self.sparrow.clip_draw(*self.look_left, 800 - i, self.sparrow_pos[i])
            self.toucan.clip_draw(*self.look_left, 800 - i, self.toucan_pos[i])