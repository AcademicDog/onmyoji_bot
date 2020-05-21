from explore.explore import ExploreFight
from tools.game_pos import CommonPos, TansuoPos
import tools.utilities as ut

import configparser
import logging
import random
import time


class PassengerExploreFight(ExploreFight):
    def __init__(self):
        # 初始化
        ExploreFight.__init__(self)
        self.mode = 3

    def start(self):
        '''乘客探索主循环'''
        mood1 = ut.Mood(2)
        mood2 = ut.Mood(2)
        while self.run:
            # 进入探索内
            self.log.writeinfo('开始本轮探索')

            while True:

                if self.yys.find_game_img('img\\ZHUN-BEI.png'):
                    self.log.writeinfo('已进入战斗')
                    time.sleep(1)

                # 等待式神准备
                # self.yys.wait_game_color(((1024,524),(1044, 544)), (138,198,233), 30)
                logging.info('式神准备完成')

                # 检查狗粮经验
                self.check_exp_full()

                # 点击准备，直到进入战斗
                self.click_until('准备按钮', 'img\\ZI-DONG.png', *
                                 TansuoPos.ready_btn, mood1.get1mood()/1000)

                # 检查是否打完
                self.check_end()
                mood1.moodsleep()

                # 在战斗结算页面
                self.yys.mouse_click_bg(ut.firstposition())
                self.click_until('结算', 'img\\JIN-BI.png',
                                 *CommonPos.second_position, mood2.get1mood()/1000)
                self.click_until('结算', 'img/JIN-BI.png',
                                 *CommonPos.second_position, mood2.get1mood()/1000, False)




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