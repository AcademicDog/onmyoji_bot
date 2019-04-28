import win32com.client 
import sys 
import time
import random
import os
import ctypes
import threading
import logsystem
import watchdog

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
HWND=[0,0]
dog = watchdog.Watchdog()

def quit():
    #退出并清理窗口
    if(done==2):
        logsystem.logging.warning('Attention, shutdown in 60 s')
        os.system("shutdown -s -t  60 ")
    elif(done==1):
        if(mode==0):
            logsystem.logging.warning('Attention, one window will be colsed')
            ts.SetWindowState(hwnd,13)
        elif(mode==1):
            logsystem.logging.warning('Attention, two windows will be colsed')
            ts_d.SetWindowState(HWND[0],13)
            ts_f.SetWindowState(HWND[1],13)
        exit()
    elif(done==0):
        exit()

def init():
    global mode
    global emyc
    global hwnd
    global done
    
    try:
        # 模式选择
        mode=int(input('\n选择游戏模式(Ctrl-C跳过并单刷)：\n0-单刷\n1-本地双开\n2-组队司机\n3-组队打手\n'))
        if(mode==2) or (mode==3):
            logsystem.logging.warning('未开发，告辞！')
            exit()
        elif((mode!=1) and (mode!=0)):
            mode=0
        logsystem.logging.info('Mode = %d',mode)

        # 点怪设置
        emyc=int(input('\n是否点怪？\n0-不点怪\n1-点中间怪\n2-点右边怪\n'))
        if((emyc!=0) and (emyc!=1) and (emyc!=2)):
            emyc=0
        logsystem.logging.info('Emyc = %d',emyc)

        # 结束设置
        done=int(input('\n结束后如何处理？\n0-不做操作\n1-退出\n2-关机\n'))
        if(not((done==0) or (done==1) or (done==2))):
            done=1
        logsystem.logging.info('Postoperation = %d',done)
    except:
        mode=0
        emyc=0
        done=1
        logsystem.logging.info('Use default parameters')

def dog_response():
    if(dog.bark() == 1):
        logsystem.logging.warning("Dog barked!")
        quit()

def is_admin():
    #UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def mysleep(slpa, slpb = 0): 
    '''
    randomly sleep for a short time between `slpa` and `slpa + slpb` \n
    because of the legacy reason, slpa and slpb are in millisecond
    '''
    slp = random.randint(slpa, slpa+slpb) 
    time.sleep(slp/1000)

def crnd(ts, x1, x2, y1, y2): 
    '''
    randomly click a point in a rectangle region (x1, y1), (x2, y2)
    '''
    xr = random.randint(x1, x2)
    yr = random.randint(y1, y2)
    ts.MoveTo(xr, yr)
    mysleep(10, 10)
    ts.LeftClick() 
    mysleep(10, 10)

def rejxs(ts): 
    colxs = ts.GetColor(750, 458)
    #print(colxs)
    if colxs == "df715e":
        crnd(ts, 750-5, 750+5, 458-5, 458+5)
        logsystem.logging.info("Successfully rejected bounty")
        mysleep(1000)
    mysleep(50)

def wtfc1(ts, colx, coly, coll, x1, x2, y1, y2, zzz, adv, hwnd):
  '''
  Usage: 
  等待并且持续判断点 (colx, coly) 的颜色，直到该点颜色
  等于 coll (if zzz == 0) 或者 不等于 coll (if zzz == 1) 
  然后开始随机点击范围 (x1, x2) (y1, y2) 内的点，直到点 (colx, coly) 的颜色
    if adv == 1: 
     不等于 coll (if zzz == 0) 或者 等于 coll (if zzz == 1)  
    if adv == 0: 
     不判断，点击一次后退出循环
  Example: 
  在准备界面时，通过判断鼓锤上某点的颜色（因为UI不会随着游戏人物摆动），来持续点击鼓面，
  直到鼓锤上该点的颜色改变，说明进入了战斗
  '''
  j = 0
  flgj =0
  while j == 0:
    rejxs(ts)
    dog_response()
    coltest = ts.GetColor(colx, coly)
    #print(colx, coly, coltest)
    if (coltest == coll and zzz == 0) or (coltest != coll and zzz == 1):
        flgj = 1
    if flgj == 1:
        rejxs(ts)
        crnd(ts, x1, x2, y1, y2)
        mysleep(1000, 333)
        if adv == 0:
            j = 1
        rejxs(ts)
        coltest2 = ts.GetColor(colx, coly)
        if (coltest2 == coll and zzz == 1) or (coltest2 != coll and zzz == 0):
            j = 1

# 单人模式
def yuhun(ts): 
    global emyc
    global hwnd

    # 检测天使插件 COM Object 是否建立成功
    need_ver = '4.019'
    if(ts.ver() != need_ver): 
        logsystem.logging.warning('Register failed')
        return 
    logsystem.logging.info('Register successful')

    # 绑定窗口
    hwnd = ts.FindWindow("", "阴阳师-网易游戏")
    ts_ret = ts.BindWindow(hwnd, 'dx2', 'windows', 'windows', 0)
    if(ts_ret != 1): 
        logsystem.logging.warning('Binding failed')
        return 
    logsystem.logging.info('Binding successful')
	
    mysleep(2000)

    # 颜色 Debug 测试 
    while True:
        tscoldebug = ts.GetColor(1, 1)
        logsystem.logging.info(tscoldebug)
        if tscoldebug != "000000" and tscoldebug != "ffffff":
            break
        mysleep(200)
    logsystem.logging.info('Passed color debug')

    # 御魂战斗主循环
    while True:
        dog.feed()
        # 在御魂主选单，点击“挑战”按钮, 需要使用“阵容锁定”！
        wtfc1(ts, 807, 442, "f3b25e", 807, 881, 442, 459, 0, 1, hwnd)
        logsystem.logging.info('Already clicked TIAO-ZHAN')

        #wtfc1(ts, 1033, 576, "e6c78f", 1004, 1073, 465, 521, 0, 1)
        #print('already clicked ZHUN-BEI')

        # 检测是否进入战斗
        while True:
            rejxs(ts)
            dog_response()
            colib = ts.GetColor(71, 577)
            if colib == "f7f2df":
                break
            mysleep(500)
        logsystem.logging.info("Now we are in the battle")

        # 在战斗中，自动点怪
        while True:
          rejxs(ts)
          dog_response()

          # 点击中间怪物
          if emyc == 1:
            crnd(ts, 509, 579, 153, 181)

          # 点击右边怪物
          elif emyc == 2:
            crnd(ts, 773, 856, 159, 190)

          mysleep(500, 500)

          rejxs(ts)
          colib = ts.GetColor(71, 577)
          if colib != "f7f2df":
              break
        logsystem.logging.info("Battle finished")
		
		# 显示时间
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(dog.lastime[0])))
        print()

        # 在战斗结算页面
        while True: 
          dog_response()
          rejxs(ts)
          crnd(ts, 980, 1030, 225, 275)

          coljs = ts.GetColor(807, 442)
          if coljs == "f3b25e":
              break
          mysleep(500, 500)
        logsystem.logging.info("back to YUHUN level selection")

def bind_two_windows(ts_d, ts_f): 
    hwnd_raw = ts_d.EnumWindowByProcess("onmyoji.exe", "", "", 16)
    HWND = hwnd_raw.split(',')
    logsystem.logging.info('windows handle:', HWND)

    if len(HWND)!=2: 
        logsystem.logging.warning('Need 2 windows!')
        return 10 

    # 绑定窗口
    ts_ret = ts_d.BindWindow(HWND[0], 'dx2', 'windows', 'windows', 0) 
    if(ts_ret != 1): 
        logsystem.logging.warning('first window binding failed')
        return 1
    ts_ret = ts_f.BindWindow(HWND[1], 'dx2', 'windows', 'windows', 0) 
    if(ts_ret != 1): 
        logsystem.logging.warning('second window binding failed')
        return 2
    mysleep(500)

    if ts_f.GetColor(*pos_button_start_battle) == col_button_yellow: 
        #ts_d, ts_f = ts_f, ts_d
        logsystem.logging.info("handle swapped, don't worry")
        HWND[1], HWND[0]=HWND[0], HWND[1]
        ts_ret = ts_d.BindWindow(HWND[0], 'dx2', 'windows', 'windows', 0) 
        ts_ret = ts_f.BindWindow(HWND[1], 'dx2', 'windows', 'windows', 0) 
    elif ts_d.GetColor(*pos_button_start_battle) == col_button_yellow: 
        pass 
    else: 
        logsystem.logging.warning("didn't find KAI-SHI-ZHAN-DOU, can't distinguish which one is driver ")
        return 20

    logsystem.logging.info('binding successful')
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
        rejxs(ts)
        dog_response()
        crnd(ts, *pos_jiesuan)

        mysleep(500, 500)

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
            logsystem.logging.info('fighter (auto) accept found at', ffc_ret)
            wtfc1(ts, ffc_ret[1], ffc_ret[2], col_to_be_found, 
                ffc_ret[1]-5, ffc_ret[1]+5, ffc_ret[2]-5, ffc_ret[2]+5, 
                0, 1, hwnd)
            logsystem.logging.info('fighter clicked (auto) accept')

        coljs = ts.GetColor(*pos_button_start_battle)
        if coljs == col_fighter_start_battle_blank: 
            logsystem.logging.info('fighter in XIE ZHAN DUI WU!')
            battle_failed_status = 0 
            stats = 1 
            break 
    logsystem.logging.info('fighter stats =', stats)

def driver_jiesuan(ts, hwnd): 
    stats = 0
    while stats == 0: 
        rejxs(ts)
        dog_response()
        crnd(ts, *pos_jiesuan)
        mysleep(500, 500)
        coljs = ts.GetColor(*pos_button_continue_invite)
        if coljs == col_button_yellow:
            if ts.GetColor(499, 321) == '725f4d': 
                # 这里意味着 勾选 继续邀请队友
                wtfc1(ts, 499, 321, '725f4d', 499-5, 499+5, 321-5, 321+5, 0, 1, hwnd)
                logsystem.logging.info('ticked MO REN YAO QING DUI YOU')
            else: 
                # 如果没有这个选项，说明战斗失败，这里不需要打勾
                logsystem.logging.warning('failed')
                global battle_failed_status 
                battle_failed_status = 1 
            wtfc1(ts, *pos_button_continue_invite, col_button_yellow, 
                pos_button_continue_invite[0]-5, pos_button_continue_invite[0]+5, 
                pos_button_continue_invite[1]-5, pos_button_continue_invite[1]+5, 
                0, 1, hwnd)
            logsystem.logging.info('clidked QUE REN, JI XU YAO QING DUI YOU')
            #stats = 1
            #break 
        
        coljs = ts.GetColor(*pos_button_start_battle)
        if coljs == col_button_yellow: 
            logsystem.logging.info('driver is in XIE ZHAN DUI WU')
            stats = 2 
            break 
    logsystem.logging.info('driver stats =', stats)

# 双人模式
def dual_yuhun(ts_d, ts_f): 
    global emyc

    # 检测 COM Object 是否建立成功
    need_ver = '4.019'
    if ts_d.ver() != need_ver or ts_f.ver() != need_ver: 
        logsystem.logging.warning('register failed')
        return 
    logsystem.logging.info('register successful')

    # 绑定两个游戏窗口, ts_d = driver = 司机, ts_f = fighter = 打手
    btw_ret = bind_two_windows(ts_d, ts_f)
    if btw_ret != 0: 
        return 

    # 御魂战斗主循环
    while True: 
        # 司机点击开始战斗
        # 需要锁定阵容！
        dog.feed()
        wtfc1(ts_d, *pos_button_start_battle, col_button_yellow, 
            868, 986, 523, 545, 0, 1, HWND[0])
        logsystem.logging.info('clicked KAI-SHI-ZHAN-DOU!')

        #判断是否已经进入战斗 
        while True: 
            col_d = ts_d.GetColor(pos_zidong[0], pos_zidong[1])
            col_f = ts_f.GetColor(pos_zidong[0], pos_zidong[1])
            if col_d == col_zidong or col_f == col_zidong: 
                break
            mysleep(50)
            dog_response()
        logsystem.logging.info('in the battle!')

        # 已经进入战斗，司机自动点怪
        while True:
            rejxs(ts_d)
            rejxs(ts_f)
            dog_response()

            # 点击中间怪物
            if emyc == 1:
                crnd(ts_d, *pos_middle_monster)

            # 点击右边怪物
            elif emyc == 2:
                crnd(ts_d, *pos_right_monster)

            mysleep(500, 500)

            rejxs(ts_d)
            rejxs(ts_f)
            col_d = ts_d.GetColor(pos_zidong[0], pos_zidong[1])
            col_f = ts_f.GetColor(pos_zidong[0], pos_zidong[1])
            if col_d != col_zidong and col_f != col_zidong: 
                break
        logsystem.logging.info('battle finished!')

        thr_f_j = threading.Thread(target=fighter_jiesuan, args=(ts_f,HWND[1],))
        thr_d_j = threading.Thread(target=driver_jiesuan, args=(ts_d,HWND[0],))

        thr_f_j.start() 
        thr_d_j.start() 

        thr_f_j.join()
        thr_d_j.join()

        logsystem.logging.info('joined, new cycle!')
    

if __name__ == "__main__":    
    logsystem.logging.info('python version: %s', sys.version)

    # 需要提前在 windows 中注册 TSPlug.dll
    # 方法: regsvr32.exe TSPlug.dll

    # Reference: http://timgolden.me.uk/pywin32-docs/html/com/win32com/HTML/QuickStartClientCom.html
    # 建立 COM Object
    
    try:
        if is_admin():
        # 注册插件，获取权限
            logsystem.logging.info('UAC pass')
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
        logsystem.logging.info('terminated')
        if(mode==0):
            logsystem.logging.info('UnBindWindow return:', ts.UnBindWindow())
        elif(mode==1):
            logsystem.logging.info("unbind results:", unbind_two_windows(ts_d, ts_f))
        os.system('regsvr32.exe /u C://TSPlug.dll')
    else:
        quit()