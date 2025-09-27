import time

class Bpm:
    def __init__(self, bpm):
        self.bpm = bpm
        self.interval = 60.0 / bpm
        self.pvTime = time.time()

    def update(self):
        cur_time = time.time()
        diff = cur_time - self.pvTime
        if diff < self.interval:
            return diff < self.interval / 10.0 or diff > self.interval * 9.0 / 10.0
        else:
            self.pvTime = cur_time
            return True