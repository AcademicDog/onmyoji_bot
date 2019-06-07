import fighter
import utilities

# 参数
col_normal_accept = '54b05f'
col_fighter_auto_accept = 'edc791'

pos_button_start_battle = (987, 528)
col_fighter_start_battle_blank = 'c7bdb4'

class FighterPassenger(fighter.Fighter):
    '''御魂战斗乘客程序，参数mode, emyc'''
    def __init__(self, mode, done, emyc = 0):
        # 初始化
        fighter.Fighter.__init__(self, emyc)

        # 战斗状态，1-失败；0-成功
        self.battle_status = 0

        # 识别模式
        if mode == 3:
            # 单刷模式
            
            # 绑定窗口
            hwnd = self.ts.FindWindow("", "阴阳师-网易游戏")
            self.fighter_binding(hwnd)

            # 启动看门狗
            self.watchdog(0, done, self.ts, self.hwnd)

    def single_start(self):
        '''单人御魂乘客'''
        # 设定点击疲劳度
        mood2 = utilities.Mood()
        mood3 = utilities.Mood()

        # 战斗主循环
        while True:
            # 喂狗
            self.dog.feed()

            # 检测是否进入战斗
            self.check_battle()

            # 已经进入战斗，乘客自动点怪
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

            self.passenger_end(mood3)

    def passenger_end(self, mood):
        '''乘客结算'''
        # 拒绝悬赏
        utilities.rejxs(self.ts)

        # 结算点击位置
        post_pos = utilities.Position()

        mood.moodsleep()
        utilities.crnd(self.ts, *post_pos.get_firstpos())
        mood.moodsleep()
        utilities.crnd(self.ts, *post_pos.get_secondpos())
        
        # 乘客状态，0-默认
        stats = 0
        while stats < 8:            
            mood.moodsleep()

            # 检测是否在等待队伍中
            coljs = self.ts.GetColor(*pos_button_start_battle)
            if coljs == col_fighter_start_battle_blank:
                self.log.writeinfo('Fighter in team!')
                self.battle_status = 0
                break
           
            # 检测是否已经开始
            col = self.ts.GetColor(71, 577)
            if col == "f7f2df":
                self.log.writeinfo('Fighter in battle!')
                break
            
            # 找色，打手的自动接受齿轮
            if self.battle_status == 0: 
                col_to_be_found = col_fighter_auto_accept
            else: 
                col_to_be_found = col_normal_accept
            intx, inty = None, None
            ffc_ret = self.ts.FindColor(16, 122, 350, 465, col_to_be_found, 1.0, 0, intx, inty)

            if ffc_ret[0] == 0:
                # 找到颜色
                self.log.writeinfo('Fighter (auto) accept found at %s', ffc_ret)
                utilities.wtfc1(self.ts, ffc_ret[1], ffc_ret[2], col_to_be_found, 
                    ffc_ret[1]-5, ffc_ret[1]+5, ffc_ret[2]-5, ffc_ret[2]+5, 
                0, 1, (300,500))
                self.log.writeinfo('Fighter clicked (auto) accept')
                break
            
            utilities.crnd(self.ts, *post_pos.get_pos())
            stats = stats + 1

        self.log.writeinfo('Fighter stats = %d', stats)