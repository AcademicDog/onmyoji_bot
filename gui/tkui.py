import json
import tkinter as tk
import tkinter.messagebox
import webbrowser
from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.url = 'http://www.onmyojibot.com'
        self.source_url = 'https://github.com/AcademicDog/onmyoji_bot'
        self.master = master
        self.master.iconbitmap('img/icon/OnmyojiBot.ico')
        self.master.wm_title('OnmyojiBot')
        self.pack()

        # 初始化参数
        self.run_section = 0
        self.run_mode = tk.IntVar()
        self.run_submode = tk.IntVar()
        self.max_times = tk.IntVar()

        self.watchdog_enable = tk.BooleanVar()
        self.max_win_time = tk.IntVar()
        self.max_op_time = tk.IntVar()

        self.explore_mode = tk.IntVar(value=0)
        self.gouliang_1 = tk.BooleanVar(value=False)
        self.gouliang_2 = tk.BooleanVar(value=True)
        self.gouliang_3 = tk.BooleanVar(value=True)
        self.gouliang_4 = tk.BooleanVar(value=False)
        self.gouliang_5 = tk.BooleanVar(value=False)
        self.fight_boss_enable = tk.BooleanVar()
        self.slide_shikigami = tk.BooleanVar()
        self.slide_shikigami_progress = tk.IntVar()
        self.change_shikigami = 1

        self.debug_enable = tk.BooleanVar()

        self.run_mode.set(0)
        self.run_submode.set(0)
        self.max_times.set(0)
        self.watchdog_enable.set(True)
        self.max_win_time.set(100)
        self.max_op_time.set(20)
        self.fight_boss_enable.set(False)
        self.slide_shikigami.set(True)
        self.slide_shikigami_progress.set(10)
        self.debug_enable.set(False)

        # 创建菜单栏
        self.create_menubar()

        # 创建标题
        self.create_title()

        # 创建客户端选项
        self.create_client()

        # 创建选项卡
        self.create_section()

        # 创建选项
        self.create_frame0()
        self.create_frame1()
        self.create_frame2()
        self.create_frame3()

        # 创建次数菜单
        self.create_times()

        # 创建高级菜单
        self.create_advance()

        # 创建日志
        self.create_log()

        # 创建操作按钮
        self.create_command()

    def create_menubar(self):
        '''
        创建菜单栏
        '''
        menubar = tk.Menu(self.master)

        # 创建菜单项
        menu1 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=menu1)
        menu1.add_command(label='启动', command=self.start_onmyoji)
        menu1.add_command(label='退出', command=self.stop_onmyoji)

        # 高级选项
        menu2 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="高级", menu=menu2)
        menu2.add_command(label='自定义延迟', command=self.delay_dialog)

        # 帮助
        menu3 = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label='帮助', menu=menu3)
        menu3.add_command(label='关于', command=self.say_hi)
        menu3.add_command(label='使用说明', command=self.help)
        menu3.add_separator()
        menu3.add_command(label='捐赠', command=self.donate)

        # 设置
        self.master.config(menu=menubar)

    def create_title(self):
        # 标题
        tk.Label(self.master, text='OnmyojiBot',
                 font='Helvetica 20 bold').pack(anchor=tk.W)
        tk.Label(
            self.master, text=self.url).pack(anchor=tk.W)

        # 主页面
        self.main_frame1 = tk.Frame(self.master)
        self.main_frame2 = tk.Frame(self.master)
        self.main_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def create_client(self):
        '''
        创建客户端选项
        '''
        self.client = ttk.Combobox(self.main_frame2)
        self.client['value'] = ('阴阳师桌面版-默认分辨率', 'MuMu模拟器-1136*640 (100%缩放)')
        self.client.pack(fill=tk.X, padx=2, pady=2)
        self.client.current(0)
        self.client.config(state='readonly')

    def create_section(self):
        '''
        创建主选项卡
        '''
        self.section = ttk.Notebook(self.main_frame1)

        # 创建选项卡1---御魂
        self.frame0 = tk.Frame(self.section)
        self.section.add(self.frame0, text='御魂')

        # 创建选项卡2---御灵
        self.frame1 = tk.Frame(self.section)
        self.section.add(self.frame1, text='御灵')

        # 创建选项卡3---探索
        self.frame2 = tk.Frame(self.section, padx=5, pady=5)
        self.section.add(self.frame2, text='探索')

        # 创建选项卡4---关于
        self.frame3 = tk.Frame(self.section)
        self.section.add(self.frame3, text='关于')

        self.section.pack(fill=tk.BOTH, expand=True)

    def create_frame0(self):
        '''
        御魂参数
        '''
        # 游戏模式
        mode = tk.LabelFrame(self.frame0, text='模式')
        mode.pack(padx=5, pady=5, fill=tk.BOTH)
        self.run_mode = tk.IntVar()
        self.run_mode.set(0)
        tk.Radiobutton(mode, text='单刷', variable=self.run_mode,
                       value=0).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(mode, text='单人司机', variable=self.run_mode,
                       value=1).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(mode, text='单人乘客', variable=self.run_mode,
                       value=2).grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(mode, text='双开', variable=self.run_mode,
                       value=3).grid(row=1, column=1, sticky=tk.W)

        # 游戏副本
        submode = tk.LabelFrame(self.frame0, text='副本(请锁定阵容)')
        submode.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        tk.Radiobutton(submode, text='八岐大蛇', variable=self.run_submode,
                       value=0).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(submode, text='业原火', variable=self.run_submode,
                       value=1).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(submode, text='卑弥呼', variable=self.run_submode,
                       value=2).grid(row=1, column=0, sticky=tk.W)

        # 标记式神
        mitama_mark = tk.Frame(self.frame0, padx=5, pady=5)
        mitama_mark.pack(fill=tk.X, expand=True)
        tk.Label(mitama_mark, text='标记己方式神:').pack(side=tk.LEFT)
        self.mitama_team_mark = ttk.Combobox(mitama_mark, width=10)
        self.mitama_team_mark['value'] = (
            '不标记', '第1个式神', '第2个式神', '第3个式神', '第4个式神', '第5个式神')
        self.mitama_team_mark.pack(fill=tk.X, expand=True, padx=2)
        self.mitama_team_mark.current(0)
        self.mitama_team_mark.config(state='readonly')

    def create_frame1(self):
        '''
        御灵参数
        '''
        text = tk.Text(self.frame1, height=5, width=25)
        text.pack(padx=5, pady=5, expand=True, fill=tk.BOTH, anchor=tk.NW)
        text.insert(tk.END, '选择好要打的御灵及层数，点击开始按钮即可。')
        text.config(state=tk.DISABLED)

    def create_frame2(self):
        '''
        探索参数
        '''
        # 副本选择
        submode = tk.LabelFrame(self.frame2, text='模式')
        submode.pack(fill=tk.BOTH, expand=True)
        tk.Radiobutton(submode, text='单刷', variable=self.explore_mode,
                       value=0, command=lambda: self.gouliang_state(1)).grid(row=0, column=0, sticky=tk.W)
        tk.Radiobutton(submode, text='单人队长', variable=self.explore_mode,
                       value=1, command=lambda: self.gouliang_state(2)).grid(row=0, column=1, sticky=tk.W)
        tk.Radiobutton(submode, text='单人队员', variable=self.explore_mode,
                       value=2, command=lambda: self.gouliang_state(1)).grid(row=1, column=0, sticky=tk.W)
        tk.Radiobutton(submode, text='桌面版双开', variable=self.explore_mode,
                       value=3, command=lambda: self.gouliang_state(3)).grid(row=1, column=1, sticky=tk.W)

        # 狗粮设置
        food = tk.LabelFrame(self.frame2, text='更换狗粮 (勿锁定阵容)')
        food.pack(fill=tk.BOTH, expand=True)
        self.gouliang_l = tk.Checkbutton(
            food, text='左', variable=self.gouliang_1)
        self.gouliang_l.grid(row=0, column=0)
        self.gouliang_m = tk.Checkbutton(
            food, text='中', variable=self.gouliang_2)
        self.gouliang_m.grid(row=0, column=1)
        self.gouliang_r = tk.Checkbutton(
            food, text='右', variable=self.gouliang_3)
        self.gouliang_r.grid(row=0, column=2)
        tk.Label(food, text='单人/队员').grid(row=0, column=3, sticky=tk.W)

        self.gouliang_lb = tk.Checkbutton(
            food, text='左', variable=self.gouliang_4)
        self.gouliang_lb.grid(row=1, column=0)
        self.gouliang_rb = tk.Checkbutton(
            food, text='右', variable=self.gouliang_5)
        self.gouliang_rb.grid(row=1, column=2)
        tk.Label(food, text='队长').grid(row=1, column=3, sticky=tk.W)
        self.gouliang_lb.config(state=tk.DISABLED)
        self.gouliang_rb.config(state=tk.DISABLED)

        # 换狗粮设置
        tk.Checkbutton(self.frame2, text='换狗粮拖放式神进度条，进度:',
                       variable=self.slide_shikigami).pack(anchor=tk.W)
        tk.Scale(self.frame2, from_=0, to=100, orient=tk.HORIZONTAL, showvalue=0,
                 variable=self.slide_shikigami_progress).pack(fill=tk.X)
        self.cmb = ttk.Combobox(self.frame2)
        self.cmb['value'] = ('更换素材', '更换N卡', '更换R卡')
        self.cmb.pack(fill=tk.X, padx=2)
        self.cmb.current(self.change_shikigami)
        self.cmb.config(state='readonly')

        # 打BOSS设置
        tk.Checkbutton(self.frame2, text='结束后打BOSS',
                       variable=self.fight_boss_enable).pack(anchor=tk.W)

    def create_frame3(self):
        '''
        关于
        '''
        text = tk.Text(self.frame3, height=5, width=25)
        text.pack(expand=True, fill=tk.BOTH)
        text.insert(
            tk.END, '网站：%s\n\n' % (self.url))
        text.insert(
            tk.END, '源码：%s\n\n' % (self.source_url))
        text.insert(
            tk.END, '交流Q群：592055060\n\n')
        text.insert(
            tk.END, '如果觉得脚本动作太慢，请到高级菜单自定义延迟。')
        text.config(state=tk.DISABLED)

    def create_times(self):
        '''
        游戏次数
        '''
        times = tk.LabelFrame(self.main_frame1, text='次数设置')
        times.pack(padx=5, fill=tk.X, anchor=tk.W)
        timeframe1 = tk.Frame(times)
        timeframe1.pack(anchor=tk.W)
        tk.Label(timeframe1, text='游戏次数(0=无数次):').pack(side=tk.LEFT)
        tk.Entry(timeframe1, width=6, textvariable=self.max_times).pack()
        self.end_operation = ttk.Combobox(times)
        self.end_operation['value'] = ('结束后关闭脚本', '结束后关闭脚本和游戏')
        self.end_operation.pack(fill=tk.X, padx=2, pady=2)
        self.end_operation.current(0)
        self.end_operation.config(state='readonly')

    def create_advance(self):
        '''
        高级菜单
        '''
        advance = tk.LabelFrame(self.main_frame1, text='高级选项')
        advance.pack(padx=5, pady=5, fill=tk.X, side=tk.BOTTOM)
        tk.Checkbutton(advance, text='调试模式',
                       variable=self.debug_enable).pack(anchor=tk.W)
        tk.Checkbutton(advance, text='超时自动关闭阴阳师',
                       variable=self.watchdog_enable).pack(anchor=tk.W)
        frame = tk.Frame(advance)
        frame.pack(anchor=tk.W)
        tk.Label(frame, text='  画面超时时间(秒):').grid(row=0, column=0)
        tk.Entry(frame, textvariable=self.max_win_time,
                 width=5).grid(row=0, column=1)
        tk.Label(frame, text='  操作超时时间(秒):').grid(row=1, column=0)
        tk.Entry(frame, textvariable=self.max_op_time,
                 width=5).grid(row=1, column=1)

    def create_log(self):
        '''
        参数显示
        '''
        tk.Label(self.main_frame2, text='运行参数:').pack(anchor=tk.W)
        self.params = tk.Text(self.main_frame2, height=20, width=28)
        self.params.pack(anchor=tk.NW, fill=tk.BOTH,
                         padx=5, pady=5, expand=True)
        self.params.config(state=tk.DISABLED)

    def create_command(self):
        '''
        按钮
        '''
        button_area = tk.Frame(self.main_frame2)
        button_area.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=5)
        tk.Button(button_area, text='开始',
                  command=self.start_onmyoji).pack(fill=tk.X)
        tk.Button(button_area, text='退出',
                  command=self.stop_onmyoji).pack(fill=tk.X)

    def show_params(self):
        self.get_gouliang()
        self.params.config(state=tk.NORMAL)
        self.params.insert(tk.END, '########1.0.1.0304########\n')
        self.params.insert(tk.END, 'client: ' + str(self.client.current()))
        self.params.insert(tk.END, '\nrun_section: ' +
                           str(self.section.index('current')))
        self.params.insert(tk.END, '\nrun_mode: '+str(self.run_mode.get()))
        self.params.insert(tk.END, '\nrun_submode: ' +
                           str(self.run_submode.get()))
        self.params.insert(tk.END, '\nmax_times: ' + str(self.max_times.get()))
        self.params.insert(tk.END, '\nend_operation: ' +
                           str(self.end_operation.current()))
        self.params.insert(tk.END, '\nwatchdog_enable: ' +
                           str(self.watchdog_enable.get()))
        self.params.insert(tk.END, '\nmax_win_time: ' +
                           str(self.max_win_time.get()))
        self.params.insert(tk.END, '\nmax_op_time: ' +
                           str(self.max_op_time.get()))
        self.params.insert(tk.END, '\nmitama_team_mark: ' +
                           str(self.mitama_team_mark.current()))
        self.params.insert(tk.END, '\nexplore_mode: ' +
                           str(self.explore_mode.get()))
        self.params.insert(tk.END, '\ngouliang: ' + str(self.gouliang))
        self.params.insert(tk.END, '\ngouliang_b: ' + str(self.gouliang_b))
        self.params.insert(tk.END, '\nfight_boss_enable: ' +
                           str(self.fight_boss_enable.get()))
        self.params.insert(tk.END, '\nslide_shikigami: ' +
                           str(self.slide_shikigami.get()))
        self.params.insert(tk.END, '\nslide_shikigami_progress: ' +
                           str(self.slide_shikigami_progress.get()))
        self.params.insert(tk.END, '\nchange_shikigami: ' +
                           str(self.cmb.current()))
        self.params.insert(tk.END, '\ndebug_enable: ' +
                           str(self.debug_enable.get())+'\n')
        self.params.insert(tk.END, '##########################\n\n')
        self.params.see(tk.END)
        self.params.config(state=tk.DISABLED)

    def say_hi(self):
        '''
        测试
        '''
        tk.messagebox.showinfo(
            "OnmyojiBot", '网站：%s\n\n源码：%s\n\n交流Q群：592055060' % (self.url, self.source_url))

    def delay_dialog(self):
        pw = DelayDialog(self)
        self.wait_window(pw)

    def help(self):
        '''
        使用说明
        '''
        Q = tk.messagebox.askyesno(
            "使用说明", '详细使用说明请参考%s\n\n是否访问？' % (self.url))
        if Q:
            webbrowser.open(self.url)

    def donate(self):
        '''
        捐赠
        '''
        Q = tk.messagebox.askyesno(
            "捐赠", '量力而行，1分就够。\n\n前往捐赠？')
        if Q:
            webbrowser.open('https://doc.onmyojibot.com/zh/latest/donate.html')

    def gouliang_state(self, state):
        '''
        禁用狗粮选项
            :param state: 1-仅启用3狗粮，2-禁用3狗粮，3-全启用
        '''
        if state == 1:
            self.gouliang_4.set(False)
            self.gouliang_5.set(False)
            self.gouliang_l.config(state=tk.NORMAL)
            self.gouliang_m.config(state=tk.NORMAL)
            self.gouliang_r.config(state=tk.NORMAL)
            self.gouliang_lb.config(state=tk.DISABLED)
            self.gouliang_rb.config(state=tk.DISABLED)
        elif state == 2:
            self.gouliang_1.set(False)
            self.gouliang_2.set(False)
            self.gouliang_3.set(False)
            self.gouliang_l.config(state=tk.DISABLED)
            self.gouliang_m.config(state=tk.DISABLED)
            self.gouliang_r.config(state=tk.DISABLED)
            self.gouliang_lb.config(state=tk.NORMAL)
            self.gouliang_rb.config(state=tk.NORMAL)
        elif state == 3:
            self.gouliang_l.config(state=tk.NORMAL)
            self.gouliang_m.config(state=tk.NORMAL)
            self.gouliang_r.config(state=tk.NORMAL)
            self.gouliang_lb.config(state=tk.NORMAL)
            self.gouliang_rb.config(state=tk.NORMAL)

    def get_gouliang(self):
        '''
        计算狗粮坐标
        '''
        # 前狗粮
        self.gouliang = []
        if self.gouliang_1.get():
            self.gouliang.append(1)
        if self.gouliang_2.get():
            self.gouliang.append(2)
        if self.gouliang_3.get():
            self.gouliang.append(3)

        # 后狗粮
        self.gouliang_b = []
        if self.gouliang_4.get():
            self.gouliang_b.append(4)
        if self.gouliang_5.get():
            self.gouliang_b.append(5)

    def start_onmyoji(self):
        self.show_params()

    def stop_onmyoji(self):
        pass


class DelayDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.title('延迟设置')
        self.parent = parent

        # 参数
        self.delay = {
            1: [tk.IntVar(value=1000), tk.IntVar(value=1500)],
            2: [tk.IntVar(value=1300), tk.IntVar(value=2100)],
            3: [tk.IntVar(value=1800), tk.IntVar(value=3000)],
            4: [tk.IntVar(value=2500), tk.IntVar(value=4000)],
            5: [tk.IntVar(value=3000), tk.IntVar(value=5000)]}

        # 延迟机制
        row1 = tk.Frame(self)
        row1.pack(fill=tk.X)
        tk.Label(row1, text='延迟机制：').pack(anchor=tk.W)
        text = tk.Text(row1, height=11, width=40)
        text.pack(expand=True, fill=tk.BOTH)
        text.insert(tk.END, '1-总共5级延迟，脚本随机从1-5级延迟中选择一级作为主延迟，\
同时在1-3级延迟中选择一级作为副延迟。在此基础上乘以随机系数。\n\n')
        text.insert(tk.END, '2-每5分钟刷新选择，计算单位毫秒。\n\n')
        text.insert(tk.END, '3-主延迟用于截图、识图等一般操作的延迟，副延迟主要用于结算。\n\n')
        text.insert(tk.END, '4-不要纠结为什么每次重开这个表格都不变，参数存在delay.json，重启有效。\n\n')
        text.config(state=tk.DISABLED)

        # 参数设置
        row2 = tk.Frame(self)
        row2.pack(fill=tk.X)
        tk.Label(row2, text='一级: ').grid(row=0, column=0)
        tk.Label(row2, text='最低').grid(row=0, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[1][0]).grid(
            row=0, column=3)
        tk.Label(row2, text='最高').grid(row=0, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[1][1]).grid(
            row=0, column=5)

        tk.Label(row2, text='二级: ').grid(row=1, column=0)
        tk.Label(row2, text='最低').grid(row=1, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[2][0]).grid(
            row=1, column=3)
        tk.Label(row2, text='最高').grid(row=1, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[2][1]).grid(
            row=1, column=5)

        tk.Label(row2, text='三级: ').grid(row=2, column=0)
        tk.Label(row2, text='最低').grid(row=2, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[3][0]).grid(
            row=2, column=3)
        tk.Label(row2, text='最高').grid(row=2, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[3][1]).grid(
            row=2, column=5)

        tk.Label(row2, text='四级: ').grid(row=3, column=0)
        tk.Label(row2, text='最低').grid(row=3, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[4][0]).grid(
            row=3, column=3)
        tk.Label(row2, text='最高').grid(row=3, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[4][1]).grid(
            row=3, column=5)

        tk.Label(row2, text='五级: ').grid(row=4, column=0)
        tk.Label(row2, text='最低').grid(row=4, column=1)
        tk.Entry(row2, width=7, textvariable=self.delay[5][0]).grid(
            row=4, column=3)
        tk.Label(row2, text='最高').grid(row=4, column=4)
        tk.Entry(row2, width=7, textvariable=self.delay[5][1]).grid(
            row=4, column=5)

        # 按钮
        row3 = tk.Frame(self)
        row3.pack(anchor=tk.E)
        tk.Button(row3, text='确定', command=self.confirm).grid(row=0, column=0)
        tk.Button(row3, text='取消', command=self.cancel).grid(row=0, column=1)

    def confirm(self):
        mydelay = {
            1: [self.delay[1][0].get(), self.delay[1][1].get() - self.delay[1][0].get()],
            2: [self.delay[2][0].get(), self.delay[2][1].get() - self.delay[2][0].get()],
            3: [self.delay[3][0].get(), self.delay[3][1].get() - self.delay[3][0].get()],
            4: [self.delay[4][0].get(), self.delay[4][1].get() - self.delay[4][0].get()],
            5: [self.delay[5][0].get(), self.delay[5][1].get() - self.delay[5][0].get()]}
        jsObj = json.dumps(mydelay)
        with open('delay.json', 'w') as f:
            f.write(jsObj)
        self.destroy()

    def cancel(self):
        self.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
