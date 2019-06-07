import fighter
import utilities

# 参数
pos_button_start_battle = (987, 528)
col_button_yellow = 'f3b25e'

pos_jiesuan = (105, 345, 20, 85)
pos_button_continue_invite = (724, 396)

class DriverFighter(fighter.Fighter):
    '''御魂战斗司机程序，参数mode, emyc'''
    def __init__(self, mode, done, emyc = 0):
        # 初始化
        fighter.Fighter.__init__(self, emyc)

        # 识别模式
        if mode == 2:
            # 单刷模式
            
            # 绑定窗口
            hwnd = self.ts.FindWindow("", "阴阳师-网易游戏")
            self.fighter_binding(hwnd)

            # 启动看门狗
            self.watchdog(0, done, self.ts, self.hwnd)
        
    def single_start(self):
        '''单人御魂司机'''
        # 设定点击疲劳度
        mood1 = utilities.Mood()
        mood2 = utilities.Mood()
        mood3 = utilities.Mood()

        # 战斗主循环
        while True:
            # 喂狗
            self.dog.feed()

            # 司机点击开始战斗，需要锁定御魂阵容
            utilities.wtfc1(self.ts, *pos_button_start_battle, col_button_yellow, 868, 986, 523, 545, 0, 1, mood1.getmood())
            self.log.writeinfo('Driver: clicked KAI-SHI-ZHAN-DOU!')

            # 检测是否进入战斗
            self.check_battle()

            # 已经进入战斗，司机自动点怪
            while True:
                # 拒绝悬赏
                utilities.rejxs(self.ts)

                # 点怪
                self.click_monster()

                mood2.moodsleep()

                utilities.rejxs(self.ts)

                # 检测是否打完
                col = self.ts.GetColor(71, 577)
                if col != "f7f2df":
                    break
            self.log.writeinfo('Battle finished!')

            self.driver_end(mood3)

    def driver_end(self, mood):
        '''司机结算'''
        # 结算点击位置
        post_pos = utilities.Position()

        # 司机状态，0-默认；2-正常
        stats = 0
        while stats == 0:
            # 拒绝悬赏
            utilities.rejxs(self.ts)

            mood.moodsleep()
            utilities.crnd(self.ts, *post_pos.get_firstpos())
            mood.moodsleep()
            utilities.crnd(self.ts, *post_pos.get_secondpos())

            # 检查是否弹出继续邀请窗口
            coljs = self.ts.GetColor(*pos_button_continue_invite)
            if coljs == col_button_yellow:
                if self.ts.GetColor(499, 321) == '725f4d': 
                    # 这里意味着 勾选 继续邀请队友
                    utilities.wtfc1(self.ts, 499, 321, '725f4d', 499-5, 499+5, 321-5, 321+5, 0, 1, [500, 1000])
                    self.log.writeinfo('Clicked auto invite')
                else: 
                    # 如果没有这个选项，说明战斗失败，这里不需要打勾
                    self.log.writewarning('Failed')
                    global battle_failed_status
                    battle_failed_status = 1
                utilities.wtfc1(self.ts, *pos_button_continue_invite, col_button_yellow, 
                    pos_button_continue_invite[0]-5, pos_button_continue_invite[0]+5, 
                    pos_button_continue_invite[1]-5, pos_button_continue_invite[1]+5, 
                0, 1, [500, 1000])
                self.log.writeinfo('Cidked confirm to invite')
                #stats = 1
                #break 
        
            coljs = self.ts.GetColor(*pos_button_start_battle)
            if coljs == col_button_yellow: 
                self.log.writeinfo('Driver is in Team')
                stats = 2 
                break 
        self.log.writeinfo('Driver stats = %d', stats)