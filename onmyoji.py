import win32com.client 
import sys 
import os
import ctypes
import threading

import fighter_driver
import fighter_passenger
import logsystem
import utilities
import single_fight

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
        if(mode==1):
            log.writewarning('未开发，告辞！')
            os._exit(0)
        elif(mode != 2 and mode != 0 and mode != 3):
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
        # 司机
        fight = fighter_driver.DriverFighter(mode, done, emyc)
        fight.single_start()
    
    if mode == 3:
        # 打手
        fight = fighter_passenger.FighterPassenger(mode, done, emyc)        
        fight.single_start()    

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

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)       
    except KeyboardInterrupt:        
        log.writeinfo('terminated')
        os.system('regsvr32.exe /u C://TSPlug.dll')
        os._exit(0)
    else:
        pass