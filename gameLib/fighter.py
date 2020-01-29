from gameLib.game_ctl import GameControl
from tools.logsystem import WriteLog
from tools.game_pos import TansuoPos, CommonPos

import os
import configparser
import logging
import random
import time
import win32gui
import threading
import tools.utilities as ut

confPath = os.path.join(os.getcwd(), "conf.ini") #拼接上配置文件名称目录

class Fighter:

    def __init__(self, name='', emyc=0, hwnd=0):
        '''
        初始化
            ：param name='': 打手名称
            : param emyc=0: 点怪设置：0-不点怪
            : param hwnd=0: 指定窗口句柄：0-否；其他-窗口句柄
        '''
        # 初始参数
        self.emyc = emyc
        self.name = name
        self.run = True

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read(confPath)
        quit_game_enable = conf.getboolean('watchdog', 'watchdog_enable')
        self.max_op_time = conf.getint('watchdog', 'max_op_time')
        self.max_win_time = conf.getint('watchdog', 'max_win_time')
        self.sign_shikigami = conf.getboolean('common', 'sign_shikigami')

        # 启动日志
        self.log = WriteLog()

        # 绑定窗口
        if hwnd == 0:
            hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
        self.yys = GameControl(hwnd, quit_game_enable)
        self.log.writeinfo(self.name + '绑定窗口成功')
        self.log.writeinfo(self.name + str(hwnd))

        # 激活窗口
        self.yys.activate_window()
        self.log.writeinfo(self.name + '激活窗口成功')
        time.sleep(0.5)

        # 自检
        debug_enable = conf.getboolean('others', 'debug_enable')
        if debug_enable:
            task = threading.Thread(target=self.yys.debug)
            task.start()

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

    def click_shikigami(self):
        # 点击第二位式神
        if self.sign_shikigami:
            self.log.writeinfo("开始标记式神")
            ut.mysleep(200, 50)
            self.click_until('标记式神', 'img/GREEN-SIGN.png', *
                             CommonPos.shikigami_position_2, 0.4, True, False)
            self.log.writeinfo("标记式神完成")

    def click_until(self, tag, img_path, pos, pos_end=None, step_time=0.5, appear=True, quit=True):
        '''
        在某一时间段内，后台点击鼠标，直到出现某一图片出现或消失
            :param tag: 按键名
            :param img_path: 图片路径
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
            :step_time=0.5: 查询间隔
            :appear: 图片出现或消失：Ture-出现；False-消失
            :quit=True: 超时后是否退出
            :return: 成功返回True, 失败退出游戏
        '''
        # 在指定时间内反复监测画面并点击
        start_time = time.time()
        while time.time()-start_time <= self.max_op_time and self.run:
            result = self.yys.find_game_img(img_path)
            if not appear:
                result = not result
            if result:
                self.log.writeinfo(self.name + '点击 ' + tag + ' 成功')
                return True
            else:
                # 点击指定位置并等待下一轮
                self.yys.mouse_click_bg(pos, pos_end)
                self.log.writeinfo(self.name + '点击 ' + tag)
            ut.mysleep(step_time*1000, 100)
        self.log.writewarning(self.name + '点击 ' + tag + ' 失败!')

        # 提醒玩家点击失败，并在5s后退出
        if quit:
            # 超时则退出游戏
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
        logging.info(self.name + '水平滑动界面')

    def get_scene(self):
        '''
        识别当前场景
            :return: 返回场景名称:1-庭院; 2-探索界面; 3-章节界面; 4-探索内
        '''
        # 拒绝悬赏
        self.yys.rejectbounty()

        # 分别识别庭院、探索、章节页、探索内
        maxVal, maxLoc = self.yys.find_multi_img(
            'img/JIA-CHENG.png', 'img/JUE-XING.png', 'img/TAN-SUO.png', 'img/YING-BING.png')

        scene_cof = max(maxVal)
        if scene_cof > 0.97:
            scene = maxVal.index(scene_cof)
            return scene + 1
        else:
            return 0

    def switch_to_scene(self, scene):
        '''
        切换场景
            :param scene: 需要切换到的场景:1-庭院; 2-探索界面; 3-章节界面; 4-探索内
            :return: 切换成功返回True；切换失败直接退出
        '''
        scene_now = self.get_scene()
        logging.info(self.name + '目前场景：' + str(scene_now))
        if scene_now == scene:
            return True
        if scene_now == 1:
            # 庭院中
            if scene == 2 or scene == 3 or scene == 4:
                # 先将界面划到最右边
                self.slide_x_scene(800)
                time.sleep(2)
                self.slide_x_scene(800)

                # 点击探索灯笼进入探索界面
                self.click_until('探索灯笼', 'img/JUE-XING.png', *
                                 TansuoPos.tansuo_denglong, 2)

                # 递归
                self.switch_to_scene(scene)

        if scene_now == 2:
            # 探索界面
            if scene == 3 or scene == 4:
                # 点击最后章节
                self.click_until('最后章节', 'img/TAN-SUO.png',
                                 *TansuoPos.last_chapter, 2)

                # 递归
                self.switch_to_scene(scene)

        if scene_now == 3:
            # 章节界面
            if scene == 4:
                # 点击探索按钮
                self.click_until('探索按钮', 'img/YING-BING.png',
                                 *TansuoPos.tansuo_btn, 2)

                # 递归
                self.switch_to_scene(scene)

        if scene_now == 4:
            # 探索内
            if scene == 3:
                # 点击退出探索
                self.click_until('退出按钮', 'img\\QUE-REN.png',
                                 *TansuoPos.quit_btn, 2)

                # 点击确认
                self.click_until('确认按钮', 'img\\QUE-REN.png',
                                 *TansuoPos.confirm_btn, 2, False)

                # 递归
                self.switch_to_scene(scene)
