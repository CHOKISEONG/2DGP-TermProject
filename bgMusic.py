from pico2d import *

class Music:
    def __init__(self, file_path):
        self.music = load_wav(file_path)
        self._is_playing = False

    def play(self, repeat=False):
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
