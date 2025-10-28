import time

class Bpm:
    def __init__(self, bpm):
        self.bpm = bpm
        self.interval = 60.0 / bpm
        self.start_time = time.time()

    def get_elapsed(self):
        return time.time() - self.start_time

    def get_current_beat(self):
        elapsed = self.get_elapsed()
        return int(elapsed / self.interval)

    def check_timing(self, input_time, window=0.15):
        nearest_beat = round((input_time - self.start_time) / self.interval)
        beat_time = self.start_time + nearest_beat * self.interval

        diff = abs(input_time - beat_time)

        if diff < window * 0.5:
            return "Perfect", diff
        elif diff < window:
            return "Good", diff
        else:
            return "Miss", diff