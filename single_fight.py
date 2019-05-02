import fighter
import logsystem
import watchdog
import utilities


log = logsystem.WriteLog()

class SingleFight(fighter.Fighter):
    # 单人御魂
    def __init__(self, mode, done, ts):
        #初始化
        fighter.Fighter.__init__(self, ts)

        # 检测天使插件 COM Object 是否建立成功
        if(not self.ready):
            log.writewarning('Register failed')
            return 
        log.writeinfo('Register successful')

        # 绑定窗口
        if(not self.fighter_binding()):    
            log.writewarning('Binding failed')
            return 
        log.writeinfo('Binding successful')

        # 颜色 Debug 测试 
        self.fighter_test()
        log.writeinfo('Passed color debug')

        # 启动看门狗
        self.dog = watchdog.Watchdog()
        self.dog.setdog(mode, done, self.ts, self.hwnd)

    def start(self):
        # 御魂战斗主循环
        while True:
            self.dog.feed()
            # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
            utilities.wtfc1(self.ts, 807, 442, "f3b25e", 807, 881, 442, 459, 0, 1)
            log.writeinfo('Already clicked TIAO-ZHAN')

            #wtfc1(ts, 1033, 576, "e6c78f", 1004, 1073, 465, 521, 0, 1)
            #print('already clicked ZHUN-BEI')

            # 检测是否进入战斗
        while True:
            utilities.rejxs(self.ts)
            self.dog.dog_response()
            colib = self.ts.GetColor(71, 577)
            if colib == "f7f2df":
                break
            utilities.mysleep(500)
        log.writeinfo("Now we are in the battle")

        # 在战斗中，自动点怪
        while True:
          utilities.rejxs(self.ts)
          self.dog.dog_response()

          # 点击中间怪物
          if fighter.Fighter.emyc == 1:
            utilities.crnd(self.ts, 509, 579, 153, 181)

          # 点击右边怪物
          elif fighter.Fighter.emyc == 2:
            utilities.crnd(self.ts, 773, 856, 159, 190)

          utilities.mysleep(500, 500)

          utilities.rejxs(self.ts)
          colib = self.ts.GetColor(71, 577)
          if colib != "f7f2df":
              break
        log.writeinfo("Battle finished")

        # 在战斗结算页面
        while True: 
          self.dog.dog_response()
          utilities.rejxs(self.ts)
          utilities.crnd(self.ts, 980, 1030, 225, 275)

          coljs = self.ts.GetColor(807, 442)
          if coljs == "f3b25e":
              break
          utilities.mysleep(500, 500)
        log.writeinfo("back to YUHUN level selection")