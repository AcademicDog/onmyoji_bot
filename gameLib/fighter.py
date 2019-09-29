from gameLib.game_ctl import GameControl
from tools.logsystem import WriteLog

import configparser
import time


class Fighter:

    def __init__(self, name='', emyc=0):
        # 初始参数
        self.emyc = emyc
        self.name = name
        self.run = True

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        quit_game_enable = conf.getboolean('watchdog', 'watchdog_enable')
        self.max_op_time = conf.getint('watchdog', 'max_op_time')
        self.max_win_time = conf.getint('watchdog', 'max_win_time')

        # 启动日志
        self.log = WriteLog()

        # 绑定窗口
        self.yys = GameControl(u'阴阳师-网易游戏', quit_game_enable)
        self.log.writeinfo(self.name + '绑定窗口成功')

        # 激活窗口
        self.yys.activate_window()
        self.log.writeinfo(self.name + '激活窗口成功')
        time.sleep(0.5)

    def check_battle(self):
        # 检测是否进入战斗
        self.log.writeinfo(self.name + '检测是否进入战斗')
        self.yys.wait_game_img('img\\ZI-DONG.png', self.max_win_time)
        self.log.writeinfo(self.name + '已进入战斗')

    def check_end(self):
        # 检测是否打完
        self.log.writeinfo(self.name + '检测是战斗是否结束')
        self.yys.wait_game_img('img\\JIE-SU.png', self.max_win_time)
        self.log.writeinfo(self.name + "战斗结束")

    def click_monster(self):
        # 点击怪物
        pass

    def click_until(self, tag, img_path, pos, pos_end=None, step_time=0.5):
        '''
        在某一时间段内，后台点击鼠标，直到出现某一图片出现
            :param tag: 按键名
            :param img_path: 图片路径
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
            :step_time=0.5: 查询间隔
            :return: 成功返回True, 失败退出游戏
        '''
        # 在指定时间内反复监测画面并点击
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            result = self.yys.find_game_img(img_path)
            if result:
                self.log.writeinfo(self.name + '点击 ' + tag + ' 成功')
                return True
            else:
                # 点击指定位置并等待下一轮
                self.yys.mouse_click_bg(pos, pos_end)
                self.log.writeinfo(self.name + '点击 ' + tag)
            time.sleep(step_time)
        self.log.writewarning(self.name + '点击 ' + tag + ' 失败!')

        # 提醒玩家点击失败，并在5s后退出
        self.yys.activate_window()
        time.sleep(5)
        self.yys.quit_game()

    def activate(self):
        self.log.writewarning(self.name + '启动脚本')
        self.run = True
        self.yys.run = True

    def deactivate(self):
        self.log.writewarning(self.name + '手动停止脚本')
        self.run = False
        self.yys.run = False
