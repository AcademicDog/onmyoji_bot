import threading
import win32com.client 

import utilities
import logsystem
import watchdog

# 参数
col_zidong = 'f7f2df'                       # 自动旋钮颜色
pos_zidong = (71, 577)                      # 自动旋钮位置

pos_middle_monster = (509, 579, 153, 181)   # 中间怪位置
pos_right_monster = (773, 856, 159, 190)    # 右边怪位置

class Fighter:

    def __init__(self, emyc = 0):
        self.ts = win32com.client.Dispatch("ts.tssoft")
        self.log = logsystem.WriteLog()
        # 检测天使插件 COM Object 是否建立成功
        need_ver = '4.019'
        if(self.ts.ver() != need_ver):
            self.log.writewarning('Register failed')
        self.log.writeinfo('Register successful')
        self.emyc = emyc

    def fighter_binding(self, hwnd):
        # 绑定窗口
        self.hwnd = hwnd
        ts_ret = self.ts.BindWindow(hwnd, 'dx2', 'windows', 'windows', 0)
        if(ts_ret != 1):
            self.log.writewarning('Binding failed')
            return
        utilities.mysleep(2000)
        self.log.writeinfo('Binding successful')

    def fighter_test(self):
        # 颜色 Debug 测试 
        while True:
            tscoldebug = self.ts.GetColor(1, 1)
            if tscoldebug != "000000" and tscoldebug != "ffffff":
                self.log.writeinfo('Passed color debug')
                return
            utilities.mysleep(500)

    def watchdog(self, mode, done, ts, hwnd):
        self.dog = watchdog.Watchdog()
        self.dog.setdog(mode, done, ts, hwnd)
        t = threading.Thread(target = self.dog.bark)
        t.start()
        self.log.writeinfo("Watchdog registered")

    def check_battle(self):
        # 检测是否进入战斗
        while True:
            utilities.rejxs(self.ts)                
            colib = self.ts.GetColor(*pos_zidong)
            if colib == col_zidong:
                break
            utilities.mysleep(500)
        self.log.writeinfo("Now we are in the battle")

    def click_monster(self):
        # 点击怪物        
        if self.emyc == 1:
            # 点击中间怪物
            utilities.crnd(self.ts, *pos_middle_monster)

        elif self.emyc == 2:
            # 点击右边怪物                
            utilities.crnd(self.ts, *pos_right_monster)