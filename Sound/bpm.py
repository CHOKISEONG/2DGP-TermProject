from pico2d import *

class Bpm:
    def __init__(self, bpm, start_time=None):
        self.bpm = bpm
        self.interval = 60.0 / bpm
        self.start_time = start_time if start_time is not None else get_time()

    def reset(self, offset=0.0):
        self.start_time = get_time() + offset

    def get_current_beat(self, t=None):
        now = get_time() if t is None else t
        elapsed = now - self.start_time
        return int(elapsed / self.interval)

    def check_timing(self, input_time=None, window=0.15):
        now = get_time() if input_time is None else input_time
        nearest_beat = round((now - self.start_time) / self.interval)
        beat_time = self.start_time + nearest_beat * self.interval
        diff = abs(now - beat_time)

        if diff < window * 0.05:
            return "Perfect", diff
        elif diff < window * 0.1:
            return "Good", diff
        else:
            return "Miss", diff
