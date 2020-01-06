from explore.explore import ExploreFight
from goryou.single_fight import GoryouFight
from mitama.dual import DualFighter
from mitama.fighter_driver import DriverFighter
from mitama.fighter_passenger import FighterPassenger
from mitama.single_fight import SingleFight
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal
from Ui_onmyoji import Ui_MainWindow

import configparser
import ctypes
import logging
import os
import sys
import threading


def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


class GuiLogger(logging.Handler):
    def emit(self, record):
        # implementation of append_line omitted
        self.edit.append(self.format(record))
        self.edit.moveCursor(QTextCursor.End)


class MyMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.textEdit.ensureCursorVisible()

        h = GuiLogger()
        h.edit = self.ui.textEdit
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(h)

    def set_conf(self, conf, section):
        '''
        设置参数至配置文件
        '''
        # 一般参数
        conf.set('watchdog', 'watchdog_enable',
                 str(self.ui.checkBox.isChecked()))
        conf.set('watchdog', 'max_win_time', str(self.ui.lineEdit.text()))
        conf.set('watchdog', 'max_op_time', str(self.ui.lineEdit_2.text()))

        conf.set('others', 'debug_enable', str(self.ui.checkBox_4.isChecked()))

        # 御魂参数
        if section == 0:
            pass

        # 探索参数
        if section == 1:
            # 探索
            conf.set('explore', 'fight_boss_enable',
                     str(self.ui.checkBox_2.isChecked()))
            conf.set('explore', 'slide_shikigami',
                     str(self.ui.checkBox_3.isChecked()))
            conf.set('explore', 'slide_shikigami_progress',
                     str(self.ui.horizontalSlider.value()))
            conf.set('explore', 'zhunbei_delay',
                     str(self.ui.lineEdit_3.text()))

    def get_conf(self, section):
        conf = configparser.ConfigParser()
        # 读取配置文件
        conf.read('conf.ini', encoding="utf-8")

        # 修改配置
        try:
            self.set_conf(conf, section)
        except:
            conf.add_section('watchdog')
            conf.add_section('explore')
            conf.add_section('others')
            self.set_conf(conf, section)

        # 保存配置文件
        with open('conf.ini', 'w') as configfile:
            conf.write(configfile)

    def start_onmyoji(self):
        section = self.ui.tabWidget.currentIndex()

        # 读取主要副本
        self.get_conf(section)

        if section == 0:
            # 御魂
            if self.ui.mitama_single.isChecked():
                # 单刷
                self.fight = SingleFight()

            elif self.ui.mitama_driver.isChecked():
                # 司机
                self.fight = DriverFighter()

            if self.ui.mitama_passenger.isChecked():
                # 乘客
                self.fight = FighterPassenger()

            if self.ui.mitama_dual.isChecked():
                # 双开
                self.fight = DualFighter()

        elif section == 1:
            # 御灵
            self.fight = GoryouFight()

        elif section == 2:
            # 探索
            self.fight = ExploreFight()

        task = threading.Thread(target=self.fight.start)
        task.start()

    def stop_onmyoji(self):
        try:
            self.fight.deactivate()
        except:
            pass


def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' %(exc_type.__name__, exc_value)

    logging.error(msg)


if __name__ == "__main__":

    try:
        # 检测管理员权限
        if is_admin():
            sys.excepthook = my_excepthook
            global mode
            mode = 0
            global section
            section = 0

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
