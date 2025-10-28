from pico2d import *
from Sound.bpm import Bpm
import time

class Music(Bpm):
    def __init__(self, file_path, beat):
        super().__init__(beat)
        self.music = load_wav(file_path)
        self.music.set_volume(50)
        self._is_playing = False

    def play(self, repeat=False):
        self.start_time = time.time()
        if repeat:
            self.music.repeat_play()
        else:
            self.music.play()
        self._is_playing = True

    def stop(self):
        self.music.stop()
        self._is_playing = False

    def set_volume(self, volume):
        self.music.set_volume(volume)

    def is_playing(self):
        return self._is_playing

    def check_input_timing(self, window=0.15):
        if not self._is_playing:
            return "Not Playing", None

        input_time = time.time()
        result, diff = self.check_timing(input_time, window)
        return result, diff

