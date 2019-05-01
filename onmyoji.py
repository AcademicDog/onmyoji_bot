import win32com.client 
import sys 
import os
import ctypes
import threading
import logsystem
import watchdog
import fighter
import utilities

# 参数
col_button_yellow = 'f3b25e'
col_fighter_start_battle_blank = 'c7bdb4'
pos_button_start_battle = (987, 528)
col_zidong = 'f7f2df'
pos_zidong = (71, 577)
pos_button_continue_invite = (724, 396)
col_fighter_auto_accept = 'edc791'
pos_jiesuan = (105, 345, 20, 85)
col_normal_accept = '54b05f'
pos_middle_monster = (509, 579, 153, 181)
pos_right_monster = (773, 856, 159, 190)

battle_failed_status = 0 

# 设置
global mode
global emyc
global hwnd
global done
hwnd = 0
HWND=[0,0]

#初始化对象
dog = watchdog.Watchdog()
log = logsystem.WriteLog()

def quit():
    #退出并清理窗口
    if(done==2):
        log.writewarning('Attention, shutdown in 60 s')
        os.system("shutdown -s -t  60 ")
    elif(done==1):
        if(mode==0):
            log.writewarning('Attention, one window will be colsed')
            ts.SetWindowState(hwnd,13)
        elif(mode==1):
            log.writewarning('Attention, two windows will be colsed')
            ts_d.SetWindowState(HWND[0],13)
            ts_f.SetWindowState(HWND[1],13)
        os._exit()
    elif(done==0):
        os._exit()

def init():
    global mode
    global emyc
    global done
    
    try:
        # 模式选择
        mode=int(input('\n选择游戏模式(Ctrl-C跳过并单刷)：\n0-单刷\n1-本地双开\n2-组队司机\n3-组队打手\n'))
        if(mode==2) or (mode==3):
            log.writewarning('未开发，告辞！')
            exit()
        elif((mode!=1) and (mode!=0)):
            mode=0
        
        # 点怪设置
        emyc=int(input('\n是否点怪？\n0-不点怪\n1-点中间怪\n2-点右边怪\n'))
        if((emyc!=0) and (emyc!=1) and (emyc!=2)):
            emyc=0
        
        # 结束设置
        done=int(input('\n结束后如何处理？\n0-不做操作\n1-退出\n2-关机\n'))
        if(not((done==0) or (done==1) or (done==2))):
            done=1
        log.writeinfo('Mode = %d',mode)
        log.writeinfo('Emyc = %d',emyc)
        log.writeinfo('Postoperation = %d',done)
    except:
        mode=0
        emyc=0
        done=1
        log.writeinfo('Use default parameters')

def dog_response():
    if(dog.bark() == 1):
        log.writewarning("Dog barked!")
        quit()

def is_admin():
    #UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# 单人模式
def yuhun(ts): 
    global emyc

    # 检测天使插件 COM Object 是否建立成功
    single_fighter = fighter.Fighter(ts)
    if(not single_fighter.ready):
        log.writewarning('Register failed')
        return 
    log.writeinfo('Register successful')

    # 绑定窗口
    if(not single_fighter.fighter_binding()):    
        log.writewarning('Binding failed')
        return 
    log.writeinfo('Binding successful')

    # 颜色 Debug 测试 
    single_fighter.fighter_test()
    log.writeinfo('Passed color debug')

    # 御魂战斗主循环
    while True:
        dog.feed()
        # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
        utilities.wtfc1(ts, 807, 442, "f3b25e", 807, 881, 442, 459, 0, 1)
        log.writeinfo('Already clicked TIAO-ZHAN')

        #wtfc1(ts, 1033, 576, "e6c78f", 1004, 1073, 465, 521, 0, 1)
        #print('already clicked ZHUN-BEI')

        # 检测是否进入战斗
        while True:
            utilities.rejxs(ts)
            dog_response()
            colib = ts.GetColor(71, 577)
            if colib == "f7f2df":
                break
            utilities.mysleep(500)
        log.writeinfo("Now we are in the battle")

        # 在战斗中，自动点怪
        while True:
          utilities.rejxs(ts)
          dog_response()

          # 点击中间怪物
          if emyc == 1:
            utilities.crnd(ts, 509, 579, 153, 181)

          # 点击右边怪物
          elif emyc == 2:
            utilities.crnd(ts, 773, 856, 159, 190)

          utilities.mysleep(500, 500)

          utilities.rejxs(ts)
          colib = ts.GetColor(71, 577)
          if colib != "f7f2df":
              break
        log.writeinfo("Battle finished")

        # 在战斗结算页面
        while True: 
          dog_response()
          utilities.rejxs(ts)
          utilities.crnd(ts, 980, 1030, 225, 275)

          coljs = ts.GetColor(807, 442)
          if coljs == "f3b25e":
              break
          utilities.mysleep(500, 500)
        log.writeinfo("back to YUHUN level selection")

def bind_two_windows(ts_d, ts_f): 
    hwnd_raw = ts_d.EnumWindowByProcess("onmyoji.exe", "", "", 16)
    HWND = hwnd_raw.split(',')
    log.writeinfo('windows handle:', HWND)

    if len(HWND)!=2: 
        log.writewarning('Need 2 windows!')
        return 10 

    # 绑定窗口
    ts_ret = ts_d.BindWindow(HWND[0], 'dx2', 'windows', 'windows', 0) 
    if(ts_ret != 1): 
        log.writewarning('first window binding failed')
        return 1
    ts_ret = ts_f.BindWindow(HWND[1], 'dx2', 'windows', 'windows', 0) 
    if(ts_ret != 1): 
        log.writewarning('second window binding failed')
        return 2
    utilities.mysleep(500)

    if ts_f.GetColor(*pos_button_start_battle) == col_button_yellow: 
        #ts_d, ts_f = ts_f, ts_d
        log.writeinfo("handle swapped, don't worry")
        HWND[1], HWND[0]=HWND[0], HWND[1]
        ts_ret = ts_d.BindWindow(HWND[0], 'dx2', 'windows', 'windows', 0) 
        ts_ret = ts_f.BindWindow(HWND[1], 'dx2', 'windows', 'windows', 0) 
    elif ts_d.GetColor(*pos_button_start_battle) == col_button_yellow: 
        pass 
    else: 
        log.writewarning("didn't find KAI-SHI-ZHAN-DOU, can't distinguish which one is driver ")
        return 20

    log.writeinfo('binding successful')
    return 0

def unbind_two_windows(ts_d, ts_f): 
    return (
        ts_d.UnBindWindow(), 
        ts_f.UnBindWindow() 
    )

def fighter_jiesuan(ts, hwnd): 
    global battle_failed_status
    stats = 0 
    while stats == 0: 
        utilities.rejxs(ts)
        dog_response()
        utilities.crnd(ts, *pos_jiesuan)

        utilities.mysleep(500, 500)

        #print('battle_failed_status =', battle_failed_status)
        if battle_failed_status == 0: 
            col_to_be_found = col_fighter_auto_accept
        else: 
            col_to_be_found = col_normal_accept

        # 找色，打手的自动接受齿轮 或 普通接受对勾
        intx, inty = None, None
        ffc_ret = ts.FindColor(16, 122, 366, 465, col_to_be_found, 1.0, 0, intx, inty)
        #print(type(ffc_ret), ffc_ret)

        if ffc_ret[0] == 0: 
            log.writeinfo('fighter (auto) accept found at', ffc_ret)
            utilities.wtfc1(ts, ffc_ret[1], ffc_ret[2], col_to_be_found, 
                ffc_ret[1]-5, ffc_ret[1]+5, ffc_ret[2]-5, ffc_ret[2]+5, 
                0, 1)
            log.writeinfo('fighter clicked (auto) accept')

        coljs = ts.GetColor(*pos_button_start_battle)
        if coljs == col_fighter_start_battle_blank: 
            log.writeinfo('fighter in XIE ZHAN DUI WU!')
            battle_failed_status = 0 
            stats = 1 
            break 
    log.writeinfo('fighter stats =', stats)

def driver_jiesuan(ts, hwnd): 
    stats = 0
    while stats == 0: 
        utilities.rejxs(ts)
        dog_response()
        utilities.crnd(ts, *pos_jiesuan)
        utilities.mysleep(500, 500)
        coljs = ts.GetColor(*pos_button_continue_invite)
        if coljs == col_button_yellow:
            if ts.GetColor(499, 321) == '725f4d': 
                # 这里意味着 勾选 继续邀请队友
                utilities.wtfc1(ts, 499, 321, '725f4d', 499-5, 499+5, 321-5, 321+5, 0, 1)
                log.writeinfo('ticked MO REN YAO QING DUI YOU')
            else: 
                # 如果没有这个选项，说明战斗失败，这里不需要打勾
                log.writewarning('failed')
                global battle_failed_status 
                battle_failed_status = 1 
            utilities.wtfc1(ts, *pos_button_continue_invite, col_button_yellow, 
                pos_button_continue_invite[0]-5, pos_button_continue_invite[0]+5, 
                pos_button_continue_invite[1]-5, pos_button_continue_invite[1]+5, 
                0, 1)
            log.writeinfo('clidked QUE REN, JI XU YAO QING DUI YOU')
            #stats = 1
            #break 
        
        coljs = ts.GetColor(*pos_button_start_battle)
        if coljs == col_button_yellow: 
            log.writeinfo('driver is in XIE ZHAN DUI WU')
            stats = 2 
            break 
    log.writeinfo('driver stats =', stats)

# 双人模式
def dual_yuhun(ts_d, ts_f): 
    global emyc

    # 检测 COM Object 是否建立成功
    need_ver = '4.019'
    if ts_d.ver() != need_ver or ts_f.ver() != need_ver: 
        log.writewarning('register failed')
        return 
    log.writeinfo('register successful')

    # 绑定两个游戏窗口, ts_d = driver = 司机, ts_f = fighter = 打手
    btw_ret = bind_two_windows(ts_d, ts_f)
    if btw_ret != 0: 
        return 

    # 御魂战斗主循环
    while True: 
        # 司机点击开始战斗
        # 需要锁定阵容！
        dog.feed()
        utilities.wtfc1(ts_d, *pos_button_start_battle, col_button_yellow, 
            868, 986, 523, 545, 0, 1)
        log.writeinfo('clicked KAI-SHI-ZHAN-DOU!')

        #判断是否已经进入战斗 
        while True: 
            col_d = ts_d.GetColor(pos_zidong[0], pos_zidong[1])
            col_f = ts_f.GetColor(pos_zidong[0], pos_zidong[1])
            if col_d == col_zidong or col_f == col_zidong: 
                break
            utilities.mysleep(50)
            dog_response()
        log.writeinfo('in the battle!')

        # 已经进入战斗，司机自动点怪
        while True:
            utilities.rejxs(ts_d)
            utilities.rejxs(ts_f)
            dog_response()

            # 点击中间怪物
            if emyc == 1:
                utilities.crnd(ts_d, *pos_middle_monster)

            # 点击右边怪物
            elif emyc == 2:
                utilities.crnd(ts_d, *pos_right_monster)

            utilities.mysleep(500, 500)

            utilities.rejxs(ts_d)
            utilities.rejxs(ts_f)
            col_d = ts_d.GetColor(pos_zidong[0], pos_zidong[1])
            col_f = ts_f.GetColor(pos_zidong[0], pos_zidong[1])
            if col_d != col_zidong and col_f != col_zidong: 
                break
        log.writeinfo('battle finished!')

        thr_f_j = threading.Thread(target=fighter_jiesuan, args=(ts_f,HWND[1],))
        thr_d_j = threading.Thread(target=driver_jiesuan, args=(ts_d,HWND[0],))

        thr_f_j.start() 
        thr_d_j.start() 

        thr_f_j.join()
        thr_d_j.join()

        log.writeinfo('joined, new cycle!')
    

if __name__ == "__main__":    
    log.writeinfo('python version: %s', sys.version)

    # 需要提前在 windows 中注册 TSPlug.dll
    # 方法: regsvr32.exe TSPlug.dll

    # Reference: http://timgolden.me.uk/pywin32-docs/html/com/win32com/HTML/QuickStartClientCom.html
    # 建立 COM Object
    
    try:
        if is_admin():
        # 注册插件，获取权限
            log.writeinfo('UAC pass')
            os.system('regsvr32.exe C://TSPlug.dll')
            init()
            if(mode==0):
                ts = win32com.client.Dispatch("ts.tssoft")
                yuhun(ts)
            if(mode==1):
                ts_d = win32com.client.Dispatch("ts.tssoft") 
                ts_f = win32com.client.Dispatch("ts.tssoft") 
                dual_yuhun(ts_d, ts_f)
        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)       
    except KeyboardInterrupt:        
        log.writeinfo('terminated')
        if(mode==0):
            log.writeinfo('UnBindWindow return:', ts.UnBindWindow())
        elif(mode==1):
            log.writeinfo("unbind results:", unbind_two_windows(ts_d, ts_f))
        os.system('regsvr32.exe /u C://TSPlug.dll')
    else:
        quit()