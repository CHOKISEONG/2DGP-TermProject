from pico2d import *

class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('birdSheet/normalBird.png')

    def draw(self):
        self.image.draw(self.x, self.y)