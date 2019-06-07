import utilities
import logsystem

class Fighter:

    def __init__(self, ts, emyc = 0):
        self.log = logsystem.WriteLog()
        # 检测天使插件 COM Object 是否建立成功
        need_ver = '4.019'
        if(ts.ver() != need_ver):
            self.log.writewarning('Register failed')
        self.log.writeinfo('Register successful')
        self.ts = ts
        self.emyc = emyc

    def fighter_binding(self, ts, hwnd):
        # 绑定窗口        
        ts_ret = self.ts.BindWindow(hwnd, 'dx2', 'windows', 'windows', 0)
        if(ts_ret != 1):
            return 0
        utilities.mysleep(2000)
        return 1

    def fighter_test(self):
        # 颜色 Debug 测试 
        while True:
            tscoldebug = self.ts.GetColor(1, 1)
            if tscoldebug != "000000" and tscoldebug != "ffffff":
                self.log.writeinfo('Passed color debug')
                return
            utilities.mysleep(500)