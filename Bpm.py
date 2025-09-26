import time

class Bpm:
    def __init__(self):
        self.bpm = 90
        self.interval = 60.0 / self.bpm
        self.pvTime = time.time()

    def update(self):
        cur_time = time.time()
        if cur_time - self.pvTime > self.interval:
            self.one_bpm()
            self.pvTime = time.time()

    def one_bpm(self):
        print("한 박자")