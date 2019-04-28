import time

class Watchdog:
    #时间，新 旧
    lastime = [0, 0]

    def __init__(self):
        Watchdog.lastime[1] = time.time()

    def feed(self):
        Watchdog.lastime[1] = time.time()

    def bark(self):
        Watchdog.lastime[0] = time.time()
        period = int(Watchdog.lastime[0] - Watchdog.lastime[1])
        if(period > 300):
            return 1
        else:
            return 0