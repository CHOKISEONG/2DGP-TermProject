import pygame
from pico2d import *
from Bpm import Bpm
from enum import Enum
from map import Map

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class AnimType():
    def __init__(self):
        self.types = {
            'down': [(8, 240, 48, 48), (8, 160, 48, 48), (88, 240, 48, 48), (88, 160, 48, 48)],
            'left': [(8, 0, 48, 48), (88, 0, 48, 48), (8, 0, 48, 48), (88, 0, 48, 48)],
            'right': [(248, 240, 48, 48), (248, 160, 48, 48), (248, 80, 48, 48), (248, 0, 48, 48)],
            'up': [(168, 240, 48, 48), (168, 160, 48, 48), (8, 80, 48, 48), (88, 80, 48, 48)]
        }
        self.current_type = 'down'

    def change_type(self, direction):
        if direction in self.types:
            self.current_type = direction

class Bird:
    def __init__(self, map):
        self.map = map
        self.pos = 0
        self.img = load_image('birdSheet/normalBird.png')
        self.img_frame = 0
        self.img_type = AnimType()
        self.bpm = Bpm()

    def getPos(self):
        return self.pos

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.map.pos[self.pos])

    def move(self, idx: int):
        new_pos = self.pos + idx
        if 0 <= new_pos < len(self.map.pos):
            self.pos = new_pos

    def handle_event(self, events):
        for event in events:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_LEFT and self.pos % 17 != 0:
                    self.img_type.change_type('left')
                    self.move(LEFT)
                elif event.key == SDLK_RIGHT and self.pos % 17 != 16:
                    self.img_type.change_type('right')
                    self.move(RIGHT)
                elif event.key == SDLK_UP and self.pos // 17 != 17:
                    self.img_type.change_type('up')
                    self.move(UP)
                elif event.key == SDLK_DOWN and self.pos // 17 != 0:
                    self.img_type.change_type('down')
                    self.move(DOWN)
        if self.bpm.update():
            self.img_frame = (self.img_frame + 1) % 4