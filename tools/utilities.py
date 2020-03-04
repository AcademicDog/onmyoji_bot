import json
import logging
import random
import time


class Mood:
    '''
    用于模拟随机的点击频率，每5分钟更换一次点击规律\n
    energetic: 状态极佳，点击延迟在1-1.5s\n
    joyful: 状态不错，点击延迟在1.3-2.1s\n
    normal: 状态一般，点击延迟在1.8-3s\n
    tired: 状态疲劳，点击延迟在2.5-4\n
    exhausted: CHSM，点击延迟在3-5s\n
    '''
    __first_init = True

    def __init__(self, state=5):
        self.lastime = time.time()
        self.state = state
        if Mood.__first_init:
            self.read_config()
            Mood.__first_init = False
        a = random.randint(1, self.state)
        logging.info("创建延迟参数，等级: %d", a)
        self.lastmood = Mood.mymood[a]

    def read_config(self):
        try:
            # 读取延迟配置
            with open('delay.json', 'r') as f:
                fileObject = f.read()
            jsObj = json.loads(fileObject)
            logging.info('读取延迟配置文件成功')
            Mood.mymood = {
                1: (jsObj['1'][0], jsObj['1'][1]),
                2: (jsObj['2'][0], jsObj['2'][1]),
                3: (jsObj['3'][0], jsObj['3'][1]),
                4: (jsObj['4'][0], jsObj['4'][1]),
                5: (jsObj['5'][0], jsObj['5'][1])}
        except FileNotFoundError:
            # 文件未找到
            logging.info('使用默认延迟参数')
            self.set_default()
        except:
            # 其他错误
            logging.warning('延迟配置文件错误，使用默认参数')
            self.set_default()
        logging.info('延迟参数: '+str(Mood.mymood))

    def set_default(self):
        '''
        设置默认延迟参数
        '''
        Mood.mymood = {
            1: (1000, 500),
            2: (1300, 800),
            3: (1800, 1200),
            4: (2500, 1500),
            5: (3000, 2000)}

    def getmood(self):
        if (time.time() - self.lastime >= 300):
            self.lastime = time.time()
            a = random.randint(1, self.state)
            self.lastmood = Mood.mymood[a]
            logging.info("修改延迟参数，等级 %d", a)
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
    safe_area = {
        1: ((20, 106), (211, 552)),
        2: ((931, 60), (1120, 620))}

    index = random.randint(1, 2)
    return safe_area[index]


def secondposition():
    '''
    获得点击位置，扣除御魂部分
        :return: 返回随机位置坐标
    '''
    return (random.randint(970, 1111), random.randint(100, 452))


def checkposition(pos):
    '''
    校核结算位置
        :param pos: (x, y)位置坐标
        :return: 如果合适返回True，否则返回False
    '''
    if pos[0] < 1111 and pos[0] > 970:
        if pos[1] < 452 and pos[1] > 100:
            return True
    return False


def mysleep(slpa, slpb=0):
    '''
    randomly sleep for a short time between `slpa` and `slpa + slpb` \n
    because of the legacy reason, slpa and slpb are in millisecond
    '''
    if slpb == 0:
        slp = random.randint(int(0.5*slpa), int(1.5*slpa))
    else:
        slp = random.randint(slpa, slpa+slpb)
    time.sleep(slp/1000)


if __name__ == "__main__":
    mood = Mood()
    print(Mood.mymood)
