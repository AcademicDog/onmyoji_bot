from onmyoji import *
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QObject, pyqtSignal
from Ui_onmyoji import *
import logging

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

    def start_onmyoji(self):
        section = self.ui.tabWidget.currentIndex()
        if section == 0:
            # 御魂
            if mode == 0:
                # 单刷
                fight = single_fight.SingleFight()
    
            if mode == 2:
                # 司机
                fight = fighter_driver.DriverFighter()
    
            if mode == 3:
                # 乘客
                fight = fighter_passenger.FighterPassenger()
        
        elif section == 1:
            # 探索
            fight = explore.ExploreFight()

        self.task = threading.Thread(target = fight.start)
        self.task.start()

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
        logging.info('Quitting!')
        os._exit(0)

        print(self.ui.tabWidget.currentIndex())

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