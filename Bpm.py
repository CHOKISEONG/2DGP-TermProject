import time

class Bpm:
    def __init__(self):
        self.bpm = 90
        self.interval = 60.0 / self.bpm
        self.pvTime = time.time()

    def update(self):
        cur_time = time.time()
        if cur_time - self.pvTime > self.interval:
            self.pvTime = time.time()
            return True
        return False