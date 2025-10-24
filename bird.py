from pico2d import *
from bpm import Bpm
from sample import *

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class AnimType:
    def __init__(self):
        self.width, self.height = 60, 60
        self.types = {
            'down': [(8, 240, self.width, self.height), (8, 160, self.width, self.height), (88, 240, self.width, self.height), (88, 160, self.width, self.height)],
            'left': [(8, 0, self.width, self.height), (88, 0, self.width, self.height), (8, 0, self.width, self.height), (88, 0, self.width, self.height)],
            'right': [(248, self.width, self.height), (248, 160, self.width, self.height), (248, 80, self.width, self.height), (248, 0, self.width, self.height)],
            'up': [(168, 240, self.width, self.height), (168, 160, self.width, self.height), (8, 80, self.width, self.height), (88, 80, self.width, self.height)]
        }
        self.current_type = 'down'

    def change_type(self, direction):
        if direction in self.types:
            self.current_type = direction

class Bird:
    def __init__(self, stage):
        self.img = None
        self.img_frame = 0
        self.img_type = AnimType()

        self.sound = Sample('sound/walkSound.mp3')
        self.stage = stage
        self.pos = 0

    def get_pos(self):
        return self.pos
    def set_pos(self, pos):
        self.pos = pos

