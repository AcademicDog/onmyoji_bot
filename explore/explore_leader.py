from explore.explore import ExploreFight
from tools.game_pos import TansuoPos
import tools.utilities as ut
from tools.logsystem import MyLog

import random
import time


class ExploreLeader(ExploreFight):
    '''
    组队探索队长
    '''

    def __init__(self, hwnd=0, delay=False):
        '''
        初始化
            :param hwnd=0: 指定窗口句柄：0-否；其他-窗口句柄
            :param mode=0: 狗粮模式：0-正常模式，1-组队后排狗粮
            :param delay=False: 完成一轮探索后，是否等待1s再邀请下一轮
        '''
        ExploreFight.__init__(self, hwnd=hwnd, mode=1)
        self.delay = delay
        self.log = MyLog.dlogger

    def prev_scene(self):
        '''
        滑动到前一页面
        '''
        x0 = random.randint(510, 1126)
        x1 = x0 - 500
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x1, y1), (x0, y0))

    def start(self):
        '''
        开始战斗
        '''
        mood1 = ut.Mood(3)
        mood2 = ut.Mood(3)
        mood3 = ut.Mood()
        scene = self.get_scene()
        if scene == 4:
            self.log.info('已进入探索，就绪')
        else:
            self.log.warning('请检查是否进入探索内，退出')
            return

        while self.run:
            # 检测当前场景
            maxVal_list, maxLoc_list = self.yys.find_multi_img(
                'img/DUI.png', 'img/YING-BING.png')
            if maxVal_list[0] < 0.8 and maxVal_list[1] > 0.8:
                # 队长退出，结束
                self.log.warning('队员已退出，脚本结束')
                self.yys.quit_game()

            # 开始打怪
            i = 0
            ok = False
            while self.run:
                if i >= 4:
                    break
                result = self.fight_moster(mood1, mood2)
                if result == 1:
                    ok = True
                    continue
                elif result == 2:
                    break
                else:
                    self.log.info('移动至下一个场景')
                    self.next_scene()
                    i += 1

            if not ok:
                # 没有经验怪，随便打一个
                fight_pos = self.yys.find_game_img('img/FIGHT.png')
                while not fight_pos:
                    self.prev_scene()
                    fight_pos = self.yys.find_game_img('img/FIGHT.png')
                # 攻击怪
                self.yys.mouse_click_bg(fight_pos)
                self.log.info('已进入战斗')

                # 等待式神准备
                self.yys.wait_game_img_knn('img/ZHUN-BEI.png', thread=30)
                self.log.info('式神准备完成')

                # 检查狗粮经验
                self.check_exp_full()

                # 点击准备，直到进入战斗
                self.click_until_knn('准备按钮', 'img/ZHUN-BEI.png', *
                                     TansuoPos.ready_btn, mood1.get1mood()/1000, False, 30)

                # 检查是否打完
                state = self.check_end()
                mood1.moodsleep()

                # 在战斗结算页面
                self.get_reward(mood2, state)

            # 退出探索
            self.log.info('结束本轮探索')
            # 点击退出探索
            self.click_until_multi('退出按钮', 'img/QUE-REN.png', 'img/TAN-SUO.png', 'img/JUE-XING.png',
                                   pos=TansuoPos.quit_btn[0], pos_end=TansuoPos.quit_btn[1], step_time=0.5)

            # 点击确认
            self.click_until('确认按钮', 'img/QUE-REN.png',
                             *TansuoPos.confirm_btn, 2, False)

            # 等待司机退出1s
            if self.delay:
                time.sleep(1)

            # 下一轮自动邀请
            self.yys.wait_game_img('img/QUE-DING.png', self.max_win_time)
            time.sleep(0.5)
            self.click_until('继续邀请', 'img/QUE-DING.png', *
                             TansuoPos.yaoqing_comfirm, mood3.get1mood()/1000, False)

            # 检查游戏次数
            self.check_times()
