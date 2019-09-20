class GamePos():
    def __init__(self,pos,pos_end=None):
        self.pos=pos
        self.pos_end=pos_end

class CommonPos():
    second_position = (877, 56), (1111, 452)  # 第二次结算所点击的位置

class TansuoPos():
    last_chapter = (934, 493), (1108, 572)  # 列表最后一章
    tansuo_btn=(787,458),(890,500) #探索按钮
    ready_btn = (1000, 460), (1069, 513)  # 准备按钮
    fight_quit=GamePos((1055,462),(1121,518)) #退出战斗
    quit_btn = (32, 45), (58, 64)  # 退出副本
    confirm_btn = (636, 350), (739, 370)  # 退出确认按钮
    change_monster = (427, 419), (457, 452)  # 切换狗粮点击区域
    quanbu_btn = (37, 574), (80, 604)  # “全部”按钮
    n_tab_btn = (142, 288), (164, 312)  # n卡标签
    quit_change_monster=GamePos((19,17),(43,38)) #退出换狗粮界面


class YuhunPos():
    tiaozhan_btn = (790, 418), (903, 469)    # 御魂挑战按钮
    kaishizhandou_btn = (857, 515), (998, 556)   # 御魂开始战斗按钮
