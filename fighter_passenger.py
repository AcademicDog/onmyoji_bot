import time
import fighter
import utilities


class FighterPassenger(fighter.Fighter):
    '''御魂战斗乘客程序，参数mode, emyc'''

    def __init__(self, done = 1, emyc = 0):
        # 初始化
        fighter.Fighter.__init__(self, 'Passenger:', emyc)

    def start(self):
        '''单人御魂乘客'''
        # 设定点击疲劳度
        mood2 = utilities.Mood()
        mood3 = utilities.Mood(3)

        # 战斗主循环
        while True:
            # 检测是否进入战斗
            self.check_battle()

            # 已经进入战斗，乘客自动点怪
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
                if(self.yys.wait_game_img('img\\LI-KAI-DUI-WU.png', mood3.get1mood()/1000, False)):
                    self.log.writeinfo('Passenger: in team')
                    break

                # 点击自动接受邀请
                if(self.yys.wait_game_img('img\\ZI-DONG-JIE-SHOU.png', 0.1, False)):
                    self.yys.mouse_click_bg((210, 227))
                    self.log.writeinfo('Passenger: auto accepted')

                # 点击普通接受邀请
                elif(self.yys.wait_game_img('img\\JIE-SHOU.png', 0.1, False)):
                    self.yys.mouse_click_bg((125, 230))
                    self.log.writeinfo('Passenger: accepted')
