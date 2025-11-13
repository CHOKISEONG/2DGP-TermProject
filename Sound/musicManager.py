from pico2d import *
from Sound.bpm import Bpm

class MusicManager(Bpm):
    # 오디오 출력 지연(환경에 따라 0.04~0.08s 사이 조정 권장)
    LATENCY_COMP = 0.06

    def __init__(self, bpm):
        super().__init__(bpm)
        self.main_music = load_wav('Sound/music/120bpm_GerudoValley.wav')
        self.main_music.set_volume(50)

    def play(self, repeat=False, sync=True, offset=0.0):
        # 음악 재생 직전에 비트 기준 리셋(지연 보정 포함)
        if sync:
            self.reset(offset - self.LATENCY_COMP)
        if repeat:
            self.main_music.repeat_play()
        else:
            self.main_music.play()

    def check_input_timing(self, window=0.15, at_time=None):
        t = get_time() if at_time is None else at_time
        return super().check_timing(t, window)

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




