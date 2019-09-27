from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, TansuoPos
import tools.utilities as ut

import configparser
import random
import time


class ExploreFight(Fighter):
    def __init__(self):
        # 初始化
        Fighter.__init__(self)

        # 读取配置文件
        conf = configparser.ConfigParser()
        conf.read('conf.ini')
        self.fight_boss_enable = conf.getboolean('explore', 'fight_boss_enable')
        self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        self.slide_shikigami_progress = conf.getint('explore', 'slide_shikigami_progress')

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

        # 点击“N”卡
        self.yys.mouse_click_bg(*TansuoPos.n_tab_btn)
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
            return -1

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
            :return: 打完返回True；未找到经验怪返回False
        '''
        while self.run:
            mood1.moodsleep()
            # 查看是否进入探索界面
            self.yys.wait_game_img('img\\YING-BING.png')
            self.log.writeinfo('进入探索页面')

            # 寻找经验怪，未找到则寻找boss，再未找到则退出
            fight_pos = self.find_exp_moster()
            if fight_pos == -1:
                if self.fight_boss_enable:
                    fight_pos = self.find_boss()
                    if fight_pos == -1:
                        self.log.writeinfo('未找到经验怪和boss')
                        return False
                else:
                    self.log.writeinfo('未找到经验怪')
                    return False

            # 攻击怪
            self.yys.mouse_click_bg(fight_pos)
            if not self.yys.wait_game_img('img\\ZHUN-BEI.png', 3, False):
                break
            self.log.writeinfo('已进入战斗')
            time.sleep(1)

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
            self.click_until('结算', 'img\\MESSAGE.png',
                             *CommonPos.second_position, mood2.get1mood()/1000)

    def start(self):
        '''单人探索主循环'''
        mood1 = ut.Mood(2)
        mood2 = ut.Mood(3)
        while self.run:
            # 点击挑战按钮
            if self.yys.find_game_img('img\\TAN-SUO.png'):
                self.click_until('探索按钮', 'img\\YING-BING.png',
                                 *TansuoPos.tansuo_btn, mood1.get1mood()/1000)
            else:
                self.click_until('最后章节', 'img\\TAN-SUO.png',
                                 *TansuoPos.last_chapter, mood1.get1mood()/1000)
                self.click_until('探索按钮', 'img\\YING-BING.png',
                                 *TansuoPos.tansuo_btn, mood1.get1mood()/1000)

            # 开始打怪
            i = 0
            while i < 4 and self.run:
                result = self.fight_moster(mood1, mood2)
                if result:
                    continue
                else:
                    self.log.writeinfo('移动至下一个场景')
                    self.next_scene()
                    i += 1

            # 退出探索
            if self.yys.find_game_img('img\\YING-BING.png'):
                while self.run:
                    self.yys.mouse_click_bg(*TansuoPos.quit_btn)
                    if self.yys.wait_game_img('img\\QUE-REN.png', 3, False):
                        break
                self.yys.mouse_click_bg(*TansuoPos.confirm_btn)
            self.log.writeinfo('结束本轮探索')
            time.sleep(0.5)
