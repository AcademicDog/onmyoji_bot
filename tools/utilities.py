import random
import time

from tools.logsystem import WriteLog

log = WriteLog()


class Mood:
    '''
    用于模拟随机的点击频率，每5分钟更换一次点击规律\n
    energetic: 状态极佳，点击延迟在1-1.3s\n
    joyful: 状态不错，点击延迟在1.3-1.8s\n
    normal: 状态一般，点击延迟在1.8-2.3s\n
    tired: 状态疲劳，点击延迟在2.3-2.8\n
    exhausted: CHSM，点击延迟在2.8-3.6s\n
    '''

    def __init__(self, state=5):
        self.lastime = time.time()
        self.state = state
        Mood.mymood = {
            1: (1000, 300),
            2: (1300, 500),
            3: (1800, 500),
            4: (2300, 500),
            5: (2800, 800)}
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
    h = 530
    while True:
        position = (random.randint(0, w), random.randint(50, h))
        if position[0] < 123 and position[1] <108:
            continue
        if position[0] < 210 or position[0] > 1083:
            return position
        elif position[1] < 260:
            return position


def mysleep(slpa, slpb=0):
    '''
    randomly sleep for a short time between `slpa` and `slpa + slpb` \n
    because of the legacy reason, slpa and slpb are in millisecond
    '''
    slp = random.randint(int(slpa), int(slpa+slpb))
    time.sleep(slp/1000)