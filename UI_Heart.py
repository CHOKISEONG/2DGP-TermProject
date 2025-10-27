from pico2d import load_image
import game_world

class Bar:
    img = None

    def __init__(self, x):
        if not Bar.img:
            Bar.img = load_image('UI/bpm_bar.png')
        self.area = (0, 0, 64, 64)
        self.x = x
        self.dx = 3 if self.x == 220 else -3
        self.y = 30
        self.size = 40

    def update(self, beat_idx):
        if 397 < self.x < 403:
            game_world.remove_object(self)
        else:
            self.x += self.dx

    def draw(self):
        self.img.clip_draw(*self.area, self.x, self.y, self.size, self.size)

class UI_Heart():
    def __init__(self):
        self.img_heart = load_image('UI/heart.png')
        self.area = (0,0,64,64)
        self.heart_pos = (400,30)
        self.last_beat_idx = -1
        self.size = 50

    def update(self, beat_idx):
        if self.last_beat_idx != beat_idx:
            self.size = 60 if self.size == 50 else 50
            self.generate_bar()
            self.last_beat_idx = beat_idx

    def draw(self):
        self.img_heart.clip_draw(*self.area,*self.heart_pos,self.size,self.size)

    def generate_bar(self):
        bar1 = Bar(220)
        bar2 = Bar(580)
        game_world.add_object(bar1)
        game_world.add_object(bar2)