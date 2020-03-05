from explore.explore import ExploreFight
from explore.explore_passenger import ExplorePassenger
from explore.explore_leader import ExploreLeader
from explore.explore_dual import ExploreDual
from goryou.single_fight import GoryouFight
from mitama.dual import DualFighter
from mitama.fighter_driver import DriverFighter
from mitama.fighter_passenger import FighterPassenger
from mitama.single_fight import SingleFight
from tools.logsystem import MyLog

import configparser
import ctypes
import logging
import os
import sys


def init():
    conf = configparser.ConfigParser()
    # 读取配置文件
    conf.read('conf.ini', encoding="utf-8")

    # 设置缩放
    # Query DPI Awareness (Windows 10 and 8)
    awareness = ctypes.c_int()
    errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(
        0, ctypes.byref(awareness))

    # Set DPI Awareness  (Windows 10 and 8)
    client = conf.getint('DEFAULT', 'client')
    if client == 0:
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(0)
    else:
        errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)

    # 读取主要副本
    section = conf.getint('DEFAULT', 'run_section')

    if section == 0:
        # 御魂
        mode = conf.getint('DEFAULT', 'run_mode')
        if mode == 0:
            # 单刷
            fight = SingleFight()

        elif mode == 1:
            # 司机
            fight = DriverFighter()

        elif mode == 2:
            # 乘客
            fight = FighterPassenger()

        elif mode == 3:
            # 双开
            fight = DualFighter()

    elif section == 1:
        # 御灵
        fight = GoryouFight()

    elif section == 2:
        # 探索
        mode = conf.getint('explore', 'explore_mode')
        if mode == 0:
            # 单刷
            fight = ExploreFight()
        elif mode == 1:
            # 单人队长
            fight = ExploreLeader()
        elif mode == 2:
            # 单人队员
            fight = ExplorePassenger()
        elif mode == 3:
            # 双开
            fight = ExploreDual()

    fight.start()


def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (
            filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' % (exc_type.__name__, exc_value)

    logging.error(msg)


if __name__ == "__main__":
    try:
        # 检测管理员权限
        if is_admin():
            # 初始化日志
            MyLog.init()

            # 错误消息进日志
            sys.excepthook = my_excepthook
            logging.info('UAC pass')

            # 设置战斗参数
            init()

        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
    except KeyboardInterrupt:
        logging.info('terminated')
        os._exit(0)
    else:
        pass
