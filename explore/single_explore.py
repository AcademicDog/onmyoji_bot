from explore.explore import ExploreFight
from tools.game_pos import CommonPos, TansuoPos
import tools.utilities as ut

import configparser
import logging
import random
import time


class SingleExploreFight(ExploreFight):
    def __init__(self):
        # 初始化
        ExploreFight.__init__(self)
        self.mode = 0

    def start(self):
        '''单人探索主循环'''
        mood1 = ut.Mood(1)
        mood2 = ut.Mood(2)
        while self.run:
            # 进入探索内
            self.switch_to_scene(4)

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
            if self.run:
                if result == 2:
                    self.click_box()
                else:
                    self.switch_to_scene(3)

            self.log.writeinfo('结束本轮探索')
            time.sleep(0.5)