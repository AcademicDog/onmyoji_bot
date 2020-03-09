# 欢迎

[![GitHub release](https://img.shields.io/github/release/academicdog/onmyoji_bot)](https://github.com/AcademicDog/onmyoji_bot/releases) ![GitHub top language](https://img.shields.io/github/languages/top/academicdog/onmyoji_bot) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/academicdog/onmyoji_bot) ![GitHub repo size](https://img.shields.io/github/repo-size/academicdog/onmyoji_bot) ![GitHub](https://img.shields.io/github/license/academicdog/onmyoji_bot)
![platforms](https://img.shields.io/badge/platform-win32|win64-brightgreen.svg) [![GitHub issues](https://img.shields.io/github/issues/academicdog/onmyoji_bot.svg)](https://github.com/academicdog/onmyoji_bot/issues) [![GitHub closed issues](https://img.shields.io/github/issues-closed/academicdog/onmyoji_bot.svg)](https://github.com/academicdog/onmyoji_bot/issues?q=is:issue+is:closed) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/academicdog/onmyoji_bot) ![GitHub contributors](https://img.shields.io/github/contributors/academicdog/onmyoji_bot.svg)

如果您对本[项目](https://github.com/AcademicDog/onmyoji_bot)感兴趣，欢迎加入[我们](https://github.com/AcademicDog/onmyoji_bot/graphs/contributors)！

* * *

# 主要功能
本工具用于阴阳师代肝，为各位阴阳师大佬养老护肝所用。
<img align="right" width="220" src="https://onmyojibot.oss-cn-beijing.aliyuncs.com/usage.png
" alt="copy URL to clipboard" />

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
  - 完成单人探索，识别经验怪，支持自动换狗粮
  - 作为队长组队探索，自动邀请
  - 作为队员组队探索，自动接受邀请
  - 双开探索
- 其他
  - 在战斗过程中，该脚本会自动拒绝所有悬赏封印的邀请。
  - 如果一定时间程序没有任何操作（卡机、体力空等），视为体力用光，为了保护加成，自动关闭YYS。
  - 该脚本仅使用了画面找色，鼠标后台点击的函数，完全模拟人类玩家行为，没有使用任何内存读写函数。在敏感位置添加了均匀分布的随机时间漂移，和随机坐标漂移。**但仍然可能存在使用风险**。
  - 该脚本自动兼容不同分辨率屏幕的系统缩放。
  - 具有一定的场景识别功能，部分副本可以在庭院内启动。

### 使用环境

> 阴阳师PC版客户端，默认分辨率(1136x640) 或者 阴阳师MuMu模拟器，分辨率设置为(1136x640)
>
> Windows 10
>
> 如需运行源码，需要Python3 32位

### 文件列表

**以下内容如果你不了解也没有关系，直接执行ui.exe就可以运行。**

本工具主要文件如下：
- /img文件夹
- CHANGELOG.md
- onmyoji.exe
- ui.exe
- conf_example.ini

其中/img文件夹包含了找图识图的素材，.png格式，可以用一般的截图软件截取。

CHANGELOG.md是更新日志。

onmyoji.exe是核心文件，包含整个脚本的运行逻辑，需要配合conf.ini配置文件使用。配置文件模板是conf_example.ini。

ui.exe是程序界面，主要作用是生成onmyoji.exe运行所需要的配置文件conf.ini并调用onmyoji.exe。

* * *

# 使用方法

使用方法请看[这里](https://doc.onmyojibot.com/)。

* * *

# 更新日志

更新日志请点击[这里](https://github.com/AcademicDog/onmyoji_bot/blob/master/CHANGELOG.md)

* * *

# 特别感谢
同[README.md](https://github.com/AcademicDog/onmyoji_bot/blob/master/README.md)。

# 捐赠

量力而行，1分就够。

<img align="right" height="150" src="https://onmyojibot.oss-cn-beijing.aliyuncs.com/donate/any.jpg" />

<img align="right" height="150" src="https://onmyojibot.oss-cn-beijing.aliyuncs.com/donate/1.jpg"/>

<img align="right" height="150" src="https://onmyojibot.oss-cn-beijing.aliyuncs.com/donate/0.01.jpg" />

同时请备注id，将来你的id将会出现在[赞助者名单](https://academicdog.github.io/onmyoji_bot/sponsors.html)中。