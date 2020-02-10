from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_onmyoji import Ui_MainWindow

import configparser
import ctypes
import logging
import os
import subprocess
import sys
import tools.logsystem


def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.conf = configparser.ConfigParser()

    def set_conf(self):
        '''
        设置参数至配置文件
        '''
        # 运行参数
        section = self.ui.tabWidget.currentIndex()
        self.conf.set('DEFAULT', 'run_section', str(section))

        # 一般参数
        self.conf.set('watchdog', 'watchdog_enable',
                      str(self.ui.checkBox.isChecked()))
        self.conf.set('watchdog', 'max_win_time', str(self.ui.lineEdit.text()))
        self.conf.set('watchdog', 'max_op_time',
                      str(self.ui.lineEdit_2.text()))

        self.conf.set('others', 'debug_enable', str(
            self.ui.checkBox_4.isChecked()))

        # 御魂参数
        if self.ui.mitama_single.isChecked():
            # 单刷
            self.conf.set('DEFAULT', 'run_mode', '0')

        elif self.ui.mitama_driver.isChecked():
            # 司机
            self.conf.set('DEFAULT', 'run_mode', '1')

        elif self.ui.mitama_passenger.isChecked():
            # 乘客
            self.conf.set('DEFAULT', 'run_mode', '2')

        elif self.ui.mitama_dual.isChecked():
            # 双开
            self.conf.set('DEFAULT', 'run_mode', '3')

        # 探索参数
        self.conf.set('explore', 'fight_boss_enable',
                      str(self.ui.checkBox_2.isChecked()))
        self.conf.set('explore', 'slide_shikigami',
                      str(self.ui.checkBox_3.isChecked()))
        self.conf.set('explore', 'slide_shikigami_progress',
                      str(self.ui.horizontalSlider.value()))
        self.conf.set('explore', 'zhunbei_delay',
                      str(self.ui.lineEdit_3.text()))
        self.conf.set('explore', 'change_shikigami',
                      str(self.ui.comboBox.currentIndex()))

    def get_conf(self):
        # 添加配置
        try:
            self.conf.add_section('watchdog')
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
        # 读取主要副本
        self.get_conf()

        subprocess.Popen("cmd.exe /c start onmyoji.exe")
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
            sys.excepthook = my_excepthook

            # 设置战斗参数
            app = QApplication(sys.argv)
            myWin = MyMainWindow()
            myWin.show()
            sys.exit(app.exec_())

        else:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, __file__, None, 1)
    except:
        pass
