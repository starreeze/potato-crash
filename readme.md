# manual for _PotatoCrash_

_PotatoCrash_ v0.9.9: NJU 老版教务平台抢课程序，支持体育补选，阅读补选，公选课补选，导学研讨课补选和跨专业补选。

因为老版系统已经停止使用，因此我将本项目完全开源，供需要者研究。

## LICENSE

~~You **understand and agree** that:~~

- ~~Although I strive to provide a good service, program sometimes would fail and **users of the program may take full responsibility** for any consequences;~~
- ~~without specific permission, you are **NOT** allowed to~~
  - ~~put it to commercial use;~~
  - ~~redistribute it, **including sharing with your friends**;~~
  - ~~modify the code and claim your ownership.~~

~~But if you really want to modify or redistribute it, feel free to contact me. ^\_^~~

**This project is now under the GPLv3 License.**

_Copyright (C) 2020~2022 by **xsy**._

Contact me by:

- xingshangyu100@gmail.com
- [github.com/xingshangyu](https://github.com/xingshangyu)

## 功能说明

### 配置环境

- python 3.8
- python 包：

  - requests
  - bs4
  - lxml

  如果你需要阻止系统休眠，还需要安装

  - pyuserinput

- 连接校内网

### 填写用户信息

1. 将选课网站**登陆后**的 cookie 填写到代码 user.py 第 2 行的单引号内。如果不知道如何获取网页 cookie 和安装 python 及相关包，建议百度；
1. 第3行campus为校区，可填写仙林或鼓楼；
2. 如果你需要使用长时间挂机选课功能（通常用于及时捡漏其他人退选的课程），建议使用阻止系统休眠的功能，它将免去你手动设置系统不休眠的麻烦（更麻烦的是你会忘了再改回来）。将 user.py 第 34行的 False 改为 True 即可，注意要安装 pyuserinput。
3. user.py 的 debug 请始终置为 False。

### 使用方式

有两种方式，分别为交互式和文件式。

#### 交互式

直接运行 main.py，不带参数。终端输入 `python3 main.py`。

待其加载完成，打印输入提示符 `>>` 时，可输入命令，输入格式见[说明](#输入格式)。

#### 文件式

将命令按照输入格式（格式与交互式完全相同）预先写入一个任意名称的文件 ，然后将文件路径作为参数传递给 main.py。使用终端运行，例如：

`linux/macos: python3 main.py path/to/your/file`

`dos/windows: python3 main.py path\to\your\file`

注意：文件内容只有第一行有效，因为 _potatoCrash_ 的有效命令几乎都是阻塞的，顺序运行无意义。

### 输入格式

`<cmd> [options] [parameters]`

如果你觉得说明写得不清楚或者太长不想看，你可以直接去看[示例](#示例)。

#### 命令(cmd)

目前有 4 个命令

- print：打印课程列表
- select：根据 id 抢课（按照给定间隔不断发送选课请求，直到成功）
- rush：根据指定的筛选条件抢课（最常用）
- exit：退出程序

#### 选项(options)

只有一个 -h ，含义为隐藏人数已满或自己已选的课程（仅对 print 有效）。

#### 详细说明

##### print

`print <course type> [academy]`

- course type 可能取值如下：

  - gym: 体育课补选；
  - read: 阅读补选；
  - public: 公选补选；
  - discuss: 导学研讨补选；
  - open: 跨专业补选。
- 如果 course type 为 open，需要填写 academy，academy 是一个整数，是教务网上跨专业补选的“开课院系”菜单栏的对应院系的序号（从1开始），例如：1是文学院，2是历史学院，……，11是数学系，……；
- 输出：选择的课程类型的可选列表。

##### select

`select <interval> <course type> [academy] [<course id>] [<course id>] ...`

- interval 是发送选课请求的间隔时间（以秒为单位，可输入小数）；
- course type 含义同上；
- 如果是跨专业补选，需要输入 academy，选其他课请忽略；
- 后面可以跟多个`<course id>`，程序将一并选择，course id 即上面 print 命令输出结果的最后一列；
- 输出：成功或失败的信息。

##### rush

`rush <interval> <course type> [academy] [<name> <time> <teacher>] [<name> <time> <teacher>] ...`

- course type, academy 和 interval 含义同上；
- 后面可以跟多组 `<name> <time> <teacher>`，程序将一并选择，其中

  - name 为课程名称；
  - time 为课程时间；
  - teacher 为授课教师。

- 注意：
  - 上述三种信息只要是实际的字符串子串（用 python 字符串的 in 判断），就视为匹配；
  - 用英文下划线\_代表空串（匹配所有信息）。
- 输出：成功或失败的信息。

#### 示例

##### 交互式

```PotatoCrash
# 打印公选课补选列表
>> print public

# 隐藏已选和人满
>> print gym -h

# 选择编号为12345，54321和66666的研讨导学课，刷新时间间隔1s
>> select 1 discuss 12345 54321 66666

# 跨专业选择：数学系的拓扑学，班级、时间和教师任意，刷新间隔2min（用于长时间运行程序挂机捡漏）
>> rush 120 open 11 拓扑学 _ _

# 选择羽毛球课，时间是1-2节，教师任意，刷新时间间隔0.5s
>> rush 0.5 gym 羽毛球 1-2 _

# 选择红楼梦阅读，时间任意，教师是苗**，刷新间隔2min
>> rush 120 read 红楼梦 _ 苗

# 同时选择钢琴基础和钢琴提高，刷新时间间隔为0，时间和教师任意
>> rush 0 public 钢琴基础 _ _ 钢琴提高 _ _
```

##### 文件式

见文本文件 cmd.pc （可使用任意文本编辑器打开）。

### 注意

1. 再次强调：恳请使用者遵守 LICENSE 的规则~~，不要将本程序公开或分发给他人~~！
2. 鉴于阅读补选近期改了接口，大概率体育补选也要改接口，但已经来不及测试了，相关代码可能会失效；
3. cookie 有时效（约几个小时），到时报错需要重新获取；
5. 间隔为 0 的刷新不建议持续太长时间，可能会对教务系统服务器造成压力，也有被封号的风险；
6. 仅在 linux 平台上测试过，鉴于 python 的跨平台特性，mac/windows 大概率没问题，但不能保证（尤其是阻止系统休眠的功能，使用前请自行测试，如果出现 bug，请不要开启）；
7. 程序健壮性较低，易崩溃，请严格按照说明使用。特别地，命令必须一次性输入完（不能删除再输入和移动光标），否则会识别不了（似乎与终端不完全支持中文有关），因此更建议使用文件式；
8. 程序可能有 bug，使用后建议进入教务处手动检查；
9. 谨慎低调使用。

## Change log

- v0.0.1, 2020.09 ：实现基本的打印课程列表、选择课程等功能。
- v0.1.0, 2020.09：新增按照课程名、时间、教师名等信息抢课的 rush 命令，增强程序健壮性，输出信息提示更合理。
- v0.1.1, 2021.01 ：新增阅读补选，删除冗余命令 watch，编写 readme 使用说明。
- v0.1.2, 2021.03：内部逻辑优化以提高效率，修复原来不能再使用的阅读补选（可能是由于教务处接口更换），新增公选和导学研讨补选，修改 LINSENCE 和 manual。
- v0.1.3, 2021.06：模块化重构，修复体育补选接口，增加阻止系统休眠功能。（尝试添加 GUI，失败——未找到好用的 python 图形库。git branch: gui）。
- v0.2.0, 2021.08：新增同时选择同一类多个课程的功能，重写使用说明。（尝试使 print 的输出更整齐，失败——各个操作系统终端对中文的处理不尽相同，过于复杂。git branch: print format）
- v0.2.1, 2021.09：新增文件式使用方式。（尝试支持学号密码登录，失败——网页一直返回错误：验证码过期。git branch: auto-login）。
- v0.2.2, 2021.09：新增跨专业补选。
- v0.9.9, 2022.07 (**The End**)：老版系统已停止使用，本项目完全开源，License改为GPLv3，后续不再维护更新。
