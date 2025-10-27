from pico2d import load_image

class UI_Heart():
    def __init__(self):
        self.img = load_image('UI/heart.png')
        self.pos = (400,30)
        self.last_beat_idx = -1
        self.size = 50

    def update(self, beat_idx):
        if self.last_beat_idx != beat_idx:
            self.size = 60 if self.size == 50 else 50
            self.last_beat_idx = beat_idx

    def draw(self):
        self.img.clip_draw(0,0,64,64,*self.pos,self.size,self.size)