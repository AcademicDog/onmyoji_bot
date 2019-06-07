import threading

import fighter
import watchdog
import utilities

class SingleFight(fighter.Fighter):
    '''单人御魂战斗，参数done, emyc'''
    def __init__(self, done, emyc):
        #初始化
        fighter.Fighter.__init__(self, emyc)

        # 绑定窗口
        hwnd = self.ts.FindWindow("", "阴阳师-网易游戏")
        self.fighter_binding(hwnd)

        # 启动看门狗
        self.watchdog(0, done, self.ts, self.hwnd)

    def start(self):
        '''单人战斗主循环'''
        mood1 = utilities.Mood()
        mood2 = utilities.Mood()
        mood3 = utilities.Mood()
        post_pos = utilities.Position()
        while True:
            # 喂狗
            self.dog.feed()

            # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
            utilities.wtfc1(self.ts, 807, 442, "f3b25e", 807, 890, 442, 459, 0, 1, mood1.getmood())
            self.log.writeinfo('Already clicked TIAO-ZHAN')

            #wtfc1(ts, 1033, 576, "e6c78f", 1004, 1073, 465, 521, 0, 1)
            #print('already clicked ZHUN-BEI')

            # 检测是否进入战斗
            self.check_battle()

            # 在战斗中，自动点怪
            while True:
                utilities.rejxs(self.ts)

                # 点怪
                self.click_monster()

                mood2.moodsleep()

                utilities.rejxs(self.ts)

                # 检测是否打完
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