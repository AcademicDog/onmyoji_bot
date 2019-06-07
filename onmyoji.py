import win32com.client 
import sys 
import os
import ctypes
import threading

import fighter_driver
import logsystem
import utilities
import single_fight

# 参数

col_fighter_start_battle_blank = 'c7bdb4'

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
log = logsystem.WriteLog()

def init():
    global mode
    global emyc
    global done
    
    try:
        # 模式选择
        mode=int(input('\n选择游戏模式(Ctrl-C跳过并单刷)：\n0-单刷\n1-本地双开\n2-组队司机\n3-组队打手\n'))
        if(mode==1) or (mode==3):
            log.writewarning('未开发，告辞！')
            exit()
        elif((mode!=2) and (mode!=0)):
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

def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def yuhun():
    '''御魂战斗'''
    if mode == 0:
        # 单刷
        fight = single_fight.SingleFight(done, emyc)
        fight.start()
    
    if mode == 2:
        fight = fighter_driver.DriverFighter(mode, done, emyc)
        fight.single_start()
        # 司机

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
        # 检测管理员权限
        if is_admin():
            # 注册插件，获取权限
            log.writeinfo('UAC pass')
            os.system('regsvr32.exe C://TSPlug.dll')

            # 设置战斗参数
            init()

            # 开始战斗              
            yuhun()
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
        pass