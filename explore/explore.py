from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, TansuoPos
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
        self.fight_boss_enable = conf.getboolean('explore', 'fight_boss_enable')
        self.slide_shikigami = conf.getboolean('explore', 'slide_shikigami')
        self.slide_shikigami_progress = conf.getint('explore', 'slide_shikigami_progress')
        self.shikigami_type = conf.getboolean('explore', 'shikigami_type')
        self.zhunbei_delay = conf.getfloat('explore', 'zhunbei_delay')

        self.fight_count = 0

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
        # 狗粮经验判断, gouliang1是左边狗粮，gouliang2是右边狗粮
        gouliang1 = self.yys.find_game_img(
            'img\\MAN0.png', 1, *TansuoPos.gouliang_man_left, 1)
        gouliang2 = self.yys.find_game_img(
            'img\\MAN2.png', 1, *TansuoPos.gouliang_man_right, 1)

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

        # 点击“N”卡或“素材”
        if self.shikigami_type == 1:
            self.yys.mouse_click_bg(*TansuoPos.n_tab_btn)
        else:
            self.yys.mouse_click_bg(*TansuoPos.sucai_tab_btn)
        time.sleep(1)

        self.change_shikigami(gouliang1,gouliang2)

    def change_shikigami(self,gouliang1,gouliang2):
        '''
        变更式神
        '''
        if self.shikigami_type == 0:
            return

        # 换n卡
        elif self.shikigami_type == 1:
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
                if self.mode == 0:
                    pos = TansuoPos.gouliang_left
                if self.mode == 2:
                    pos = TansuoPos.gouliang_driver_left
                if self.mode == 3:
                    pos = TansuoPos.gouliang_passenger_left
                self.yys.mouse_drag_bg(*pos)
            if gouliang2:
                time.sleep(1)
                if self.mode == 0:
                    pos = TansuoPos.gouliang_right
                if self.mode == 2:
                    pos = TansuoPos.gouliang_driver_right
                if self.mode == 3:
                    pos = TansuoPos.gouliang_passenger_right
                self.yys.mouse_drag_bg(*pos)

        # 换2星1级白蛋
        elif self.shikigami_type == 2:
            if gouliang1:
                if self.mode == 0:
                    pos2 = TansuoPos.gouliang_target_left
                if self.mode == 2:
                    pos2 = TansuoPos.gouliang_target_left
                if self.mode == 3:
                    pos2 = TansuoPos.gouliang_target_left
                self.yys.mouse_drag_bg(TansuoPos.gouliang_sucai_0,pos2)
            if gouliang2:
                time.sleep(1)
                if gouliang1:
                    self.yys.mouse_drag_bg(TansuoPos.gouliang_sucai_0,(TansuoPos.gouliang_sucai_0[0]+3,TansuoPos.gouliang_sucai_0[1]+3))
                    time.sleep(0.7)
                if self.mode == 0:
                    pos2 = TansuoPos.gouliang_target_right
                if self.mode == 2:
                    pos2 = TansuoPos.gouliang_target_right
                if self.mode == 3:
                    pos2 = TansuoPos.gouliang_target_right
                self.yys.mouse_drag_bg(TansuoPos.gouliang_sucai_0,pos2)

        # 换高级白蛋
        elif self.shikigami_type == 3:
            if gouliang1:
                if gouliang2:
                    pos1 = TansuoPos.gouliang_sucai_1
                else:
                    pos1 = TansuoPos.gouliang_sucai_2
                if self.mode == 0:
                    pos2 = TansuoPos.gouliang_target_left
                if self.mode == 2:
                    pos2 = TansuoPos.gouliang_target_left
                if self.mode == 3:
                    pos2 = TansuoPos.gouliang_target_left
                self.yys.mouse_drag_bg(pos1,pos2)
            if gouliang2:
                time.sleep(1)
                if gouliang1:
                    pos1 = TansuoPos.gouliang_sucai_2
                    self.yys.mouse_drag_bg(TansuoPos.gouliang_sucai_0,(pos1[0]+3,pos1[1]+3))
                    time.sleep(0.7)
                else:
                    pos1 = TansuoPos.gouliang_sucai_1
                if self.mode == 0:
                    pos2 = TansuoPos.gouliang_target_right
                if self.mode == 2:
                    pos2 = TansuoPos.gouliang_target_right
                if self.mode == 3:
                    pos2 = TansuoPos.gouliang_target_right
                self.yys.mouse_drag_bg(pos1,pos2)

    def find_exp_moster(self):
        '''
        寻找经验怪
            return: 成功返回经验怪的攻打图标位置；失败返回-1
        '''
        # 查找经验图标
        exp_pos = self.yys.find_color(
            ((2, 115), (1127, 545)), (140, 122, 44), 4)
        if exp_pos == -1:
            exp_pos = self.yys.find_color(
                        ((2, 115), (1127, 545)), (52, 23, 10), 4)
        if exp_pos == -1:
            exp_pos = self.yys.find_color(
                        ((2, 115), (1127, 545)), (44, 18, 9), 4)
        if exp_pos == -1:
            exp_pos = self.yys.find_color(
                        ((2, 115), (1127, 545)), (140, 76, 40), 4)
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

    def find_moster(self):
        '''
        寻找普通怪
            :return: 成功返回攻打图标位置；失败返回-1
        '''
        # 查找攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\FIGHT.png', 1, (2, 115), (1127, 545))
        if not find_pos:
            return -1

        # 返回攻打图标位置
        fight_pos = ((find_pos[0]+2), (find_pos[1]++115))
        return fight_pos

    def find_boss(self):
        '''
        寻找BOSS
            :return: 成功返回BOSS的攻打图标位置；失败返回-1
        '''
        # 查找BOSS攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\BOSS.png', 1, (2, 115), (1127, 545))
        if not find_pos:
            return -1

        # 返回BOSS攻打图标位置
        fight_pos = ((find_pos[0]+2), (find_pos[1]+115))
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

            # 寻找普通或经验怪，未找到则寻找boss，再未找到则退出
            if self.only_fight_exp:
                fight_pos = self.find_exp_moster()
            else:
                fight_pos = self.find_moster()
            boss = False
            if fight_pos == -1:
                if self.fight_boss_enable:
                    fight_pos = self.find_boss()
                    boss = True
                    if fight_pos == -1:
                        self.log.writeinfo('未找到你想刷的怪和boss')
                        return -2
                else:
                    self.log.writeinfo('未找到你想刷的怪')
                    return -1

            # 攻击怪
            self.log.writeinfo('click')
            self.yys.mouse_click_bg(fight_pos)
            self.log.writeinfo(fight_pos)
            if self.shikigami_type != 0:
                if not self.yys.wait_game_img('img\\ZHUN-BEI.png', self.zhunbei_delay, False):
                    break
            else:
                if not self.yys.wait_game_img('img\\ZI-DONG.png', self.zhunbei_delay, False):
                    break
            self.log.writeinfo('已进入战斗')
            time.sleep(1)

            # 等待式神准备
            # self.yys.wait_game_color(((1024,524),(1044, 544)), (138,198,233), 30)
            logging.info('式神准备完成')

            # 检查狗粮经验
            if self.shikigami_type != 0:
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

            self.fight_count = self.fight_count + 1
            if self.fight_count>=self.shikigami_brush_max:
                if self.shikigami_brush_max_quit:
                    self.yys.activate_window()
                    time.sleep(5)
                    self.yys.quit_game()
                else:
                    self.deactivate()

            # 返回结果
            if boss:
                return 2
            else:
                return 1

    def click_box(self):
        '''
        点击宝箱
        '''
        time.sleep(1)
        start_time = time.time()
        while True:
            scene_now = self.get_scene()
            if scene_now != 4 or ( time.time() - start_time > 10000):
                break
            pos = self.yys.find_game_img('img\\BAO-WU.png')
            if pos:
                self.log.writeinfo('点击打开宝物')
                self.yys.mouse_click_bg(pos)
                time.sleep(0.5)
                self.yys.mouse_click_bg(*CommonPos.second_position)
            time.sleep(0.5)