from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, TansuoPos
import tools.utilities as ut

import logging
import time


class FighterPassenger(Fighter):
    '''御魂战斗乘客程序，参数mode, emyc'''

    def __init__(self, emyc=0, hwnd=0):
        # 初始化
        Fighter.__init__(self, 'Passenger: ', emyc, hwnd)

    def start(self):
        '''单人御魂乘客'''
        # 设定点击疲劳度
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # 战斗主循环
        while self.run:
            # 检测是否进入战斗
            self.check_battle()

            # 已经进入战斗，乘客自动标记第二位式神
            self.click_shikigami()

            # 已经进入战斗，乘客自动点怪
            self.click_monster()

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 等待下一轮
            self.yys.mouse_click_bg(ut.firstposition())
            start_time = time.time()
            jiesuan_status = 0
            while time.time() - start_time <= 20 and self.run:
                # 检测是否回到队伍中
                if(self.yys.wait_game_img('img\\XIE-ZHAN-DUI-WU.png', mood3.get1mood()/1000, False) or self.yys.find_game_img('img\\XIE-ZHAN-DUI-WU.png', 0, None, None, 1) or self.yys.find_game_img('img\\ZI-DONG.png')):
                    self.log.writeinfo('Passenger: 进入队伍')
                    break

                # 点击结算
                if jiesuan_status == 0:
                    if not (self.yys.find_game_img('img\\MESSAGE.png') or self.yys.find_game_img('img\\JIA-CHENG.png')):
                        self.yys.mouse_click_bg(*CommonPos.second_position)
                        self.log.writeinfo('Passenger: 点击结算')
                    else:
                        jiesuan_status = 1
                        self.log.writeinfo('Passenger: 点击结算成功，待进入队伍')

                # 检测是否有御魂邀请
                yuhun_loc = self.yys.wait_game_img(
                    'img\\YU-HUN.png', 0.1, False)
                if yuhun_loc:
                    # 点击自动接受邀请
                    if self.yys.find_game_img('img\\ZI-DONG-JIE-SHOU.png'):
                        self.yys.mouse_click_bg((210, yuhun_loc[1]))
                        self.log.writeinfo('Passenger: 自动接受邀请')

                    # 点击普通接受邀请
                    elif self.yys.find_game_img('img\\JIE-SHOU.png'):
                        self.yys.mouse_click_bg((125, yuhun_loc[1]))
                        self.log.writeinfo('Passenger: 接受邀请')
