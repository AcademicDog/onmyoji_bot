from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, YuhunPos
import tools.utilities as ut

import logging
import time


class DriverFighter(Fighter):
    '''御魂战斗司机程序，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Driver: ', emyc, hwnd)

    def start(self):
        '''单人御魂司机'''
        # 设定点击疲劳度
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # 战斗主循环

        while self.run:
            # 司机点击开始战斗，需要锁定御魂阵容
            self.log.writeinfo('Driver: 进入队伍')
            mood1.moodsleep()

            # 拒绝悬赏
            self.yys.rejectbounty()

            self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png',
                                 self.max_win_time)

            # 全部队员进入房间才开始
            if self.multiPassenger:
                start_time = time.time()
                timenotout = True
                while timenotout and self.run:
                    result = self.yys.find_game_img('img\\FANG-JIAN-YAO-QING.png')
                    result2 = self.yys.find_game_img('img\\FANG-JIAN-YAO-QING2.png')
                    if not (result or result2):
                        break
                    else:
                        self.log.writeinfo('有乘客未进入房间')
                        self.log.writeinfo(result)
                    time.sleep(0.5)
                    timenotout = time.time()-start_time <= self.max_op_time

                if not timenotout:
                    self.yys.activate_window()
                    time.sleep(5)
                    self.yys.quit_game()

            self.log.writeinfo('Driver: 点击开始战斗按钮')
            self.click_until('开始战斗按钮', 'img\\ZI-DONG.png', *
                             YuhunPos.kaishizhandou_btn, mood2.get1mood()/1000)
            self.log.writeinfo('Driver: 已进入战斗')

            # 已经进入战斗，乘客自动标记第二位式神
            self.click_shikigami()

            # 已经进入战斗，司机自动点怪
            self.click_monster()

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(ut.firstposition())
            start_time = time.time()
            jiesuan_status = 0
            while time.time() - start_time <= 20 and self.run:
                if(self.yys.wait_game_img('img\\XIE-ZHAN-DUI-WU.png', mood3.get1mood()/1000, False)):
                    break

                # 点击结算
                if jiesuan_status == 0:
                    if not (self.yys.find_game_img('img\\MESSAGE.png') or self.yys.find_game_img('img\\JIA-CHENG.png') or self.yys.find_game_img('img\\XIE-ZHAN-DUI-WU.png')):
                        self.yys.mouse_click_bg(*CommonPos.second_position)
                        self.log.writeinfo('Driver: 点击结算')
                    else:
                        jiesuan_status = 1
                        self.log.writeinfo('Driver: 点击结算成功，待进入队伍')

                # 点击默认邀请
                if self.yys.find_game_img('img\\ZI-DONG-YAO-QING.png'):
                    self.yys.mouse_click_bg((497, 319))
                    time.sleep(0.2)
                    self.yys.mouse_click_bg((674, 384))
                    self.log.writeinfo('Driver: 自动邀请')
