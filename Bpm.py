import time

class Bpm:
    def __init__(self):
        self.bpm = 90
        self.interval = 60.0 / self.bpm
        self.pvTime = time.time()

    def update(self):
        curTime = time.time()
        if curTime - self.pvTime > self.interval:
            self.oneBpm()
            self.pvTime = time.time()

    def oneBpm(self):
        print("한 박자")

bpm = Bpm()
while True:
    bpm.update()
    time.sleep(bpm.interval)