from gameLib.game_ctl import GameControl
from explore.explore_leader import ExploreLeader
from explore.explore_passenger import ExplorePassenger

import logging
import threading
import win32gui

hwndlist = []


def get_all_hwnd(hwnd, mouse):
    '''
    获取所有阴阳师窗口
    '''
    if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd) and win32gui.IsWindowVisible(hwnd):
        if win32gui.GetWindowText(hwnd) == u'阴阳师-网易游戏':
            hwndlist.append(hwnd)


def get_game_hwnd():
    win32gui.EnumWindows(get_all_hwnd, 0)


class ExploreDual():
    def __init__(self):
        # 初始化窗口信息
        get_game_hwnd()
        self.hwndlist = hwndlist

        # 检测窗口信息是否正确
        num = len(self.hwndlist)
        if num == 2:
            logging.info('检测到两个窗口，窗口信息正常')
        else:
            logging.warning('检测到'+str(num)+'个窗口，窗口信息异常！')

        # 初始化司机和打手
        for hwnd in hwndlist:
            yys = GameControl(hwnd)
            if yys.find_game_img('img/DUI.png', 1, (68, 242), (135, 306), thread=0.8):
                self.driver = ExploreLeader(hwnd=hwnd, delay=True)
                hwndlist.remove(hwnd)
                logging.info('发现队长')
                break
        self.passenger = ExplorePassenger(hwnd=hwndlist[0])
        logging.info('发现乘客')

    def start(self):
        task1 = threading.Thread(target=self.driver.start)
        task2 = threading.Thread(target=self.passenger.start)
        task1.start()
        task2.start()

        task1.join()
        task2.join()

    def deactivate(self):
        self.hwndlist = []
        self.driver.deactivate()
        self.passenger.deactivate()
