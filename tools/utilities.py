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
        if position[0] < 123 and position[0] <108:
            continue
        if position[0] < 332 or position[0] > 931:
            return position
        elif position[1] < 350 or position[1] > 462:
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
        if position[0] < 123 and position[0] <108:
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
    slp = random.randint(slpa, slpa+slpb)
    time.sleep(slp/1000)


def crnd(ts, x1, x2, y1, y2):
    '''
    randomly click a point in a rectangle region (x1, y1), (x2, y2)
    '''
    xr = random.randint(x1, x2)
    yr = random.randint(y1, y2)
    ts.MoveTo(xr, yr)
    mysleep(100, 100)
    ts.LeftClick()
    mysleep(100, 100)


def rejxs(ts):
    '''拒绝悬赏'''
    colxs = ts.GetColor(750, 458)
    # print(colxs)
    if colxs == "df715e":
        crnd(ts, 750-5, 750+5, 458-5, 458+5)
        log.writeinfo("Successfully rejected bounty")
        mysleep(1000)
    mysleep(50)


def wtfc1(ts, colx, coly, coll, x1, x2, y1, y2, zzz, adv, mood):
    '''
    Usage: 
    等待并且持续判断点 (colx, coly) 的颜色，直到该点颜色
    等于 coll (if zzz == 0) 或者 不等于 coll (if zzz == 1) 
    然后开始随机点击范围 (x1, x2) (y1, y2) 内的点，直到点 (colx, coly) 的颜色
    if adv == 1: 
        不等于 coll (if zzz == 0) 或者 等于 coll (if zzz == 1)  
    if adv == 0: 
        不判断，点击一次后退出循环
    Example: 
    在准备界面时，通过判断鼓锤上某点的颜色（因为UI不会随着游戏人物摆动），来持续点击鼓面，
    直到鼓锤上该点的颜色改变，说明进入了战斗
    '''
    j = 0
    flgj = 0
    while j == 0:
        rejxs(ts)
        coltest = ts.GetColor(colx, coly)
        #print(colx, coly, coltest)
        if (coltest == coll and zzz == 0) or (coltest != coll and zzz == 1):
            flgj = 1
        if flgj == 1:
            rejxs(ts)
            crnd(ts, x1, x2, y1, y2)
            mysleep(*mood)
            if adv == 0:
                j = 1
            rejxs(ts)
            coltest2 = ts.GetColor(colx, coly)
            if (coltest2 == coll and zzz == 1) or (coltest2 != coll and zzz == 0):
                j = 1
    return 1
