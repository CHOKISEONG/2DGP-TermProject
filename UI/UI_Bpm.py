from pico2d import load_font
import game_world

class UI_Bpm():
    def __init__(self):
        self.font = load_font('ENCR10B.TTF', 100)
        self.font_pos = (310,650)
        self.last_beat_idx = -1
        self.size = 50

    def update(self, beat_idx):
        if self.last_beat_idx != beat_idx:
            self.size = 1.1 if self.size == 1 else 1
            self.last_beat_idx = beat_idx

    def draw(self):
        self.font.draw(*self.font_pos, '120')