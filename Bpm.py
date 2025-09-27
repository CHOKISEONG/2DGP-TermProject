import time

class Bpm:
    def __init__(self, bpm):
        self.bpm = bpm
        self.interval = 60.0 / bpm
        self.coyote_time = 0.1
        self.pvTime = time.time()

    def update(self):
        cur_time = time.time()
        if cur_time - self.pvTime > self.interval:
            self.pvTime = time.time()
            return True
        elif cur_time - self.pvTime > self.interval - self.coyote_time:
            return True
        return False