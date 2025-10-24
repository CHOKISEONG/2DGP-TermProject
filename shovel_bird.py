import bird
from pico2d import *

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class ShovelBird(bird.Bird):
    def __init__(self, stage):
        bird.Bird.__init__(self, stage)
        self.img = load_image('birdSheet/shovelBird.png')

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.stage.pos[self.pos])

    def move(self, degree):
        if degree == 0:
            if self.pos % 17 != 0:
                self.img_type.change_type('left')
                new_pos = self.pos + LEFT
                if 0 <= new_pos < len(self.stage.pos):
                    self.pos = new_pos
                self.sound.play()
        elif degree == 180:
            if self.pos % 17 != 16:
                self.img_type.change_type('right')
                self.move(RIGHT)
                self.sound.play()
        elif degree == 60:
            if self.pos // 17 != 17:
                self.img_type.change_type('up')
                self.move(UP)
                self.sound.play()
            if event.key == SDLK_k and self.pos // 17 != 0:
                self.img_type.change_type('down')
                self.move(DOWN)
                self.sound.play()

    def handle_event(self, events):
        for event in events:
            if event.type == SDL_KEYDOWN:
                self.img_frame = (self.img_frame + 1) % 4
                if event.key == SDLK_j and self.pos % 17 != 0:
                    self.img_type.change_type('left')
                    self.move(LEFT)
                    self.sound.play()
                if event.key == SDLK_l and self.pos % 17 != 16:
                    self.img_type.change_type('right')
                    self.move(RIGHT)
                    self.sound.play()
                if event.key == SDLK_i and self.pos // 17 != 17:
                    self.img_type.change_type('up')
                    self.move(UP)
                    self.sound.play()
                if event.key == SDLK_k and self.pos // 17 != 0:
                    self.img_type.change_type('down')
                    self.move(DOWN)
                    self.sound.play()