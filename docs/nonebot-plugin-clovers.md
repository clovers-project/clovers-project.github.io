<div align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
  <a href="https://clovers-project.github.io/">
    <img src="https://raw.githubusercontent.com/clovers-project/clovers.github.io/master/docs/icon.png" width="200" height="200" alt="clovers">
  </a>

<b><font size="6">NoneBot clovers 加载器</font></b>

✨ 专用对接 NoneBot 框架的预制 clovers 运行例 ✨

<img src="https://img.shields.io/badge/python-3.12+-blue.svg" alt="python">
<a href="https://github.com/clovers-project/nonebot-plugin-clovers/blob/master/LICENSE">
  <img src="https://img.shields.io/github/license/KarisAya/nonebot_plugin_clovers.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_clovers">
  <img src="https://img.shields.io/pypi/v/nonebot_plugin_clovers.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_clovers">
  <img src="https://img.shields.io/pypi/dm/nonebot_plugin_clovers" alt="pypi download">
</a>
</div>

# 介绍

本模块曾经为 NoneBot 插件。

但在 2.0 更新后移除了全部 on 响应器，不再对接响应。

只提供一个预制的 clovers 实例。

现在是普通的 python 模块。

# 使用方法

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

进入你的 nonebot 项目的插件目录，创建一个文件`connect_to_the_clovers.py`，内容如下：

<details close>
<summary>connect_to_the_clovers.py</summary>

```python
from nonebot import on_message, get_driver
from nonebot.matcher import Matcher
from nonebot_plugin_clovers import clovers, extract_command

driver = get_driver()
main = on_message(priority=20, block=False)

from nonebot.adapters.satori import Bot as SatoriBot
from nonebot.adapters.satori.event import MessageCreatedEvent as SatoriEvent
from nonebot_plugin_clovers.adapters.satori import adapter as satori_adapter

clovers.register_adapter(satori_adapter)
satori = clovers.leaf(satori_adapter.name)
driver.on_startup(satori.startup)
driver.on_shutdown(satori.shutdown)


@main.handle()
async def _(bot: SatoriBot, event: SatoriEvent, matcher: Matcher):
    message = extract_command(event.get_plaintext())
    if await satori.response(message, bot=bot, event=event):
        matcher.stop_propagation()


from nonebot.adapters.onebot.v11 import Bot as OnebotV11Bot, MessageEvent as OnebotV11Event
from nonebot_plugin_clovers.adapters.onebot.v11 import adapter as onebot_v11_adapter

clovers.register_adapter(onebot_v11_adapter)
onebot_v11 = clovers.leaf(onebot_v11_adapter.name)
driver.on_startup(onebot_v11.startup)
driver.on_shutdown(onebot_v11.shutdown)


@main.handle()
async def _(bot: OnebotV11Bot, event: OnebotV11Event, matcher: Matcher):
    message = extract_command(event.get_plaintext())
    if await onebot_v11.response(message, bot=bot, event=event):
        matcher.stop_propagation()


from nonebot.adapters.qq import Bot as QQBot
from nonebot.adapters.qq import GroupAtMessageCreateEvent as QQGroupEvent
from nonebot_plugin_clovers.adapters.qq.group import adapter as qq_group_adapter

clovers.register_adapter(qq_group_adapter)
qq_group = clovers.leaf(qq_group_adapter.name)
driver.on_startup(qq_group.startup)
driver.on_shutdown(qq_group.shutdown)


@main.handle()
async def _(bot: QQBot, event: QQGroupEvent, matcher: Matcher):
    message = extract_command(event.get_plaintext())
    if await qq_group.response(message, bot=bot, event=event):
        matcher.stop_propagation()


from nonebot.adapters.qq import AtMessageCreateEvent as QQGuildEvent
from nonebot_plugin_clovers.adapters.qq.guild import adapter as qq_guild_adapter

clovers.register_adapter(qq_guild_adapter)
qq_guild = clovers.leaf(qq_guild_adapter.name)
driver.on_startup(qq_guild.startup)
driver.on_shutdown(qq_guild.shutdown)


@main.handle()
async def _(bot: QQBot, event: QQGuildEvent, matcher: Matcher):
    message = extract_command(event.get_plaintext())
    if await qq_guild.response(message, bot=bot, event=event):
        matcher.stop_propagation()
```

</details>

这样就完成了对接

# 配置

本模块的配置在 clovers 的配置文件中的一个名为 `clovers` 的 table 中，配置项如下：

```toml
[clovers]
plugins = []
plugin_dirs = [ "./clovers_library/plugins",]
adapters = []
adapters_dirs = [ "./clovers_library/adapters",]
```

`plugins` 加载插件的模块名列表
`plugin_dirs` 插件模块的目录列表，目录下的所有符合 python 模块名的文件都会被加载
`adapters` 加载适配器的模块名列表
`adapters_dirs` 适配器的目录列表，目录下的所有符合 python 模块名的文件都会被加载

# 预制的 clovers 实例

模块下的 clovers 加载了全部配置中的插件和适配器，只需要调用 `clovers.leaf(adapter_name)` 方法即得到选定适配器的 Leaf 实例

# 预制的适配器 adapter

模块下的 adapters 仅是一个模块内的包，并不在模块初始化时被加载。

已完成的[适配器方法](https://github.com/KarisAya/nonebot_plugin_clovers/tree/master/nonebot_plugin_clovers/adapters)

adapters 提供了如下适配器：

**ONEBOT.V11**

适用于 nonebot.adapters.onebot.v11 适配器的 clover 适配器

**SATORI**

适用于 nonebot.adapters.satori 适配器的 clover 适配器

**QQ.GROUP**

适用于 nonebot.adapters.qq 适配器的 clover 适配器，专门响应 GroupAtMessageCreateEvent

**QQ.GUILD**

适用于 nonebot.adapters.qq 适配器的 clover 适配器，专门响应 AtMessageCreateEvent

_因为 qq 适配器的群组/频道消息事件差别过大，所以分成了 QQ.GROUP 和 QQ.GUILD 两个适配器_

这些适配器全部实现了如下 5 种发送方法

`text` 纯文本消息

数据类型 `str`

`image` 图片消息

数据类型 `str` 或 `bytes` 或 `io.BytesIO` 。

`str` 类型被认为是网络位置

`voice` 语音消息

数据类型 `str` 或 `bytes` 或 `io.BytesIO` 。

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
