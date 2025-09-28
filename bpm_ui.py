from pico2d import *
from Bpm import Bpm

class BpmUI:
    def __init__(self):
        def __init__(self, map):
            self.img = load_image('UI/PS4.png')
            self.bpm = Bpm(160)
            self.x = 0
            self.y = 0
