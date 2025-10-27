from pico2d import load_image
import game_world

class LineBar:
    img = None

    def __init__(self):
        if not LineBar.img:
            LineBar.img = load_image('UI/bpm_bar2.png')
        self.last_beat_idx = -1
        self.area = (0, 0, 64, 64)
        self.x = 400
        self.y = 30
        self.w = 380
        self.h = 40

    def draw(self):
        self.img.clip_draw(*self.area, self.x, self.y, self.w, self.h)

class Bar:
    img = None

    def __init__(self, x, is_move = True):
        if not Bar.img:
            Bar.img = load_image('UI/bpm_bar.png')
        self.area = (0, 0, 64, 64)
        self.x = x
        self.dx = 3 if self.x == 220 else -3
        self.y = 30
        self.size = 40
        self.is_move = is_move

    def update(self, beat_idx):
        if self.is_move:
            if 397 < self.x < 403:
                game_world.remove_object(self)
            else:
                self.x += self.dx

    def draw(self):
        self.img.clip_draw(*self.area, self.x, self.y, self.size, self.size)

class UI_Heart():
    def __init__(self):
        self.img_heart = load_image('UI/heart.png')
        self.img_line = LineBar()
        self.img_line2 = Bar(210,False)
        self.img_line3 = Bar(590, False)
        self.area = (0,0,64,64)
        self.heart_pos = (400,30)
        self.last_beat_idx = -1
        self.size = 50

    def update(self, beat_idx):
        if self.last_beat_idx != beat_idx:
            self.size = 60 if self.size == 50 else 50
            self.img_line.h = 100 if self.img_line.h == 40 else 40
            self.generate_bar()

            self.last_beat_idx = beat_idx

    def draw(self):
        self.img_line.draw()
        self.img_line2.draw()
        self.img_line3.draw()
        self.img_heart.clip_draw(*self.area,*self.heart_pos,self.size,self.size)

    def generate_bar(self):
        bar1 = Bar(220)
        bar2 = Bar(580)
        game_world.add_object(bar1)
        game_world.add_object(bar2)