from explore.explore import ExploreFight
from goryou.single_fight import GoryouFight
from mitama.dual import DualFighter
from mitama.fighter_driver import DriverFighter
from mitama.fighter_passenger import FighterPassenger
from mitama.single_fight import SingleFight

import configparser
import ctypes
import logging
import os
import sys
import tools.logsystem


def init():
    conf = configparser.ConfigParser()
    # 读取配置文件
    conf.read('conf.ini', encoding="utf-8")

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
        fight = ExploreFight()

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
    logging.info('python version: %s', sys.version)

    try:
        # 检测管理员权限
        if is_admin():
            # 注册插件，获取权限
            sys.excepthook = my_excepthook
            logging.info('UAC pass')

            # Query DPI Awareness (Windows 10 and 8)
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(
                0, ctypes.byref(awareness))

            # Set DPI Awareness  (Windows 10 and 8)
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(0)

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
