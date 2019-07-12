# 欢迎

如果您对本[项目](https://github.com/AcademicDog/onmyoji_bot)感兴趣，欢迎加入[我们](https://github.com/AcademicDog/onmyoji_bot/graphs/contributors)！

## 主要功能
本工具用于阴阳师代肝，为各位阴阳师大佬养老护肝所用。

![Branching](https://raw.githubusercontent.com/AcademicDog/myresource/master/usage.png)

### 特性

- 御魂
  - 单人御魂
  - 作为司机组队御魂，自动邀请
  - 作为乘客组队御魂，自动接受邀请
  - 双开御魂
- 业原火
  - 自动刷贪、嗔、痴卷
- 御灵
  - 自动刷御灵
- 探索
  - 完成探索，识别经验怪，支持自动换狗粮

**此外，本脚本能识别卡机、体力空等异常情况，在出现异常后自动退出阴阳师客户端，防止浪费加成。**

### 使用环境

> 阴阳师PC版客户端，默认分辨率(1136x640)
>
> Windows 10和Windows 7，屏幕(1920x1080)，显示设置100%
>
> 如需运行源码，需要Python3 32位

* * *

# 使用方法

### 单人刷御魂/业原火/御灵

1.  打开本工具，切换至御魂选项卡；

1.  游戏中进入御魂/业原火/御灵主界面（就是有“挑战”按钮的页面），请提前备好式神并**锁定阵容**；

1.  点击本工具的“开始”按钮。

### 组队刷御魂

1.  打开本工具，切换至御魂选项卡，根据自身情况选择“单人司机”或者“单人乘客”；

1.  游戏中进入组队页面，请提前备好式神并**锁定阵容**；

1.  点击本工具的“开始”按钮。

### 单人探索

1.  打开本工具，切换至探索选项卡；

1.  在游戏种提前将狗粮队长放在阴阳师最左边，并且**取消锁定阵容**；

1.  游戏中点开需要探索的章节（就是有“探索”按钮的页面）；

1.  点击本工具的“开始”按钮。

* * *

# 更新日志

*   v1.0.0.0619--抛弃dll插件，用win32api，同时用图像识别替代简单找色。
*   v1.0.0.0621--修改了完成战斗后，等待时间重复计算的bug，同时移除了不必要的参数设置。
*   v1.0.0.06211--根据[#2](https://github.com/AcademicDog/onmyoji_bot/issues/2)，增加了对已编译文件使用的说明，同时将/img文件夹一起打包发布。
*   v1.0.0.0622--根据[#3](https://github.com/AcademicDog/onmyoji_bot/issues/3)，优化了乘客结算代码；将原先的灰度图像识别更改为彩色图像识别；在结算失败时，通过激活窗口来提醒玩家。
*   v1.0.0.0623--调整了结算时开蛋的点击，现在不会在主界面仍然无脑点击了，同时优化了司机结算代码，移除了激活窗口代码。
*   v1.0.0.0625--增加了UI，目前在ui分支中。
*   v1.0.0.0707--根据[#4](https://github.com/AcademicDog/onmyoji_bot/issues/4)，调整了UI设计。
*   v1.0.0.0710--增加了单人探索的代码。
*   v1.0.0.0711--根据[#5](https://github.com/AcademicDog/onmyoji_bot/issues/5)，调整了结算点击位置。

### 下一步工作计划

暂无

* * *

# 特别感谢
特别感谢society765在本项目中给与的启发，本项目在其[工作基础](https://github.com/society765/yys-auto-yuhun)上修改完成。

同时感谢sup817ch的图像识别思路，本项目game_ctl模块基于其[工作基础](https://github.com/sup817ch/AutoOnmyoji)。

感谢每一个在[ISSUE](https://github.com/AcademicDog/onmyoji_bot/issues)中提出问题的人。