from gameLib.game_ctl import GameControl
from gameLib.game_scene import GameScene
from tools.logsystem import MyLog
from tools.game_pos import TansuoPos, YuhunPos
import tools.utilities as ut

import configparser
import os
import random
import threading
import time
import win32gui


class Fighter(GameScene):

    def __init__(self, emyc=0, hwnd=0):
        '''
        初始化
            : param emyc=0: 点怪设置：0-不点怪
            : param hwnd=0: 指定窗口句柄：0-否；其他-窗口句柄
        '''
        # 初始参数
        self.emyc = emyc
        self.run = True

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.client = conf.getint('DEFAULT', 'client')
        quit_game_enable = conf.getboolean('watchdog', 'watchdog_enable')
        self.max_op_time = conf.getint('watchdog', 'max_op_time')
        self.max_win_time = conf.getint('watchdog', 'max_win_time')
        self.mitama_team_mark = conf.getint('mitama', 'mitama_team_mark')
        self.max_times = conf.getint('DEFAULT', 'max_times')
        self.end_operation = conf.getint('DEFAULT', 'end_operation')
        self.run_times = 0

        # 启动日志
        self.log = MyLog.mlogger

        # 绑定窗口
        if hwnd == 0:
            if self.client == 0:
                hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
            elif self.client == 1:
                hwnd = win32gui.FindWindow(0, u'阴阳师 - MuMu模拟器')
                # TansuoPos.InitPosWithClient__()
                # YuhunPos.InitPosWithClient__()
        self.yys = GameControl(hwnd, quit_game_enable)
        self.log.info('绑定窗口成功')
        self.log.info(str(hwnd))

        # 激活窗口
        self.yys.activate_window()
        self.log.info('激活窗口成功')
        time.sleep(0.5)

        # 绑定场景

        # 自检
        debug_enable = conf.getboolean('others', 'debug_enable')
        if debug_enable:
            task = threading.Thread(target=self.yys.debug)
            task.start()

    def check_battle(self):
        # 检测是否进入战斗
        self.log.info('检测是否进入战斗')
        self.yys.wait_game_img('img\\ZI-DONG.png', self.max_win_time)
        self.log.info('已进入战斗')

    def check_end(self):
        '''
        检测是否打完
            :return: 胜利页面返回0；奖励页面返回1
        '''
        self.log.info('检测是战斗是否结束')
        start_time = time.time()
        myend = -1
        while time.time()-start_time <= self.max_win_time and self.run:
            # 拒绝悬赏
            self.yys.rejectbounty()

            maxVal, maxLoc = self.yys.find_multi_img(
                'img/SHENG-LI.png', 'img/TIAO-DAN.png', 'img/JIN-BI.png', 'img/JIE-SU.png')
            end_cof = max(maxVal)
            if end_cof > 0.9:
                myend = maxVal.index(end_cof)
                break
            time.sleep(0.5)
        if myend in [0, 3]:
            self.log.info('战斗成功')
            return 0
        elif myend in [1, 2]:
            self.log.info('本轮战斗结束')
            return 1

    def check_times(self):
        '''
        监测游戏次数是否达到最大次数
        '''
        self.run_times = self.run_times + 1
        self.log.info('游戏已运行'+str(self.run_times)+'次')
        if(self.run_times == self.max_times):
            if(self.end_operation == 0):
                self.log.warning('关闭脚本(次数已满)...')
                self.run = False
                os._exit(0)
            elif(self.end_operation == 1):
                self.log.warning('关闭游戏(次数已满)...')
                self.yys.quit_game()
                self.log.warning('关闭脚本(次数已满)...')
                self.run = False
                os._exit(0)

    def get_reward(self, mood, state):
        '''
        结算处理
            :param mood: 状态函数
            :param state: 上一步的状态。0-战斗成功页面; 1-领取奖励页面
        '''
        # 初始化结算点
        mypos = ut.secondposition()
        if state == 0:
            self.yys.mouse_click_bg(mypos)
            self.log.info('点击结算')
            mood.moodsleep()
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # 拒绝悬赏
            self.yys.rejectbounty()

            while True:
                newpos = (mypos[0] + random.randint(-50, 50),
                          mypos[1] + random.randint(-50, 50))
                if ut.checkposition(newpos):
                    mypos = newpos
                    break

            # 点击一次结算
            self.yys.mouse_click_bg(mypos)
            self.log.info('点击结算')
            mood.moodsleep()

            # 错误纠正
            maxVal, maxLoc = self.yys.find_multi_img(
                'img/FA-SONG-XIAO-XI.png', 'img/ZHI-LIAO-LIANG.png')
            if max(maxVal) > 0.9:
                self.yys.mouse_click_bg((35, 295), (140, 475))
                self.log.info('错误纠正')
                mood.moodsleep()
                continue

            # 正常结算
            maxVal, maxLoc = self.yys.find_multi_img(
                'img/SHENG-LI.png', 'img/TIAO-DAN.png', 'img/JIN-BI.png', 'img/JIE-SU.png')
            if max(maxVal) < 0.9:
                self.log.info('结算成功')
                return

        self.log.warning('点击结算失败!')
        # 提醒玩家点击失败，并在5s后退出
        self.yys.activate_window()
        time.sleep(5)
        self.yys.quit_game()

    def mitama_team_click(self):
        '''
        御魂标记己方式神
        '''
        num = self.mitama_team_mark
        if num > 0:
            # 100 1040
            # 125 50
            # 御魂场景获取标记位置
            min = (num - 1) * 105 + (num - 1) * 100 + 95
            max = min + 50
            pos = (min, 355), (max, 425)

            start_time = time.time()
            while time.time() - start_time <= 3:
                x1 = pos[0][0] - 100
                y1 = pos[0][1] - 250
                x2 = pos[1][0] + 100
                y2 = pos[1][1]
                exp_pos = self.yys.find_color(
                    ((x1, y1), (x2, y2)), (134, 227, 96), 5)
                # print('颜色位置', exp_pos)
                if exp_pos != -1:
                    self.log.info('标记式神成功')
                    return True
                else:
                    # 点击指定位置并等待下一轮
                    self.yys.mouse_click_bg(*pos)
                    self.log.info('标记式神')
                    ut.mysleep(500)

            self.log.warning('标记式神失败')

    def click_monster(self):
        # 点击怪物
        pass

    def click_until(self, tag, img_path, pos, pos_end=None, step_time=0.8, appear=True):
        '''
        在某一时间段内，后台点击鼠标，直到出现某一图片出现或消失
            :param tag: 按键名
            :param img_path: 图片路径
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
            :step_time=0.5: 查询间隔
            :appear: 图片出现或消失：Ture-出现；False-消失
            :return: 成功返回True, 失败退出游戏
        '''
        # 在指定时间内反复监测画面并点击
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # 点击指定位置
            self.yys.mouse_click_bg(pos, pos_end)
            self.log.info('点击 ' + tag)
            ut.mysleep(step_time*1000)

            result = self.yys.find_game_img(img_path)
            if not appear:
                result = not result
            if result:
                self.log.info('点击 ' + tag + ' 成功')
                return True

        # 提醒玩家点击失败，并在5s后退出
        self.click_failed(tag)

    def click_until_multi(self, tag, *img_path, pos, pos_end=None, step_time=0.8):
        '''
        在某一时间段内，后台点击鼠标，直到出现列表中任一图片
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
            # 点击指定位置
            self.yys.mouse_click_bg(pos, pos_end)
            self.log.info('点击 ' + tag)
            ut.mysleep(step_time*1000)

            maxval, _ = self.yys.find_multi_img(*img_path)
            if max(maxval) > 0.9:
                self.log.info('点击 ' + tag + ' 成功')
                return True

        # 提醒玩家点击失败，并在5s后退出
        self.click_failed(tag)

    def click_until_knn(self, tag, img_path, pos, pos_end=None, step_time=0.8, appear=True, thread=0):
        '''
        在某一时间段内，后台点击鼠标，直到出现某一图片出现或消失
            :param tag: 按键名
            :param img_path: 图片路径
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
            :step_time=0.5: 查询间隔
            :appear: 图片出现或消失：Ture-出现；False-消失
            :thread: 检测阈值
            :return: 成功返回True, 失败退出游戏
        '''
        # 在指定时间内反复监测画面并点击
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            # 点击指定位置并等待下一轮
            self.yys.mouse_click_bg(pos, pos_end)
            self.log.info('点击 ' + tag)
            ut.mysleep(step_time*1000)

            result = self.yys.find_game_img_knn(img_path, thread=thread)
            if not appear:
                result = not result
            if result:
                self.log.info('点击 ' + tag + ' 成功')
                return True

        # 提醒玩家点击失败，并在5s后退出
        self.click_failed(tag)

    def click_failed(self, tag):
        # 提醒玩家点击失败，并在5s后退出
        self.log.warning('点击 ' + tag + ' 失败!')
        self.yys.activate_window()
        time.sleep(5)
        self.yys.quit_game()

    def activate(self):
        self.log.warning('启动脚本')
        self.run = True
        self.yys.run = True

    def deactivate(self):
        self.log.warning('手动停止脚本')
        self.run = False
        self.yys.run = False

    def slide_x_scene(self, distance):
        '''
        水平滑动场景
            :return: 成功返回True; 失败返回False
        '''
        x0 = random.randint(distance + 10, 1126)
        x1 = x0 - distance
        y0 = random.randint(436, 486)
        y1 = random.randint(436, 486)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))
        self.log.info('水平滑动界面')
