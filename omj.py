import sys
import os
import logging
import ctypes

from explore.single_explore import SingleExploreFight
from explore.explore import ExploreFight
from mitama.fighter_driver import DriverFighter
from mitama.fighter_passenger import FighterPassenger
from mitama.single_fight import SingleFight
from tools.logsystem import WriteLog

# 设置
global mode
global emyc
global done
global sign_shikigami

#初始化对象
log = WriteLog()

def init():
    global section
    global mode
    global emyc
    global done
    global sign_shikigami
    global multiPassenger
    global shikigami_type
    global shikigami_brush_max
    global shikigami_brush_max_quit
    global only_fight_exp

    multiPassenger = False

    try:
        # 选择打什么
        section = int(input('\n选择刷什么(Ctrl-C跳过并单刷御魂：\n0-御魂/业原火/御灵\n1-探索\n'))
        log.writeinfo('Section = %d', section)
        if section == 0:
            # 御魂模式选择
            mode=int(input('\n选择游戏模式(Ctrl-C跳过并单刷)：\n0-单刷\n2-组队司机\n3-组队打手\n22-组队司机（双乘客）\n'))
            if(mode==1):
                log.writewarning('未开发，告辞！')
                os._exit(0)
            elif(mode == 22):
                mode=2
                multiPassenger = True
            elif(mode != 2 and mode != 0 and mode != 3):
                mode=0

            # 标记式神设置
            sign_shikigami=int(input('\n是否标记式神？\n3-使用配置文件的设置\n0-不标记\n1-标记\n'))
            if((sign_shikigami!=3) and (sign_shikigami!=0) and (sign_shikigami!=1)):
                sign_shikigami=3
        else:
            # 探索模式选择
            # mode=int(input('\n选择游戏模式(Ctrl-C跳过并单刷)：\n0-单刷\n2-组队司机\n3-组队打手\n'))
            # if(mode==1):
            #     log.writewarning('未开发，告辞！')
            #     os._exit(0)
            # elif(mode != 2 and mode != 0 and mode != 3):
            #     mode=0
            mode=0

            log.writewarning('提示！！！！探索建议手动刷，探索相关的脚本 防检测机制 不够完善')
            log.writewarning('狗粮队长请放中间')
            shikigami_type=int(input('\n选择要自动换满级式神的类型：\n0-不替换满级式神（需锁定阵容）\n1-替换N卡（不能锁定阵容，需要关闭式神折叠）\n2-替换1级2星白蛋（不能锁定阵容，需要折叠相同式神）\n'))
            if shikigami_type!=1 and shikigami_type!=2 and shikigami_type!=3:
                shikigami_type = 0

            only_fight_exp=int(input('\是否只刷经验怪：\n1：是\n2：否\n'))
            if only_fight_exp == 1:
                only_fight_exp = True
            else:
                only_fight_exp = False

            shikigami_brush_max=int(input('\n填写要刷的局数：\n'))
            if not shikigami_brush_max:
                shikigami_brush_max = 999

            shikigami_brush_max_quit=int(input('\是否刷完关闭游戏：\n1：是\n2：否\n'))
            if shikigami_brush_max_quit == 1:
                shikigami_brush_max_quit = True
            else:
                shikigami_brush_max_quit = False

        # 点怪设置
        # emyc=int(input('\n是否点怪？\n0-不点怪\n1-点中间怪\n2-点右边怪\n'))
        # if((emyc!=0) and (emyc!=1) and (emyc!=2)):
        #     emyc=0

        # 结束设置
        # done=int(input('\n结束后如何处理？\n0-退出\n1-关机\n'))
        # if not ((done == 0) or (done == 1)):
        #     done = 0
            log.writeinfo('Mode = %d',mode)
        # log.writeinfo('Emyc = %d',emyc)
        # log.writeinfo('Postoperation = %d',done)
    except:
        section = 0
        mode=0
        emyc=0
        done=1
        sign_shikigami=3
        log.writeinfo('Use default parameters')

def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def yuhun():
    '''御魂战斗'''
    try:
        if mode == 0:
            # 单刷
            fight = SingleFight()

        if mode == 2:
            # 司机
            fight = DriverFighter()

        if mode == 3:
            # 乘客
            fight = FighterPassenger()

        if sign_shikigami != 3:
            fight.sign_shikigami = sign_shikigami
        fight.multiPassenger = multiPassenger
        fight.start()

    except Exception as e:
        log.writeinfo(e)
        os.system("pause")
    
def tansuo():
    '''探索战斗'''
    try:
        if mode == 0:
            # 单刷
            fight = SingleExploreFight()

        if mode == 2:
            # 司机
            fight = DriverExploreFight()

        if mode == 3:
            # 乘客
            fight = PassengerExploreFight()

        fight.shikigami_type = shikigami_type
        if shikigami_brush_max:
            fight.shikigami_brush_max = shikigami_brush_max
        fight.shikigami_brush_max_quit = shikigami_brush_max_quit
        fight.only_fight_exp = only_fight_exp
        fight.start()

    except Exception as e:
        log.writeinfo(e)
        os.system("pause")

def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' %(exc_type.__name__, exc_value)

    logging.error(msg)

if __name__ == "__main__":
    log.writeinfo('python version: %s', sys.version)
    
    try:
        # 检测管理员权限
        if is_admin():
            sys.excepthook = my_excepthook

            # 注册插件，获取权限
            log.writeinfo('UAC pass')            

            # 设置战斗参数
            init()

            # 开始战斗
            if section == 0:
                yuhun()
            elif section == 1:
                tansuo()

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)       
    except KeyboardInterrupt:
        log.writeinfo('terminated')
        os._exit(0)
    else:
        pass