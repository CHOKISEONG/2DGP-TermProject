from pico2d import *
from Bpm import Bpm
from musicManager import Music

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class AnimType:
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
        self.img = load_image('birdSheet/normalBird.png')
        self.img_frame = 0
        self.img_type = AnimType()

        self.sound = Music('sound/walkSound.mp3')
        self.bpm = Bpm(90)
        self.map = map
        self.pos = 0

    def getPos(self):
        return self.pos

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.map.pos[self.pos])

    def move(self, idx: int):
        new_pos = self.pos + idx
        if 0 <= new_pos < len(self.map.pos):
            self.pos = new_pos

    def handle_event(self, events):
        if self.bpm.update():
            for event in events:
                if event.type == SDL_KEYDOWN:
                    self.img_frame = (self.img_frame + 1) % 4
                    if event.key == SDLK_LEFT and self.pos % 17 != 0:
                        self.img_type.change_type('left')
                        self.move(LEFT)
                        self.sound.play()
                    elif event.key == SDLK_RIGHT and self.pos % 17 != 16:
                        self.img_type.change_type('right')
                        self.move(RIGHT)
                        self.sound.play()
                    elif event.key == SDLK_UP and self.pos // 17 != 17:
                        self.img_type.change_type('up')
                        self.move(UP)
                        self.sound.play()
                    elif event.key == SDLK_DOWN and self.pos // 17 != 0:
                        self.img_type.change_type('down')
                        self.move(DOWN)
                        self.sound.play()
