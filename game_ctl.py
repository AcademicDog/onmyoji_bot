import ctypes
import sys
import time
import random
import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from PIL import Image

class GameControl():
    def __init__(self,window_name):
        self.hwnd = win32gui.FindWindow(0,window_name)

    def window_full_shot(self,file_name=None):
        """
        窗口截图
            :param file_name=None: 截图文件的保存名称
            :return: file_name为空则返回RGB数据
        """
        try:
            l, t, r, b = win32gui.GetWindowRect(self.hwnd)
            #39和16为Window与Client高和宽的差值
            h = b - t - 39
            w = r - l - 16
            hwindc = win32gui.GetWindowDC(self.hwnd)
            srcdc = win32ui.CreateDCFromHandle(hwindc)
            memdc = srcdc.CreateCompatibleDC()
            bmp = win32ui.CreateBitmap()
            bmp.CreateCompatibleBitmap(srcdc, w, h)
            memdc.SelectObject(bmp)
            memdc.BitBlt((0, 0), (w, h), srcdc, (8, 31), win32con.SRCCOPY)
            if file_name!=None:
                bmp.SaveBitmapFile(memdc,file_name)
                srcdc.DeleteDC()
                memdc.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwindc)
                win32gui.DeleteObject(bmp.GetHandle())
                return
            else:
                signedIntsArray = bmp.GetBitmapBits(True)
                img = np.fromstring(signedIntsArray, dtype='uint8')
                img.shape = (h, w, 4)                
                srcdc.DeleteDC()
                memdc.DeleteDC()
                win32gui.ReleaseDC(self.hwnd, hwindc)
                win32gui.DeleteObject(bmp.GetHandle())
                #cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))
                #cv2.waitKey(0)
                return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        except:
            pass

    def window_part_shot(self,pos1,pos2,file_name=None):
        """
        窗口区域截图
            :param pos1: (x,y) 截图区域的左上角坐标
            :param pos2: (x,y) 截图区域的右下角坐标
            :param file_name=None: 截图文件的保存路径
            :return: file_name为空则返回RGB数据
        """
        w=pos2[0]-pos1[0]
        h=pos2[1]-pos1[1]
        hwindc = win32gui.GetWindowDC(self.hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, w, h)
        memdc.SelectObject(bmp)
        memdc.BitBlt((0, 0), (w, h), srcdc, (pos1[0]+8, pos1[1]+31), win32con.SRCCOPY)
        if file_name!=None:
            bmp.SaveBitmapFile(memdc,file_name)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            return
        else:
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())            
            return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

    def find_color(self,region,color,tolerance=0):
        """
        寻找颜色
            :param region: ((x1,y1),(x2,y2)) 欲搜索区域的左上角坐标和右下角坐标
            :param color: (r,g,b) 欲搜索的颜色
            :param tolerance=0: 容差值
            :return: 成功返回客户区坐标，失败返回-1
        """
        img=Image.fromarray(self.window_part_shot(region[0],region[1]),'RGB')
        width,height=img.size
        r1,g1,b1=color[:3]
        for x in range(width):
            for y in range(height):
                try:
                    pixel=img.getpixel((x,y))
                    r2,g2,b2=pixel[:3]
                    if abs(r1-r2)<=tolerance and abs(g1-g2)<=tolerance and abs(b1-b2)<=tolerance:
                        return x+region[0][0],y+region[0][1]
                except:
                    return -1
        return -1

    def check_color(self,pos,color,tolerance=0):
        """
        对比窗口内某一点的颜色
            :param pos: (x,y) 欲对比的坐标
            :param color: (r,g,b) 欲对比的颜色 
            :param tolerance=0: 容差值
            :return: 成功返回True,失败返回False
        """
        img=Image.fromarray(self.window_full_shot(),'RGB')
        r1,g1,b1=color[:3]
        r2,g2,b2=img.getpixel(pos)[:3]
        if abs(r1-r2)<=tolerance and abs(g1-g2)<=tolerance and abs(b1-b2)<=tolerance:
            return True
        else:
            return False

    def find_img(self,img_template_path):
        """
        查找图片
            :param img_template_path: 欲查找的图片路径
            :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
        """
        img_src = self.window_full_shot()
        img_template=cv2.imread(img_template_path,0)
        res = cv2.matchTemplate(img_src, img_template, cv2.TM_CCOEFF_NORMED)
        minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
        #print(maxLoc)
        return maxVal,maxLoc

    def activate_window(self):
        user32 = ctypes.WinDLL('user32.dll')
        user32.SwitchToThisWindow(self.hwnd,True)

    def mouse_move(self,pos,pos_end=None):
        """
        模拟鼠标移动
            :param pos: (x,y) 鼠标移动的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标移动至以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
        """
        pos2 = win32gui.ClientToScreen(self.hwnd,pos)
        if pos_end==None:
            win32api.SetCursorPos(pos2)
        else:
            pos_end2=win32gui.ClientToScreen(self.hwnd,pos_end)
            pos_rand = (random.randint(pos2[0],pos_end2[0]),random.randint(pos2[1],pos_end2[1]))
            win32api.SetCursorPos(pos_rand)

    def mouse_click(self):
        """
        鼠标单击
        """
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        time.sleep(0.05)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

    def mouse_drag(self,pos1,pos2):
        """
        鼠标拖拽
            :param pos1: (x,y) 起点坐标
            :param pos2: (x,y) 终点坐标
        """
        pos1_s=win32gui.ClientToScreen(self.hwnd,pos1)
        pos2_s=win32gui.ClientToScreen(self.hwnd,pos2)
        screen_x=win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_y=win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        start_x=pos1_s[0]*65535//screen_x
        start_y=pos1_s[1]*65535//screen_y
        dst_x=pos2_s[0]*65535//screen_x
        dst_y=pos2_s[1]*65535//screen_y
        move_x=np.linspace(start_x,dst_x,num=20,endpoint=True)[0:]
        move_y=np.linspace(start_y,dst_y,num=20,endpoint=True)[0:]
        self.mouse_move(pos1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
        for i in range(20):
            x=int(round(move_x[i]))
            y=int(round(move_y[i]))
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE|win32con.MOUSEEVENTF_ABSOLUTE,x,y,0,0)
            time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

    def mouse_click_bg(self,pos,pos_end=None):
        """
        后台鼠标单击
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
        """
        if pos_end==None:
            win32gui.SendMessage(self.hwnd,win32con.WM_MOUSEMOVE,0,win32api.MAKELONG(pos[0],pos[1]))
            win32gui.SendMessage(self.hwnd,win32con.WM_LBUTTONDOWN,0,win32api.MAKELONG(pos[0],pos[1]))
            time.sleep(random.randint(20,80)/1000)
            win32gui.SendMessage(self.hwnd,win32con.WM_LBUTTONUP,0,win32api.MAKELONG(pos[0],pos[1]))
        else:
            pos_rand = (random.randint(pos[0],pos_end[0]),random.randint(pos[1],pos_end[1]))
            win32gui.SendMessage(self.hwnd,win32con.WM_MOUSEMOVE,0,win32api.MAKELONG(pos_rand[0],pos_rand[1]))
            win32gui.SendMessage(self.hwnd,win32con.WM_LBUTTONDOWN,0,win32api.MAKELONG(pos_rand[0],pos_rand[1]))
            time.sleep(random.randint(20,80)/1000)
            win32gui.SendMessage(self.hwnd,win32con.WM_LBUTTONUP,0,win32api.MAKELONG(pos_rand[0],pos_rand[1]))
    
    def mouse_drag_bg(self,pos1,pos2):
        """
        后台鼠标拖拽
            :param pos1: (x,y) 起点坐标
            :param pos2: (x,y) 终点坐标
        """
        move_x=np.linspace(pos1[0],pos2[0],num=20,endpoint=True)[0:]
        move_y=np.linspace(pos1[1],pos2[1],num=20,endpoint=True)[0:]
        win32gui.SendMessage(self.hwnd,win32con.WM_LBUTTONDOWN,0,win32api.MAKELONG(pos1[0],pos1[1]))
        for i in range(20):
            x=int(round(move_x[i]))
            y=int(round(move_y[i]))
            win32gui.SendMessage(self.hwnd,win32con.WM_MOUSEMOVE,0,win32api.MAKELONG(x,y))
            time.sleep(0.01)
        win32gui.SendMessage(self.hwnd,win32con.WM_LBUTTONUP,0,win32api.MAKELONG(pos2[0],pos2[1]))

    def wait_game_img(self, img_path, max_time = 30, quit=True):
        """
        等待游戏图像
            :param img_path: 图片路径
            :param max_time=30: 超时时间
            :param quit=True: 超时后是否退出
            :return: 成功返回True，失败返回False
        """
        start_time=time.time()
        while time.time()-start_time<=max_time:
            maxVal,maxLoc=self.find_img(img_path)
            if maxVal>0.97:
                return True
            if max_time > 5:
                time.sleep(1)
            else:
                time.sleep(0.1)
        if quit:
            # 超时则退出游戏
            self.quit_game()
        else:
            return False
    
    def wait_game_color(self,region,color,tolerance=0,max_time=60,quit=True):
        """
        等待游戏颜色
            :param region: ((x1,y1),(x2,y2)) 欲搜索的区域
            :param color: (r,g,b) 欲等待的颜色
            :param tolerance=0: 容差值
            :param max_time=30: 超时时间
            :param quit=True: 超时后是否退出
            :return: 成功返回True，失败返回False
        """
        self.rejectbounty()
        start_time=time.time()
        while time.time()-start_time<=max_time:
            pos=self.find_color(region,color)
            if pos!=-1:
                return True
            time.sleep(1)
        if quit:
            #超时则退出游戏
            self.quit_game()
        else:
            return False

    def quit_game(self):
        """
        退出游戏
        """
        self.takescreenshot() #保存一下现场
        win32gui.SendMessage(self.hwnd,win32con.WM_DESTROY,0,0) #退出游戏
        sys.exit(0)

    def takescreenshot(self):
        '''
        截图
        '''
        img_src_path='img\\full.png'
        self.window_full_shot(img_src_path)

    def rejectbounty(self):
        '''
        拒绝悬赏
            :return: 拒绝成功返回True，其他情况返回False
        '''
        maxVal, maxLoc = self.find_img('img\\XUAN-SHANG.png')
        print(maxVal, maxLoc)
        if maxVal>0.97:
            self.mouse_click_bg((757,460))
            return True
        return False

#测试用
def main():
    yys=GameControl(u'阴阳师-网易游戏')
    #yys.mouse_click_bg((427,419),(457,452))
    #yys.mouse_drag_bg((1130,118),(20,118))
    #print(yys.window_full_shot('tmp\\full.png'))
    #print(yys.find_color(((380,200),(480,400)),(251,237,2),3))
    #print(yys.find_color(((630,250),(730,450)),(251,237,2),3))
    #print(yys.find_color(((1006,526),(1058,549)),(242,215,165),0))

if __name__ == '__main__':
    main()
