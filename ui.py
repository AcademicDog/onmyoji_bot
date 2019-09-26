from explore.explore import ExploreFight
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
        self.edit.append(self.format(record))  # implementation of append_line omitted
        self.edit.moveCursor(QTextCursor.End)

class MyMainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MyMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.textEdit.ensureCursorVisible()
        
        h = GuiLogger()
        h.edit = self.ui.textEdit
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.addHandler(h)

    def set_conf(self, conf):
        '''
        设置参数至配置文件
        '''
        conf.set('watchdog', 'watchdog_enable',
                 str(self.ui.checkBox.isChecked()))
        conf.set('watchdog', 'max_win_time', str(self.ui.lineEdit.text()))
        conf.set('watchdog', 'max_op_time', str(self.ui.lineEdit_2.text()))
        conf.set('explore', 'fight_boss_enable',
                 str(self.ui.checkBox_2.isChecked()))
    
    def get_conf(self):
        conf = configparser.ConfigParser()
        # 读取配置文件
        conf.read('conf.ini')

        # 修改配置
        try:
            self.set_conf(conf)
        except:
            conf.add_section('watchdog')
            conf.add_section('explore')
            self.set_conf(conf)

        # 保存配置文件
        with open('conf.ini', 'w') as configfile:
                conf.write(configfile)

    def start_onmyoji(self):
        # 读取配置
        self.get_conf()

        section = self.ui.tabWidget.currentIndex()
        if section == 0:
            # 御魂
            if mode == 0:
                # 单刷
                self.fight = SingleFight()
    
            if mode == 2:
                # 司机
                self.fight = DriverFighter()
    
            if mode == 3:
                # 乘客
                self.fight = FighterPassenger()
        
        elif section == 1:
            # 探索
            self.fight = ExploreFight()

        task = threading.Thread(target = self.fight.start)
        task.start()

    def set_mood1(self):
        global mode
        mode = 0

    def set_mood2(self):
        global mode
        mode = 2

    def set_mood3(self):
        global mode
        mode = 3

    def stop_onmyoji(self):
        try:
            self.fight.deactivate()
        except:
            pass

if __name__=="__main__":  
    
    try:
        # 检测管理员权限
        if is_admin():
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
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    except:
        pass
