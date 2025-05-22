<div align="center">

<a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot" /></a>
<a href="https://clovers-project.github.io/"><img src="./icon.svg" width="200" height="200" alt="clovers" /></a>

<b><font size="6">NoneBot Clovers Client</font></b>

✨ 对接 NoneBot 框架的 clovers 寄生客户端 ✨

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/nonebot-plugin-clovers.svg)](https://pypi.python.org/pypi/nonebot-plugin-clovers)
[![pypi download](https://img.shields.io/pypi/dm/nonebot-plugin-clovers)](https://pypi.python.org/pypi/nonebot-plugin-clovers)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Github](https://img.shields.io/badge/GitHub-Clovers-00CC33?logo=github)](https://github.com/clovers-project/clovers)
[![LICENSE](https://img.shields.io/github/license/clovers-project/nonebot-plugin-clovers.svg)](https://github.com/clovers-project/nonebot-plugin-clovers)

</div>

# 介绍

[项目地址](https://github.com/clovers-project/nonebot-plugin-clovers)

本模块在 NoneBot 内部运行，寄生方式为 nonebot.on_message 响应器

# 配置与使用方法

首先先安装本模块

<details open>
<summary>pip</summary>

```bash
pip install nonebot_plugin_clovers
```

</details>

<details>
<summary>poetry</summary>

```bash
poetry add nonebot_plugin_clovers
```

</details>

打开 NoneBot 项目目录下的 pyproject.toml 文件，添加 nonebot_plugin_clovers 到 plugins

```toml
# pyproject.toml
[tool.nonebot]
...
plugins = ["nonebot_plugin_clovers"]
```

然后在 nb 项目文件夹下创建 clovers.toml ,填写如下配置

```toml
# clovers.toml
[clovers]
plugins = ["clovers_setu_collection"]
plugin_dirs = [ "./clovers_library/plugins"]
using_adapters = ["nonebot_plugin_clovers.adapters.onebot.v11"]
```

`plugins` 加载插件的模块名列表
`plugin_dirs` 插件模块的目录列表，目录下的所有符合 python 模块名的文件都会被加载
`using_adapters` 加载适配器的模块名列表

这样就完成了对接

每个 using_adapters 内的元素都会添加一个监听事件，时间类型由模块内的 handler 函数的参数类型列表决定。

此外在插件内可以像这样使用 NoneBot Clovers Client 加载 clovers 插件

```python
from nonebot_plugin_clovers import get_client

get_client().load_plugin("clovers_setu_collection")
```

# 适用于 NoneBot Clovers Client 的适配器

适配器方法能够使用的参数：

- `bot`: `Bot` 的子类，具体为 Handler 内指定的参数类型
- `event`: `Event` 的子类，具体为 Handler 内指定的参数类型

所有适配器都会被添加一个名为 Bot_Nickname 的属性方法，用于获取当前 Bot 的昵称。

适配器模块内应该定义一个名为 handler 的异步函数，NoneBot 进程会根据函数参数类型签名来触发响应。

例：

```python
async def handler(bot: Bot, event: MessageCreatedEvent, matcher: Matcher): ...
```

# 预制的适配器 adapter

adapters 提供了如下适配器：

**ONEBOT.V11**

适用于 nonebot.adapters.onebot.v11 适配器的 clover 适配器，用于响应 MessageEvent 事件

**SATORI**

适用于 nonebot.adapters.satori 适配器的 clover 适配器，用于响应 MessageCreateEvent 事件

**QQ.GROUP**

适用于 nonebot.adapters.qq 适配器的 clover 适配器，用于响应 GroupAtMessageCreateEvent 事件

**QQ.GUILD**

适用于 nonebot.adapters.qq 适配器的 clover 适配器，用于响应 AtMessageCreateEvent 事件

_因为 qq 适配器的群组/频道消息事件差别过大，所以分成了 QQ.GROUP 和 QQ.GUILD 两个适配器_

这些适配器全部实现了如下 5 种发送方法

`text` 纯文本消息

数据类型 `str`

`image` 图片消息

数据类型 `str`,`Path`,`bytes`,`io.BytesIO` 。

`str` 类型被认为是网络位置

`voice` 语音消息

数据类型 `str`,`Path`,`bytes`,`io.BytesIO` 。

`str` 类型被认为是网络位置

`list` 图片文字混合消息

数据类型 `list[Result]`，适配器会尝试拼接列表中结果的类型，基本上仅支持 `text` 和 `image`，部分适配器还支持 `at` @群内成员

`segmented` 分段发送消息

数据类型 `AsyncGenerator` 异步生成器，生成的元素是 `Result` 类型，每段消息在生成时发送。

_因为 qq 适配器语音消息需要 silk 格式的音频而其他适配器有的并不支持此格式，所以这些适配器同名方法并不等价_

_包内的适配器方法仅作为适配器写法示例，并不作为任何标准，不建议直接调用。_

# 故事

- [nonebot2](https://github.com/nonebot/nonebot2) 跨平台 Python 异步聊天机器人框架
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) 基于 Mirai 以及 MiraiGo 的 OneBot Golang 原生实现
- [unidbg-fetch-qsign](https://github.com/fuqiuluo/unidbg-fetch-qsign) unidbg 模拟实现 QQ 签名计算
- [LiteLoaderQQNT](https://liteloaderqqnt.github.io/) LiteLoaderQQNT QQNT 插件加载器
- [Chronocat](https://github.com/chrononeko/chronocat) 模块化的 Satori 框架
- [OpenShamrock](https://github.com/whitechi73/OpenShamrock) 基于 Lsposed 的 OneBot11 协议的 Bot 框架
- [Lagrange.Core](https://github.com/LagrangeDev/Lagrange.Core) 基于 Konata 的 NTQQ 协议的纯 C#实现
- [LLOneBot](https://github.com/LLOneBot/LLOneBot) 实现 OneBot 11 和 Satori 协议，用于 QQ 机器人开发
- [NapCatQQ](https://github.com/NapNeko/NapCatQQ) NapCatQQ 是现代化的基于 NTQQ 的 Bot 协议端实现
