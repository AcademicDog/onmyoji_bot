from explore.explore import ExploreFight
from tools.game_pos import CommonPos, TansuoPos
import tools.utilities as ut

import configparser
import logging
import random
import time


class DriverExploreFight(ExploreFight):
    def __init__(self):
        # 初始化
        ExploreFight.__init__(self)
        self.mode = 2

    def start(self):
        '''司机探索主循环'''
        mood1 = ut.Mood(2)
        mood2 = ut.Mood(3)
        while self.run:
            # 进入探索内
            self.log.writeinfo('开始本轮探索')

            # 开始打怪
            i = 0
            while self.run:
                if i >= 4:
                    break
                result = self.fight_moster(mood1, mood2)
                if result == 1:
                    continue
                elif result == 2:
                    break
                else:
                    self.log.writeinfo('移动至下一个场景')
                    self.next_scene()
                    i += 1

            # 退出探索
            if result == 2:
                self.click_box()
            else:
                self.switch_to_scene(3)

            self.log.writeinfo('结束本轮探索')
            time.sleep(0.5)

            # 邀请好友
            if self.yys.wait_game_img('img\\YAO-QING.png', self.max_op_time):
                # 点击确认
                self.click_until('确认按钮', 'img\\YAO-QING.png',
                                             *TansuoPos.confirm_btn, 2, False)