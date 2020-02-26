import tkinter as tk
import tkinter.messagebox
from tkinter import ttk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
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
        menu1.add_command(label='About', command=self.say_hi)

        # 链接
        menubar.add_cascade(label="File", menu=menu1)

        # 设置
        self.master.config(menu=menubar)

    def create_title(self):
        # 标题
        tk.Label(self.master, text='OnmyojiBot',
                 font='Helvetica 20 bold').pack(anchor=tk.W)
        tk.Label(
            self.master, text='https://github.com/AcademicDog/onmyoji_bot').pack(anchor=tk.W)

        # 主页面
        self.main_frame1 = tk.Frame(self.master)
        self.main_frame2 = tk.Frame(self.master)
        self.main_frame1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.main_frame2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

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
        submode = tk.LabelFrame(self.frame0, text='副本')
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
        # 提示文本
        textframe = tk.Frame(self.frame2)
        textframe.pack(expand=True, fill=tk.BOTH)
        s = tk.Scrollbar(textframe)
        s.pack(side=tk.RIGHT)
        text = tk.Text(textframe, height=5, width=21)
        text.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        text.insert(tk.INSERT, '把狗粮队长放在最左边，点开需要打的章节，然后开始。\n')
        text.insert(tk.INSERT, '支持自动换狗粮，只打经验怪。\n')
        text.insert(tk.END, '最好把“合并相同式神”选项关闭。\n')
        s.config(command=text.yview)
        text.config(yscrollcommand=s.set, state=tk.DISABLED)

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
            tk.END, '网址：https://github.com/AcademicDog/onmyoji_bot\n\n交流Q群：592055060')
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
        self.params.config(state=tk.NORMAL)
        self.params.insert(tk.END, '##########################\n')
        self.params.insert(tk.END, 'run_section: ' +
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
            "OnmyojiBot", '网址：https://github.com/AcademicDog/onmyoji_bot\n\n交流Q群：592055060')

    def start_onmyoji(self):
        self.show_params()

    def stop_onmyoji(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
