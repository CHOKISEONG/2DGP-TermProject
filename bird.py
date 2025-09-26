from pico2d import *
from Bpm import Bpm

class AnimType():
    def __init__(self):
        self.test = [(8, 0, 48, 48),(8, 80, 48, 48),(8, 160, 48, 48),(8, 240, 48, 48)]

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('birdSheet/normalBird.png')
        self.frame = 0
        self.anim_type = AnimType()
        self.bpm = Bpm()

    def draw(self):
        self.image.clip_draw(*self.anim_type.test[self.frame],self.x, self.y)

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def animate(self):
        self.draw()

    def update(self):
        if self.bpm.update():
            self.frame = (self.frame + 1) % 4