import time
import fighter
import utilities


class DriverFighter(fighter.Fighter):
    '''御魂战斗司机程序，参数mode, emyc'''

    def __init__(self, done = 1, emyc = 0):
        # 初始化
        fighter.Fighter.__init__(self, 'Driver:', emyc)

    def start(self):
        '''单人御魂司机'''
        # 设定点击疲劳度
        mood1 = utilities.Mood()
        mood2 = utilities.Mood()
        mood3 = utilities.Mood(3)

        # 战斗主循环
        while True:
            # 司机点击开始战斗，需要锁定御魂阵容
            self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png')
            mood1.moodsleep()
            self.yys.mouse_click_bg((857, 515), (998, 556))
            self.log.writeinfo('Driver: clicked KAI-SHI-ZHAN-DOU!')

            # 检测是否进入战斗
            self.check_battle()

            # 已经进入战斗，司机自动点怪
            self.click_monster()

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(utilities.firstposition())
            mood3.moodsleep()
            start_time = time.time()
            while time.time() - start_time <= 10:
                # 点击结算
                self.yys.mouse_click_bg(utilities.secondposition())
                if(self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png', mood3.get1mood()/1000, False)):
                    self.log.writeinfo('Driver: in team')
                    break

                # 点击默认邀请
                if(self.yys.wait_game_img('img\\ZI-DONG-YAO-QING.png', 0.2, False)):
                    self.yys.mouse_click_bg((497, 319))
                    time.sleep(0.2)
                    self.yys.mouse_click_bg((674, 384))
                    self.log.writeinfo('Driver: auto invited')
