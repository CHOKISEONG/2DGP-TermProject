from pico2d import *
from Sound.bpm import Bpm
import time

class Music(Bpm):
    def __init__(self, bpm):
        super().__init__(bpm)
        self.main_music = load_wav('Sound/music/120bpm_GerudoValley.wav')
        self.direction_tile_sound = load_music('Sound/sample/put_tile.mp3')
        self.main_music.set_volume(50)
        self.direction_tile_sound.set_volume(50)

    def play(self, name = '',repeat=False):
        sound = getattr(self, name, None)
        if sound is None:
            print(f"'{name}' 이 없음")
            return

        if repeat:
            sound.repeat_play()
        else:
            sound.play()

    def set_volume(self, volume):
        self.main_music.set_volume(volume)

    def check_input_timing(self, window=0.15):
        input_time = get_time()
        result, diff = self.check_timing(input_time, window)
        return result, diff

