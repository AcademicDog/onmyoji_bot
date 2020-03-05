from gui.tkui import Application
from tools.logsystem import MyLog

import configparser
import ctypes
import logging
import os
import subprocess
import sys
import tkinter as tk


def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class MyBattle(Application):
    def __init__(self, master):
        Application.__init__(self, master)
        self.conf = configparser.ConfigParser()

    def set_conf(self):
        '''
        设置参数至配置文件
        '''
        # 运行参数
        self.conf.set('DEFAULT', 'client', str(self.client.current()))
        section = self.section.index('current')
        self.conf.set('DEFAULT', 'run_section', str(section))

        # 一般参数
        self.conf.set('watchdog', 'watchdog_enable',
                      str(self.watchdog_enable.get()))
        self.conf.set('watchdog', 'max_win_time', str(self.max_win_time.get()))
        self.conf.set('watchdog', 'max_op_time',
                      str(self.max_op_time.get()))

        self.conf.set('others', 'debug_enable', str(
            self.debug_enable.get()))

        # 御魂参数
        self.conf.set('DEFAULT', 'run_mode', str(self.run_mode.get()))
        self.conf.set('DEFAULT', 'max_times', str(self.max_times.get()))
        self.conf.set('DEFAULT', 'end_operation',
                      str(self.end_operation.current()))
        self.conf.set('mitama', 'run_submode', str(self.run_submode.get()))
        self.conf.set('mitama', 'mitama_team_mark',
                      str(self.mitama_team_mark.current()))

        # 探索参数
        self.conf.set('explore', 'explore_mode', str(self.explore_mode.get()))
        self.conf.set('explore', 'gouliang', str(self.gouliang))
        self.conf.set('explore', 'gouliang_b', str(self.gouliang_b))
        self.conf.set('explore', 'fight_boss_enable',
                      str(self.fight_boss_enable.get()))
        self.conf.set('explore', 'slide_shikigami',
                      str(self.slide_shikigami.get()))
        self.conf.set('explore', 'slide_shikigami_progress',
                      str(self.slide_shikigami_progress.get()))
        self.conf.set('explore', 'change_shikigami',
                      str(self.cmb.current()))

    def get_conf(self):
        # 添加配置
        try:
            self.conf.add_section('watchdog')
            self.conf.add_section('mitama')
            self.conf.add_section('explore')
            self.conf.add_section('others')
        except:
            pass

        # 修改配置
        self.set_conf()

        # 保存配置文件
        with open('conf.ini', 'w') as configfile:
            self.conf.write(configfile)

    def start_onmyoji(self):
        # 显示参数
        self.show_params()

        # 读取主要副本
        self.get_conf()

        subprocess.Popen("cmd.exe /c start Core.exe")
        # os.system("onmyoji.exe")

    def stop_onmyoji(self):
        os._exit(0)


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
            logging.info('获取管理员权限')

            # Query DPI Awareness (Windows 10 and 8)
            awareness = ctypes.c_int()
            errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(
                0, ctypes.byref(awareness))

            # Set DPI Awareness  (Windows 10 and 8)
            errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)
            # the argument is the awareness level, which can be 0, 1 or 2:
            # for 1-to-1 pixel control I seem to need it to be non-zero (I'm using level 2)

            # Set DPI Awareness  (Windows 7 and Vista)
            success = ctypes.windll.user32.SetProcessDPIAware()
            # behaviour on later OSes is undefined, although when I run it on my Windows 10 machine, it seems to work with effects identical to SetProcessDpiAwareness(1)

            # 设置战斗参数
            root = tk.Tk()
            app = MyBattle(root)
            app.mainloop()

        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
    except:
        pass
