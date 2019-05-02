import time
import logsystem
import os

class Watchdog:
    #时间，新 旧
    lastime = [0, 0]

    def __init__(self):
        Watchdog.lastime[1] = time.time()
        self.log = logsystem.WriteLog()

    def setdog(self, mode, done, ts, hwnd):
        Watchdog.mode = mode
        Watchdog.done = done
        Watchdog.ts = ts
        Watchdog.hwnd = hwnd

    def feed(self):
        Watchdog.lastime[1] = time.time()

    def bark(self):
        Watchdog.lastime[0] = time.time()
        period = int(Watchdog.lastime[0] - Watchdog.lastime[1])
        if(period > 10):
            return 1
        else:
            return 0

    def clean(self):
        #退出并清理窗口
        if(self.done==2):
            self.log.writewarning('Attention, shutdown in 60 s')
            os.system("shutdown -s -t  60 ")
        elif(self.done==1):
            if(self.mode==0):
                self.log.writewarning('Attention, one window will be colsed')
                self.ts.SetWindowState(self.hwnd,13)
            elif(self.mode==1):
                self.log.writewarning('Attention, two windows will be colsed')
                self.ts[0].SetWindowState(self.hwnd[0],13)
                self.ts[1].SetWindowState(self.hwnd[1],13)
            os._exit(0)
        elif(self.done==0):
            os._exit(0)

    def dog_response(self):
        if(self.bark() == 1):
            self.log.writewarning("Dog barked!")
            self.clean()