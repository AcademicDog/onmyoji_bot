from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, YuhunPos
from tools.logsystem import MyLog
import tools.utilities as ut

import time


class DriverFighter(Fighter):
    '''御魂战斗司机程序，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, emyc, hwnd)
        self.log = MyLog.dlogger

    def start(self):
        '''单人御魂司机'''
        # 设定点击疲劳度
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # 战斗主循环
        self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png',
                               self.max_win_time)
        while self.run:
            # 司机点击开始战斗，需要锁定御魂阵容
            mood1.moodsleep()
            self.log.info('Driver: 点击开始战斗按钮')
            self.click_until('开始战斗按钮', 'img\\KAI-SHI-ZHAN-DOU.png', *
                             YuhunPos.kaishizhandou_btn, mood2.get1mood()/1000, False)
            
            # 检测是否进入战斗
            self.check_battle()

            # 在战斗中，标记己方式神
            self.mitama_team_click()

            # 已经进入战斗，司机自动点怪
            self.click_monster()

            # 检测是否打完
            state = self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.get_reward(mood3, state)

            # 等待下一轮
            self.log.info('Driver: 等待下一轮')
            start_time = time.time()
            while time.time() - start_time <= 20 and self.run:
                if(self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png', 1, False)):
                    self.log.info('Driver: 进入队伍')
                    break

                # 点击默认邀请
                if self.yys.find_game_img('img\\ZI-DONG-YAO-QING.png'):
                    self.yys.mouse_click_bg((497, 319))
                    time.sleep(0.2)
                    self.yys.mouse_click_bg((674, 384))
                    self.log.info('Driver: 自动邀请')

            # 检查游戏次数
            self.check_times()
