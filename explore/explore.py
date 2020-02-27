from gameLib.fighter import Fighter
from tools.game_pos import TansuoPos
import tools.utilities as ut

import configparser
import logging
import random
import time


class ExploreFight(Fighter):
    def __init__(self):
        # 初始化
        Fighter.__init__(self)

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.fight_boss_enable = conf.getboolean(
            'explore', 'fight_boss_enable')
        self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        self.slide_shikigami_progress = conf.getint(
            'explore', 'slide_shikigami_progress')
        self.change_shikigami = conf.getint('explore', 'change_shikigami')

    def next_scene(self):
        '''
        移动至下一个场景，每次移动400像素
        '''
        x0 = random.randint(510, 1126)
        x1 = x0 - 500
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))

    def check_exp_full(self):
        '''
        检查狗粮经验，并自动换狗粮
        '''
        # 狗粮经验判断, gouliang1是中间狗粮，gouliang2是右边狗粮
        gouliang1 = self.yys.find_game_img(
            'img\\MAN1.png', 1, *TansuoPos.gouliang_middle, 1)
        gouliang2 = self.yys.find_game_img(
            'img\\MAN2.png', 1, *TansuoPos.gouliang_right, 1)

        # print(gouliang1)
        # print(gouliang2)

        # 如果都没满则退出
        if not gouliang1 and not gouliang2:
            return

        # 开始换狗粮
        while self.run:
            # 点击狗粮位置
            self.yys.mouse_click_bg(*TansuoPos.change_monster)
            if self.yys.wait_game_img('img\\QUAN-BU.png', 3, False):
                break
        time.sleep(1)

        # 点击“全部”选项
        self.yys.mouse_click_bg(*TansuoPos.quanbu_btn)
        time.sleep(1)

        # 点击卡片
        if self.change_shikigami == 1:
            self.yys.mouse_click_bg(*TansuoPos.n_tab_btn)
        elif self.change_shikigami == 0:
            self.yys.mouse_click_bg(*TansuoPos.s_tab_btn)
        elif self.change_shikigami == 2:
            self.yys.mouse_click_bg(*TansuoPos.r_tab_btn)
        time.sleep(1)

        # 拖放进度条
        if self.slide_shikigami:
            # 读取坐标范围
            star_x = TansuoPos.n_slide[0][0]
            end_x = TansuoPos.n_slide[1][0]
            length = end_x - star_x

            # 计算拖放范围
            pos_end_x = int(star_x + length/100*self.slide_shikigami_progress)
            pos_end_y = TansuoPos.n_slide[0][1]

            self.yys.mouse_drag_bg(
                TansuoPos.n_slide[0], (pos_end_x, pos_end_y))

        # 更换狗粮
        if gouliang1:
            self.yys.mouse_drag_bg((309, 520), (554, 315))
        if gouliang2:
            time.sleep(1)
            self.yys.mouse_drag_bg((191, 520), (187, 315))

    def find_exp_moster(self):
        '''
        寻找经验怪
            return: 成功返回经验怪的攻打图标位置；失败返回-1
        '''
        # 查找经验图标
        exp_pos = self.yys.find_color(
            ((2, 205), (1127, 545)), (140, 122, 44), 2)
        if exp_pos == -1:
            exp_pos = self.yys.find_img_knn(
                'img\\EXP.png', 1, (2, 205), (1127, 545))
            if exp_pos == (0, 0):
                return -1
            else:
                exp_pos = (exp_pos[0]+2, exp_pos[1]+205)

        # 查找经验怪攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\FIGHT.png', 1, (exp_pos[0]-150, exp_pos[1]-250), (exp_pos[0]+150, exp_pos[1]-50))
        if not find_pos:
            return -1

        # 返回经验怪攻打图标位置
        fight_pos = ((find_pos[0]+exp_pos[0]-150),
                     (find_pos[1]+exp_pos[1]-250))
        return fight_pos

    def find_boss(self):
        '''
        寻找BOSS
            :return: 成功返回BOSS的攻打图标位置；失败返回-1
        '''
        # 查找BOSS攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\BOSS.png', 1, (2, 205), (1127, 545))
        if not find_pos:
            return -1

        # 返回BOSS攻打图标位置
        fight_pos = ((find_pos[0]+2), (find_pos[1]+205))
        return fight_pos

    def fight_moster(self, mood1, mood2):
        '''
        打经验怪
            :return: 打完普通怪返回1；打完boss返回2；未找到经验怪返回-1；未找到经验怪和boss返回-2
        '''
        while self.run:
            mood1.moodsleep()
            # 查看是否进入探索界面
            self.yys.wait_game_img('img\\YING-BING.png')
            self.log.writeinfo('进入探索页面')

            # 寻找经验怪，未找到则寻找boss，再未找到则退出
            fight_pos = self.find_exp_moster()
            boss = False
            if fight_pos == -1:
                if self.fight_boss_enable:
                    fight_pos = self.find_boss()
                    boss = True
                    if fight_pos == -1:
                        self.log.writeinfo('未找到经验怪和boss')
                        return -2
                else:
                    self.log.writeinfo('未找到经验怪')
                    return -1

            # 攻击怪
            self.yys.mouse_click_bg(fight_pos)            
            self.log.writeinfo('已进入战斗')

            # 等待式神准备
            self.yys.wait_game_img_knn('img\\ZHUN-BEI.png', thread=30)
            logging.info('式神准备完成')

            # 检查狗粮经验
            self.check_exp_full()

            # 点击准备，直到进入战斗
            self.click_until('准备按钮', 'img\\ZI-DONG.png', *
                             TansuoPos.ready_btn, mood1.get1mood()/1000)

            # 检查是否打完
            state = self.check_end()
            mood1.moodsleep()

            # 在战斗结算页面
            self.get_reward(mood2, state)

            # 返回结果
            if boss:
                return 2
            else:
                return 1

    def start(self):
        '''单人探索主循环'''
        mood1 = ut.Mood(2)
        mood2 = ut.Mood(3)
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
            self.switch_to_scene(3)
            self.log.writeinfo('结束本轮探索')
            time.sleep(0.5)

            # 检查游戏次数
            self.check_times()
