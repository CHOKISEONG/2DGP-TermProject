from pico2d import *
from Sound.bpm import Bpm

class MusicManager(Bpm):
    def __init__(self, bpm):
        super().__init__(bpm)
        self.main_music = load_wav('Sound/music/120bpm_GerudoValley.wav')
        self.main_music.set_volume(50)

    def play(self, repeat=False):
        if repeat:
            self.main_music.repeat_play()
        else:
            self.main_music.play()

    def check_input_timing(self, window=0.15):
        input_time = get_time()
        result, diff = self.check_timing(input_time, window)
        return result, diff

class SfxManager:
    def __init__(self):
        self.sfx = {
            'direction_tile' : load_music('Sound/sample/put_tile.mp3'),
            'walk' : load_music('Sound/sample/walk.mp3'),
            'explosion' : load_music('Sound/sample/explosion.mp3')
        }
        for s in self.sfx.values():
            s.set_volume(50)

    def play(self, name):
        if name not in self.sfx:
            print(f'{name} 사운드가 없음')
            return

        self.sfx[name].play()




