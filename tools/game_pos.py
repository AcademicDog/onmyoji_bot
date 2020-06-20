class GamePos():
    def __init__(self,pos,pos_end=None):
        self.pos=pos
        self.pos_end=pos_end

class CommonPos():
    second_position = (960, 60), (1111, 452)  # 第二次结算所点击的位置
    shikigami_position_2 = (315, 390), (365, 506)  # 标记第二只式神的位置

class TansuoPos():
    last_chapter = (934, 493), (1108, 572)  # 列表最后一章
    tansuo_btn=(787,458),(890,500) #探索按钮
    tansuo_denglong = (424, 118), (462, 158)  # 探索灯笼
    ready_btn = (1000, 460), (1069, 513)  # 准备按钮
    fight_quit=GamePos((1055,462),(1121,518)) #退出战斗
    quit_btn = (32, 45), (58, 64)  # 退出副本
    confirm_btn = (636, 350), (739, 370)  # 退出确认按钮
    change_monster = (427, 419), (457, 452)  # 切换狗粮点击区域
    quanbu_btn = (37, 574), (80, 604)  # “全部”按钮
    n_tab_btn = (142, 288), (164, 312)  # n卡标签
    sucai_tab_btn = (44, 268), (88, 308)  # 素材卡标签
    n_slide = (168, 615), (784, 615)  # n卡进度条，从头至尾
    quit_change_monster=GamePos((19,17),(43,38)) #退出换狗粮界面

    gouliang_man_left = (190, 122), (370, 430)  # 左边狗粮满字位置
    gouliang_man_middle = (397, 122), (500, 430)  # 中间狗粮满字位置
    gouliang_man_right = (578, 122), (750, 430)  # 右边狗粮满字位置

    # 拖放相关位置
    gouliang_target_left = (990, 315)  # 左边狗粮拖放位置
    gouliang_target_middle = (554, 315)  # 中间狗粮拖放位置
    gouliang_target_right = (187, 315)  # 右边狗粮拖放位置

    # n卡拖放相关位置
    gouliang_left = (309, 520), gouliang_target_left  # 左边狗粮拖放路线
    gouliang_middle = (309, 520), gouliang_target_middle  # 中间狗粮拖放路线
    gouliang_right = (191, 520), gouliang_target_right  # 右边狗粮拖放路线

    gouliang_driver_left = (309, 520), (308, 306)  # 左边狗粮拖放路线(司机)
    gouliang_driver_right = (191, 520), (835, 306)  # 右边狗粮拖放路线(司机)

    gouliang_passenger_left = (309, 520), (554, 325)  # 左边狗粮拖放路线(乘客)
    gouliang_passenger_right = (191, 520), (187, 325)  # 右边狗粮拖放路线(乘客)

    # 素材卡拖放相关位置
    gouliang_sucai_0 = 204, 520  # 1级素材拖放起点
    gouliang_sucai_1 = 526, 520  # 1+级素材拖放起点1
    gouliang_sucai_2 = 648, 520  # 1+级素材拖放起点2


class YuhunPos():
    tiaozhan_btn = (960, 501), (1090, 631)    # 御魂挑战按钮
    kaishizhandou_btn = (1048, 535), (1113, 604)   # 御魂开始战斗按钮
