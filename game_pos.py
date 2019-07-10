class GamePos():
    def __init__(self,pos,pos_end=None):
        self.pos=pos
        self.pos_end=pos_end

class TansuoPos():
    last_chapter=GamePos((934,493),(1108,572)) #列表最后一章
    tansuo_btn=GamePos((787,458),(890,500)) #探索按钮
    ready_btn=GamePos((1000,460),(1069,513)) #准备按钮
    fight_quit=GamePos((1055,462),(1121,518)) #退出战斗
    quit_btn=GamePos((32,45),(58,64)) #退出副本
    confirm_btn=GamePos((636,350),(739,370)) #退出确认按钮
    change_monster=GamePos((427,419),(457,452)) #切换狗粮点击区域
    quanbu_btn=GamePos((37,574),(80,604)) #“全部”按钮
    n_tab_btn=GamePos((142,288),(164,312)) #n卡标签
    quit_change_monster=GamePos((19,17),(43,38)) #退出换狗粮界面