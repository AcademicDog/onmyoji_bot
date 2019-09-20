from gameLib.fighter import Fighter
from tools.game_pos import CommonPos, YuhunPos
import tools.utilities as ut


class SingleFight(Fighter):
    '''单人御魂战斗，参数done, emyc'''

    def __init__(self, done=1, emyc=0):
        # 初始化
        Fighter.__init__(self, '', emyc)

    def start(self):
        '''单人战斗主循环'''
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)
        while True:
            # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
            self.yys.wait_game_img('img\\TIAO-ZHAN.png',
                                   self.max_win_time)
            mood1.moodsleep()
            self.yys.mouse_click_bg(*YuhunPos.tiaozhan_btn)
            self.log.writeinfo('Already clicked TIAO-ZHAN')

            # 检测是否进入战斗
            self.check_battle()

            # 在战斗中，自动点怪
            self.click_monster()

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(ut.firstposition())
            self.click_until('结算', 'img\\TIAO-ZHAN.png',
                             *CommonPos.second_position, mood3.get1mood()/1000)
            self.log.writeinfo("Back to YUHUN level selection")
