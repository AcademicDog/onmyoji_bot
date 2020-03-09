from tools.game_pos import TansuoPos, YuhunPos

import time


class GameScene():
    def __init__(self):
        self.deep = 0

    def get_scene(self):
        '''
        识别当前场景
            :return: 返回场景名称:
            1-庭院; 
            2-探索界面; 
            3-章节界面; 
            4-探索内; 
            5-御魂菜单; 
            6-御魂开始
            7-业原火开始
            8-卑弥呼开始
        '''
        # 拒绝悬赏
        self.yys.rejectbounty()

        # 分别识别庭院、探索、章节页、探索内
        maxVal, maxLoc = self.yys.find_multi_img(
            'img/JIA-CHENG.png', 'img/JUE-XING.png', 'img/TAN-SUO.png', 'img/YING-BING.png', 'img/BA-QI-DA-SHE.png', 'img/TIAO-ZHAN.png')

        scene_cof = max(maxVal)
        if scene_cof > 0.9:
            scene = maxVal.index(scene_cof)
            return scene + 1
        else:
            return 0

    def switch_to_scene(self, scene):
        '''
        切换场景
            :param scene: 需要切换到的场景:1-8
            :return: 切换成功返回True；切换失败直接退出
        '''
        scene_now = self.get_scene()
        self.log.info('目前场景：' + str(scene_now))

        if scene_now == 0:
            self.log.info('暂未识别场景，2s后重试一次')
            time.sleep(2)
            scene_now = self.get_scene()
            self.log.info('目前场景：' + str(scene_now))

        if scene_now == scene:
            return True
        if scene_now == 1:
            # 庭院中
            if scene in [2, 3, 4, 5, 6, 7, 8]:
                # 先将界面划到最右边
                self.slide_x_scene(800)
                time.sleep(2)
                self.slide_x_scene(800)

                # 点击探索灯笼进入探索界面
                self.click_until('探索灯笼', 'img/JUE-XING.png', *
                                 TansuoPos.tansuo_denglong, 2)

                # 递归
                self.switch_to_scene(scene)

        elif scene_now == 2:
            # 探索界面
            if scene == 3 or scene == 4:
                # 点击最后章节
                self.click_until('最后章节', 'img/TAN-SUO.png',
                                 *TansuoPos.last_chapter, 2)
                # 递归
                self.switch_to_scene(scene)
            elif scene in [5, 6, 7, 8]:
                # 点击御魂按钮
                self.click_until('御魂菜单', 'img/BA-QI-DA-SHE.png',
                                 *YuhunPos.yuhun_menu, 2)
                # 递归
                self.switch_to_scene(scene)

        elif scene_now == 3:
            # 章节界面
            if scene == 4:
                # 点击探索按钮
                self.click_until('探索按钮', 'img/YING-BING.png',
                                 *TansuoPos.tansuo_btn, 2)
                # 递归
                self.switch_to_scene(scene)
            elif scene in [5, 6, 7, 8]:
                self.click_until('退出章节', 'img/JUE-XING.png',
                                 *TansuoPos.quit_last_chapter, 2)
                self.switch_to_scene(scene)

        elif scene_now == 4:
            # 探索内
            if scene in [2, 3]:
                # 点击退出探索
                self.click_until_multi('退出按钮', 'img/QUE-REN.png', 'img/TAN-SUO.png', 'img/JUE-XING.png',
                                 pos=TansuoPos.quit_btn[0], pos_end=TansuoPos.quit_btn[1], step_time=0.5)

                # 点击确认
                self.click_until('确认按钮', 'img\\QUE-REN.png',
                                 *TansuoPos.confirm_btn, 2, False)
                # 递归
                self.switch_to_scene(scene)

        elif scene_now == 5:
            # 御魂菜单内
            if scene == 6:
                # 点击御魂
                self.click_until_knn('御魂选项', 'img/TIAO-ZHAN.png',
                                     *YuhunPos.yuhun_btn, 2, thread=20)
                # 递归
                self.switch_to_scene(scene)
            elif scene == 7:
                # 点击业原火
                self.click_until_knn('业原火选项', 'img/TIAO-ZHAN.png',
                                     *YuhunPos.yeyuanhuo_btn, 2, thread=20)
                # 递归
                self.switch_to_scene(scene)
            elif scene == 8:
                # 点击卑弥呼
                self.click_until_knn('卑弥呼选项', 'img/TIAO-ZHAN.png',
                                     *YuhunPos.beimihu_btn, 2, thread=20)
                # 递归
                self.switch_to_scene(scene)
