import time
import random
import watchdog
import logsystem

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
    log = logsystem.WriteLog()
    colxs = ts.GetColor(750, 458)
    #print(colxs)
    if colxs == "df715e":
        crnd(ts, 750-5, 750+5, 458-5, 458+5)
        log.writeinfo("Successfully rejected bounty")
        mysleep(1000)
    mysleep(50)


def wtfc1(ts, colx, coly, coll, x1, x2, y1, y2, zzz, adv):
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
    dog = watchdog.Watchdog()  
    while j == 0:
        rejxs(ts)
        if(dog.bark() == 1):
            return 0
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
    return 1