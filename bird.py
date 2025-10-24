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

    def getPos(self):
        return self.pos

    def handle_event(self, events):
        for event in events:
            if event.type == SDL_KEYDOWN:
                self.img_frame = (self.img_frame + 1) % 4
                if event.key == SDLK_LEFT and self.pos % 17 != 0:
                    self.img_type.change_type('left')
                    self.move(LEFT)
                    self.sound.play()
                if event.key == SDLK_RIGHT and self.pos % 17 != 16:
                    self.img_type.change_type('right')
                    self.move(RIGHT)
                    self.sound.play()
                if event.key == SDLK_UP and self.pos // 17 != 17:
                    self.img_type.change_type('up')
                    self.move(UP)
                    self.sound.play()
                if event.key == SDLK_DOWN and self.pos // 17 != 0:
                    self.img_type.change_type('down')
                    self.move(DOWN)
                    self.sound.play()

