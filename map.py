from pico2d import *

class Map:
    def __init__(self):
        self.map = load_image('map/desert.png')
        self.pos = [
            ((35 + x * 42.7 + 21) if y % 2 == 1 else (35 + x * 42.7), 95 + y * 28)
            for y in range(18) for x in range(17)
        ]

    def draw(self):
        self.map.draw(400,300,1000,800)
