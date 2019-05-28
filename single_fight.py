import threading

import fighter
import logsystem
import watchdog
import utilities

class SingleFight(fighter.Fighter):
    '''单人御魂战斗，参数mode, done, ts'''
    def __init__(self, done, ts, dog):
        #初始化
        self.log = logsystem.WriteLog()
        fighter.Fighter.__init__(self, ts)

        # 检测天使插件 COM Object 是否建立成功
        if(not self.ready):
            self.log.writewarning('Register failed')
            return 
        self.log.writeinfo('Register successful')

        # 绑定窗口
        self.hwnd = ts.FindWindow("", "阴阳师-网易游戏")
        if(not self.fighter_binding(ts, self.hwnd)):    
            self.log.writewarning('Binding failed')
            return 
        self.log.writeinfo('Binding successful')

        # 颜色 Debug 测试 
        self.fighter_test()
        self.log.writeinfo('Passed color debug')

        # 启动看门狗
        self.dog = dog
        self.dog.setdog(0, done, self.ts, self.hwnd)        

    def start(self):
        '''单人战斗主循环'''
        mood1 = utilities.Mood()
        mood2 = utilities.Mood()
        mood3 = utilities.Mood()
        post_pos = utilities.Position()
        while True:
            self.dog.feed()
            # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
            utilities.wtfc1(self.ts, 807, 442, "f3b25e", 807, 890, 442, 459, 0, 1, mood1.getmood())
            self.log.writeinfo('Already clicked TIAO-ZHAN')

            #wtfc1(ts, 1033, 576, "e6c78f", 1004, 1073, 465, 521, 0, 1)
            #print('already clicked ZHUN-BEI')

            # 检测是否进入战斗
            while True:
                utilities.rejxs(self.ts)                
                colib = self.ts.GetColor(71, 577)
                if colib == "f7f2df":
                    break
                utilities.mysleep(500)
            self.log.writeinfo("Now we are in the battle")

            # 在战斗中，自动点怪
            while True:
                utilities.rejxs(self.ts)                

                # 点击中间怪物
                if fighter.Fighter.emyc == 1:
                    utilities.crnd(self.ts, 509, 579, 153, 181)

                # 点击右边怪物
                elif fighter.Fighter.emyc == 2:
                    utilities.crnd(self.ts, 773, 856, 159, 190)

                mood2.moodsleep()

                utilities.rejxs(self.ts)
                colib = self.ts.GetColor(71, 577)
                if colib != "f7f2df":
                    break
            self.log.writeinfo("Battle finished")

            # 在战斗结算页面
            mood3.moodsleep()
            utilities.crnd(self.ts, *post_pos.get_firstpos())
            mood3.moodsleep()
            utilities.crnd(self.ts, *post_pos.get_secondpos())
            while True:                
                utilities.rejxs(self.ts)
                coljs = self.ts.GetColor(807, 442)
                if coljs == "f3b25e":
                    break
                utilities.crnd(self.ts, *post_pos.get_pos())
                mood3.moodsleep()
            self.log.writeinfo("back to YUHUN level selection")