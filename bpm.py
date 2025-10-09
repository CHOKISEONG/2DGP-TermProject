import time

class Bpm:
    def __init__(self, bpm):
        self.bpm = bpm
        self.interval = 60.0 / bpm
        self.start_time = time.time()

    def update(self):
        cur_time = time.time()
        elapsed = cur_time - self.start_time
        current_beat = round(elapsed / self.bpm)
        beat_time = self.start_time + current_beat * self.interval
        diff = abs(cur_time - beat_time)
        return diff <= 0.1, current_beat + 1, diff