import random
import time

from tools.logsystem import WriteLog

log = WriteLog()


class Mood:
    '''
    用于模拟随机的点击频率，每5分钟更换一次点击规律\n
    energetic: 状态极佳，点击延迟在1-1.5s\n
    joyful: 状态不错，点击延迟在1.3-2.1s\n
    normal: 状态一般，点击延迟在1.8-3s\n
    tired: 状态疲劳，点击延迟在2.5-4\n
    exhausted: CHSM，点击延迟在3-5s\n
    '''

    def __init__(self, state=5):
        self.lastime = time.time()
        self.state = state
        Mood.mymood = {
            1: (1000, 500),
            2: (1300, 800),
            3: (1800, 1200),
            4: (2500, 1500),
            5: (3000, 2000)}
        a = random.randint(1, self.state)
        log.writeinfo("Now you mood is level %d", a)
        self.lastmood = Mood.mymood[a]

    def getmood(self):
        if (time.time() - self.lastime >= 300):
            self.lastime = time.time()
            a = random.randint(1, self.state)
            self.lastmood = Mood.mymood[a]
            log.writeinfo("Now you mood is level %d", a)
        return self.lastmood

    def moodsleep(self):
        mysleep(*self.getmood())

    def get1mood(self):
        return random.randint(self.getmood()[0], self.getmood()[0] + self.getmood()[1])


def firstposition():
    '''
    获得点击位置，扣除御魂部分
        :return: 返回随机位置坐标
    '''
    w = 1136
    h = 640
    while True:
        position = (random.randint(0, w), random.randint(50, h))
        if position[0] < 123 and position[1] <108:
            continue
        if position[0] < 332 or position[0] > 931:
            return position
        elif position[1] < 260:
            return position


def secondposition():
    '''
    获得点击位置，扣除御魂部分
        :return: 返回随机位置坐标
    '''
    return (random.randint(887, 1111), random.randint(56, 452))
    '''
    while True:
        position = (random.randint(0, w), random.randint(50, h - 90))
        if position[0] < 123 and position[1] <108:
            continue
        if position[0] > 1020 and position[1] <80:
            continue
        if position[0] < 180 or position[0] > 956:
            return position
        elif position[1] < 112:
            return position
    '''


def mysleep(slpa, slpb=0):
    '''
    randomly sleep for a short time between `slpa` and `slpa + slpb` \n
    because of the legacy reason, slpa and slpb are in millisecond
    '''
    slp = random.randint(int(slpa), int(slpa+slpb))
    time.sleep(slp/1000)