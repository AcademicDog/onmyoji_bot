from explore.explore import ExploreFight
from tools.game_pos import TansuoPos
from tools.logsystem import MyLog
import tools.utilities as ut

import time


class ExplorePassenger(ExploreFight):
    '''
    组队探索队员
    '''

    def __init__(self, hwnd=0):
        '''
        初始化
        '''
        ExploreFight.__init__(self, hwnd=hwnd)
        self.log = MyLog.plogger
        self.start_time = time.time()

    def start(self):
        '''
        开始战斗
        '''
        mood = ut.Mood(3)
        mood1 = ut.Mood(3)
        scene = self.get_scene()
        if scene == 4:
            self.log.info('已进入探索，就绪')
        else:
            self.log.warning('请检查是否进入探索内，退出')
            return

        while self.run:
            # 检测当前场景
            maxVal_list, _ = self.yys.find_multi_img(
                'img/DUI.png', 'img/YING-BING.png')
            # print(maxVal_list)
            if maxVal_list[0] < 0.8 and maxVal_list[1] > 0.8:
                self.start_time = time.time()

                # 队长退出，则跟着退出
                self.log.info('队长已退出，跟随退出')
                self.switch_to_scene(3)

                # 等待邀请
                js_loc = self.yys.wait_game_img(
                    'img/JIE-SHOU.png', self.max_win_time)
                if js_loc:
                    # 点击接受邀请
                    if self.yys.find_game_img('img/JIE-SHOU.png'):
                        self.click_until('接受邀请', 'img/JIE-SHOU.png', (127, js_loc[1]+34), appear=False)
                        self.log.info('接受邀请')

                # 检查游戏次数
                self.check_times()

            elif maxVal_list[0] > 0.8 and maxVal_list[1] < 0.8:
                self.start_time = time.time()

                # 进入战斗，等待式神准备
                self.yys.wait_game_img_knn('img/ZHUN-BEI.png', thread=30)
                self.log.info('式神准备完成')

                # 检查狗粮经验
                self.check_exp_full()

                # 点击准备，直到进入战斗
                self.click_until_knn('准备按钮', 'img/ZHUN-BEI.png', *
                            TansuoPos.ready_btn, mood1.get1mood()/1000, False, thread=30)

                # 检测是否打完
                state = self.check_end()
                mood.moodsleep()

                # 点击结算
                self.get_reward(mood, state)

            else:
                # 其他，不做任何操作
                time.sleep(0.5)
                if time.time() - self.start_time > self.max_win_time:
                    self.yys.quit_game()
