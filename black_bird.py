import bird
from pico2d import *

LEFT = -1
RIGHT = 1
UP = 17
DOWN = -17

class BlackBird(bird.Bird):
    def __init__(self, stage):
        bird.Bird.__init__(self, stage)
        self.img = load_image('birdSheet/blackBird.png')

    def draw(self):
        self.img.clip_draw(*self.img_type.types[self.img_type.current_type][self.img_frame], *self.stage.pos[self.pos])

    def handle_event(self, events):
        if self.bpm.update():
            for event in events:
                if event.type == SDL_KEYDOWN:
                    self.img_frame = (self.img_frame + 1) % 4
                    if event.key == SDLK_a and self.pos % 17 != 0:
                        self.img_type.change_type('left')
                        self.move(LEFT)
                        self.sound.play()
                    if event.key == SDLK_d and self.pos % 17 != 16:
                        self.img_type.change_type('right')
                        self.move(RIGHT)
                        self.sound.play()
                    if event.key == SDLK_w and self.pos // 17 != 17:
                        self.img_type.change_type('up')
                        self.move(UP)
                        self.sound.play()
                    if event.key == SDLK_s and self.pos // 17 != 0:
                        self.img_type.change_type('down')
                        self.move(DOWN)
                        self.sound.play()