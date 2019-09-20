# 欢迎

[![GitHub release](https://img.shields.io/github/release/academicdog/onmyoji_bot)](https://github.com/AcademicDog/onmyoji_bot/releases) ![GitHub top language](https://img.shields.io/github/languages/top/academicdog/onmyoji_bot) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/academicdog/onmyoji_bot)  ![GitHub repo size](https://img.shields.io/github/repo-size/academicdog/onmyoji_bot)    ![GitHub](https://img.shields.io/github/license/academicdog/onmyoji_bot)   ![platforms](https://img.shields.io/badge/platform-win32|win64-brightgreen.svg) [![GitHub issues](https://img.shields.io/github/issues/academicdog/onmyoji_bot.svg)](https://github.com/academicdog/onmyoji_bot/issues) [![GitHub closed issues](https://img.shields.io/github/issues-closed/academicdog/onmyoji_bot.svg)](https://github.com/academicdog/onmyoji_bot/issues?q=is:issue+is:closed)  ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/academicdog/onmyoji_bot)  ![GitHub contributors](https://img.shields.io/github/contributors/academicdog/onmyoji_bot.svg)

<img align="right" width="300" src="https://raw.githubusercontent.com/AcademicDog/myresource/master/usage.png" alt="copy URL to clipboard" />

本工具用于阴阳师代肝，为各位阴阳师大佬养老护肝所用。

目前已开通项目网站，请访问🌍[此地址](https://academicdog.github.io/onmyoji_bot/)获取最新信息。

# 特别感谢

特别感谢society765在本项目中给与的启发，本项目在其[工作基础](https://github.com/society765/yys-auto-yuhun)上修改完成。

同时感谢sup817ch的图像识别思路，本项目game_ctl模块基于其[工作基础](https://github.com/sup817ch/AutoOnmyoji)。

# 注意事项

环境：python 3.7, 32 bit；yys PC端 默认分辨率 (1136x640)；win 10系统，屏幕(1920x1080)，显示设置100%。

1.  窗口现在可以完全后台，可以被遮挡，但是**不能最小化**。

1.  不要开启游戏中的“模型描边”。

1.  当使用 Windows 7 系统时，需要调整系统的画面设置：把主题调为最丑最挫的那个。在 Windows 10 系统中，不需要调整系统画面设置。

1.  当使用高分辨率屏幕时，在阴阳师客户端程序兼容性选项里，不要勾选“替代高DPI缩放行为”，这个选项应该是默认不勾选的。

1.  如果不想安装运行环境，可以访问下载最新已[编译](https://github.com/AcademicDog/onmyoji_bot/releases)版本，该版本有图形界面，同时注意.exe文件和/img文件夹应该放在同一目录后再运行。

1.  探索换狗粮的时候，默认是换上第一个N卡，因此注意**不要**对N卡点击“喜欢”，导致反复换上一个满级的狗粮。 

# 更新说明
v1.0.0.0619--抛弃dll插件，用win32api，同时用图像识别替代简单找色。

v1.0.0.0621--修改了完成战斗后，等待时间重复计算的bug，同时移除了不必要的参数设置。

v1.0.0.06211--根据[#2](https://github.com/AcademicDog/onmyoji_bot/issues/2)，增加了对已编译文件使用的说明，同时将/img文件夹一起打包发布。

v1.0.0.0622--根据[#3](https://github.com/AcademicDog/onmyoji_bot/issues/3)，优化了乘客结算代码；将原先的灰度图像识别更改为彩色图像识别；在结算失败时，通过激活窗口来提醒玩家。

v1.0.0.0623--调整了结算时开蛋的点击，现在不会在主界面仍然无脑点击了，同时优化了司机结算代码，移除了激活窗口代码。

v1.0.0.0625--增加了UI，目前在ui分支中。

v1.0.0.0707--根据[#4](https://github.com/AcademicDog/onmyoji_bot/issues/4)，调整了UI设计。

v1.0.0.0710--增加了单人探索的代码。

v1.0.0.0711--根据[#5](https://github.com/AcademicDog/onmyoji_bot/issues/5)，调整了结算点击位置。

v1.0.0.0724--优化了探索代码。

v1.0.0.0728--根据[#6](https://github.com/AcademicDog/onmyoji_bot/issues/6)，优化了满级狗粮识别代码。

v1.0.0.0804--增加了探索完成后打BOSS的代码。

v1.0.0.0827--重新调整了代码文件组织架构，明确了功能模块，方便后续开发。

v1.0.0.0904--由于打完BOSS后不能正常开始下一轮，临时移除打BOSS。

v1.0.0.0907--根据[#8](https://github.com/AcademicDog/onmyoji_bot/issues/8)、[#10](https://github.com/AcademicDog/onmyoji_bot/issues/10)，修复了部分情况下会导致程序卡死的bug，同时修复了打BOSS后异常的bug。

v1.0.0.0918--由于在某些情况下还是存在着异常退出的问题，增加“是否打BOSS”的选项按钮，让玩家自行决定。同时“超时时间”、“是否自动退出阴阳师游戏等”选项目前已可以使用。

v1.0.0.0920--根据[#12](https://github.com/AcademicDog/onmyoji_bot/issues/12)适配了新版本UI。

# 协议 (License)

该源代码使用了 [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) 开源协议。

This project is licensed under the [GPLv3](https://www.gnu.org/licenses/gpl-3.0.html) license.