# CHANGELOG

## v1.0.1.030?
#### Fixes (bugs & defects):
* 修复探索乘客不能自动退出。

## v1.0.1.0307
#### Fixes (bugs & defects):
*  双开探索时，队长退出后等待1s再邀请队员。
*  重写了日志系统，使之更规范合理。
*  修复了双开御魂乘客、司机争相标记。
*  优化了最后截图保存，现在最后运行截图将会以时间作为文件名，而不是统一的full.png。
*  调整了UI菜单栏，增加了向说明页面的导向，添加donate按钮。
*  修复了探索打完BOSS后，没有宝箱使得无法有效退出的问题。

## v1.0.1.0304
#### New features:
*  探索双开
#### Fixes (bugs & defects):
*  修复了探索副本中不停反复点击准备按钮的问题。
*  修复了部分玩家BitBlt失败的问题。
*  优化了结算

## v1.0.1.0301
#### New features:
*  增加延迟设定选项。
#### Fixes (bugs & defects):
*  根据[#48](https://github.com/AcademicDog/onmyoji_bot/issues/48)，优化了御魂司机的标记。

## v1.0.1.0229
#### New features:
*  增加了更详细的调试信息显示。
#### Fixes (bugs & defects):
*  进一步提高了结算可靠性。
*  进一步提高了结算速度。

## v1.0.1.0227
#### New features:
*  新增对MuMu模拟器的支持。
#### Fixes (bugs & defects):
*  现在结算不怕点到好友头像、战斗数据、各种加成了。 
*  提高了结算速度。
*  修复了司机不等乘客的问题。

## v1.0.1.0226
#### New features:
*  取消了满级狗粮识别的延迟设定，现在改为更智能的自动处理方式。
*  针对近期鬼使黑的问题，大幅优化了结算方式。

## v1.0.1.0224
#### New features:
*  系统缩放自适应。
*  增加了游戏次数的选项。
*  增加了游戏结束后的选项。
*  为本程序增加了图标。

## v1.0.1.0221
#### New features:
*  采用了新的算法，大幅度提高了图片识别的准确性，目前在部分场景有应用。
*  新增3个场景，识别御魂、业原火、卑弥呼副本。
*  提高了经验怪的识别率。
#### Fixes (bugs & defects):
*  提高了单刷稳定性。
*  缩小了结算点击范围，防止点到战斗数据。
*  将默认识图阈值从0.97降低为0.9。

## v1.0.1.0220
#### New features:
*  根据[#22](https://github.com/AcademicDog/onmyoji_bot/issues/22)，增加了御魂标记己方式神的选项。
#### Fixes (bugs & defects):
*  修复了上一个版本无法选择所上卡片的bug。
*  修复了UI中某些元素没对齐的bug。

## v1.0.1.0219
#### Fixes (bugs & defects):
*  抛弃PyQt，用tkinter重写ui，以减小文件体积。

## v1.0.1.0211
#### New features:
*  根据[#39](https://github.com/AcademicDog/onmyoji_bot/issues/39)，增加了更换素材和R卡的选项。

## v1.0.1.0210
#### New features:
*  前后台分离，目前编译为2个.exe文件，前后台分离。既可以ui运行，也可以单独控制台运行。
#### Fixes (bugs & defects):
*  调整了日志记录系统。
*  应用界面调整。

## v1.0.1.0106
#### New features:
*  完善了刷御灵的流程。
*  在程序出现异常崩溃时捕获TrackBack至log.log。

## v1.0.1.0102
#### New features:
*  增加了简单的自检逻辑。
#### Fixes (bugs & defects):
*  根据[#28](https://github.com/AcademicDog/onmyoji_bot/issues/28)，修复了探索的时候如果拉到场景图的最后，不会判断有没有经验怪的问题。
*  修复了双开结束后不清除窗口信息的问题。

## v1.0.0.1129
#### Fixes (bugs & defects):
*  调整了探索战斗的结算逻辑，现在不检查邮箱图标了，同时修复[#21](https://github.com/AcademicDog/onmyoji_bot/issues/21)、[#28](https://github.com/AcademicDog/onmyoji_bot/issues/28)。
*  删除了冗余代码。
*  根据[#24](https://github.com/AcademicDog/onmyoji_bot/issues/24)，调整了结算点击范围。

## v1.0.0.1009
#### New features:
*  增加了探索中“满级狗粮识别延迟”的设置选项。
#### Fixes (bugs & defects):
*  调整了御魂战斗的结算逻辑。

## v1.0.0.1008
#### Fixes (bugs & defects):
*  减小了结算图片的尺寸，这样在非28章探索也能顺利结算了。

## v1.0.0.1001
#### New features:
*  新增了场景识别，目前涉及的场景仅有4个，即0-其他; 1-庭院; 2-探索界面; 3-章节界面; 4-探索内。因此场景识别仅针对探索有效。进一步测试后将会逐渐推广。

## v1.0.0.0930
#### New features:
*  新增了御魂本地双开的初始代码，目前还在测试中

## v1.0.0.0929
#### New features:
*  新增御魂双开选项，代码目前还在调试
#### Fixes (bugs & defects):
*  修复了御魂战斗有时候会把御魂识别为“MAIL.png”，从而导致逻辑混乱的问题。
*  修复了打完boss仍然会继续探索的bug。

## v1.0.0.0927
#### New features:
*  更新了UI系统，现在预留了更多的设置空间。
*  增加了狗粮更换滑块，现在可以自由设置狗粮更换的式神进度。
#### Fixes (bugs & defects):
*  修复了某些情况下，打完boss脚本会死掉的情况。
*  根据[#14](https://github.com/AcademicDog/onmyoji_bot/issues/14)，修复了乘客在庭院上车，可能会出现进入其他界面问题。

## v1.0.0.0926
#### Fixes (bugs & defects):
*  修复了部分模型过大（如茨林、拍屁股），导致无法有效更换满级狗粮的问题。

## v1.0.0.0924
#### Fixes (bugs & defects):
*  改进了脚本的结束按钮，现在点击“结束”不再退出脚本UI。
*  将部分英文日志记录更改为中文。

## v1.0.0.0922
#### New features:
*  优化了更换满级狗粮，现在更换狗粮时会拖动至10% N卡进度条。
*  为GameControl模块增加了默认参数“quit_game_enable=1”。
*  优化了更新日志的展示方式，现在更新日志为独立文件。
*  代码中开源了界面文件。
#### Fixes (bugs & defects):
*  改进了探索结算点击的代码：适当增加了进入探索的延迟，同时降低了结算点击的延迟。
*  根据[#15](https://github.com/AcademicDog/onmyoji_bot/issues/15)，增加了百度网盘的下载地址。

## v1.0.0.0920
根据[#12](https://github.com/AcademicDog/onmyoji_bot/issues/12)适配了新版本UI。

## v1.0.0.0918
由于在某些情况下还是存在着异常退出的问题，增加“是否打BOSS”的选项按钮，让玩家自行决定。同时“超时时间”、“是否自动退出阴阳师游戏等”选项目前已可以使用。

## v1.0.0.0907
根据[#8](https://github.com/AcademicDog/onmyoji_bot/issues/8)、[#10](https://github.com/AcademicDog/onmyoji_bot/issues/10)，修复了部分情况下会导致程序卡死的bug，同时修复了打BOSS后异常的bug。

## v1.0.0.0904
由于打完BOSS后不能正常开始下一轮，临时移除打BOSS。

## v1.0.0.0827
重新调整了代码文件组织架构，明确了功能模块，方便后续开发。

## v1.0.0.0804
增加了探索完成后打BOSS的代码。

## v1.0.0.0728
根据[#6](https://github.com/AcademicDog/onmyoji_bot/issues/6)，优化了满级狗粮识别代码。

## v1.0.0.0724
优化了探索代码。

## v1.0.0.0711
根据[#5](https://github.com/AcademicDog/onmyoji_bot/issues/5)，调整了结算点击位置。

## v1.0.0.0710
增加了单人探索的代码。

## v1.0.0.0707
根据[#4](https://github.com/AcademicDog/onmyoji_bot/issues/4)，调整了UI设计。

## v1.0.0.0625
增加了UI，目前在ui分支中。

## v1.0.0.0623
调整了结算时开蛋的点击，现在不会在主界面仍然无脑点击了，同时优化了司机结算代码，移除了激活窗口代码。

## v1.0.0.0622
根据[#3](https://github.com/AcademicDog/onmyoji_bot/issues/3)，优化了乘客结算代码；将原先的灰度图像识别更改为彩色图像识别；在结算失败时，通过激活窗口来提醒玩家。

## v1.0.0.06211
根据[#2](https://github.com/AcademicDog/onmyoji_bot/issues/2)，增加了对已编译文件使用的说明，同时将/img文件夹一起打包发布。

## v1.0.0.0621
修改了完成战斗后，等待时间重复计算的bug，同时移除了不必要的参数设置。

## v1.0.0.0619
抛弃dll插件，用win32api，同时用图像识别替代简单找色。





