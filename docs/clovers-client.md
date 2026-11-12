<div align="center">
<a href="https://clovers-project.github.io/"><img src="./icon.svg" width="200" height="200" alt="clovers" /></a>

<b><font size="6">Clovers Client</font></b>

✨ Clovers 客户端 ✨

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/clovers-client.svg)](https://pypi.python.org/pypi/clovers-client)
[![pypi download](https://img.shields.io/pypi/dm/clovers-client)](https://pypi.python.org/pypi/clovers-client)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Github](https://img.shields.io/badge/GitHub-Clovers-00CC33?logo=github)](https://github.com/clovers-project/clovers)
[![LICENSE](https://img.shields.io/github/license/clovers-project/clovers-client.svg)](https://github.com/clovers-project/clovers-client)

</div>

# clovers-client 使用文档

`clovers-client` 为 Clovers 插件提供事件属性、消息结果类型和平台适配器。插件通过统一的事件接口读取消息、调用平台能力并发送回复，适配器负责把这些操作转换成对应平台的行为。

本文依据 `clovers-client 0.3.8` 的代码编写，要求 Python 3.12 及以上，Clovers 依赖范围为 `>=0.5.0,<0.6.0`。下面以 console 为例：它启动 HTTP / WebSocket 服务器，供网页控制台连接，同时加载 Clovers 插件处理消息。

适配器可以扩展。本文会分别说明通用接口的约定和 console 的实际支持情况；协议中声明了某个属性或方法，不代表所有适配器都已经实现它。

## 1. 运行一个 console 服务器

### 1.1 安装

在准备用来运行机器人的目录中安装 console 所需的依赖：

```bash
python -m pip install "clovers-client[console]"
```

基础包 `clovers-client` 不包含全部 console 运行依赖，运行本文示例需要安装 `[console]`。

如果使用本项目源码，在源码仓库根目录执行：

```bash
python -m pip install -e ".[console]"
```

### 1.2 编写启动脚本

新建 `bot.py`，写入以下代码。这是使用者需要自行编写的入口：

```python
import asyncio

from clovers_client.console import Client

asyncio.run(Client().run())
```

在 `bot.py` 所在目录运行：

```bash
python bot.py
```

默认监听 `127.0.0.1:11000`，服务器启动后在浏览器访问：

```text
http://127.0.0.1:11000/
```

`Client` 是 `ConsoleClient` 的导出别名。创建客户端时会初始化日志、加载适配器与插件、创建数据目录并读取公开群组和令牌配置；`run()` 启动 Clovers 核心和 Web 服务，并保持运行。前台运行时可按 `Ctrl+C` 停止服务器。

默认没有加载任何插件，所以服务器能够接收消息，但不会自动回答。接下来添加一个最小插件验证完整流程。

### 1.3 加载一个会回复的插件

先停止服务器，按下面的结构准备文件：

```text
console-bot/
├── bot.py
├── clovers.toml
└── plugins/
    ├── __init__.py
    └── hello.py
```

`plugins/__init__.py` 留空，在 `plugins/hello.py` 中写入：

```python
from clovers import Plugin, Result
from clovers_client import Event

plugin = Plugin()


@plugin.handle(r"^ping$")
async def ping(event: Event):
    return Result("text", "pong")


@plugin.handle(r"^你好$", ["nickname", "user_id"])
async def hello(event: Event):
    return Result("text", f"你好，{event.nickname}！你的 ID 是 {event.user_id}。")


@plugin.handle(r"^复读\s+(.+)$")
async def echo(event: Event):
    return Result("text", event.args[0])
```

在 `clovers.toml` 中启用插件目录：

```toml
[clovers]
plugin_dirs = ["plugins"]
```

重新运行 `python bot.py`，打开网页控制台发送 `ping`，应收到 `pong`。发送 `你好` 会收到昵称与用户 ID；发送 `复读 测试消息` 会收到 `测试消息`。

这里的 `plugin` 必须是模块级的 `Plugin` 实例。加载器支持的实例名称包括 `PLUGIN`、`plugin` 和 `__plugin__`。默认 `Plugin()` 的响应器应返回 `clovers.Result` 或 `None`，不能直接用字符串代替 `Result("text", "...")`。

请始终从 `console-bot` 目录启动。配置文件、插件目录、日志和默认数据目录都与运行时的当前工作目录有关。

## 2. 配置

### 2.1 clovers.toml

默认读取当前工作目录下的 `clovers.toml`，console 配置位于 `[clovers]`。可以只填写需要修改的字段，其余字段使用默认值。

下面给出完整字段示例，其中 `plugin_dirs` 已启用上一节的插件目录：

```toml
[clovers]
LOG_FILE = "./log/clovers.log"
LOG_LEVEL = "DEBUG"
BOT_NICKNAME = "Bot酱"
BOT_AVATAR_URL = "/download/bot_avatar.png"

host = "127.0.0.1"
port = 11000
message_history_limit = 1000
data_dir = "./data/CloversConsole"

adapters = []
adapter_dirs = []
plugins = []
plugin_dirs = ["plugins"]
```

| 字段 | 默认值 | 用途 |
| --- | --- | --- |
| `LOG_FILE` | `"./log/clovers.log"` | 日志文件路径 |
| `LOG_LEVEL` | `"DEBUG"` | 终端日志等级，可选 `DEBUG`、`INFO`、`WARNING`、`ERROR`、`CRITICAL` |
| `BOT_NICKNAME` | `"Bot酱"` | 机器人昵称，也是 console 识别昵称前缀和 @ 的依据 |
| `BOT_AVATAR_URL` | `"/download/bot_avatar.png"` | 机器人头像地址 |
| `host` | `"127.0.0.1"` | 监听地址；需要其他设备访问时可设为 `"0.0.0.0"` |
| `port` | `11000` | 监听端口 |
| `message_history_limit` | `1000` | 内存中保留的广播消息数量上限 |
| `data_dir` | `"./data/CloversConsole"` | 上传文件、公开群组和令牌配置的存放目录 |
| `adapters` | `[]` | 额外适配器的 Python 模块名列表 |
| `adapter_dirs` | `[]` | 扫描额外适配器的本地目录列表 |
| `plugins` | `[]` | 插件的 Python 模块名列表 |
| `plugin_dirs` | `[]` | 扫描插件的本地目录列表 |

`adapters` / `plugins` 中的模块必须已经安装，或可以从当前 Python 导入路径找到。例如 `plugins = ["plugins.hello"]` 可以加载上文的单个插件。目录配置则扫描目录下不以 `_` 开头的 Python 文件和子目录；本地目录应位于当前工作目录下，并且模块可以正常导入。

客户端先加载内置 console 适配器，再加载额外适配器，最后加载插件。需要扩展能力的插件应在对应适配器加载之后再加载。

`LOG_LEVEL` 控制终端日志；文件处理器的等级为 `INFO`，同时仍受日志记录器总等级限制。默认文件日志按 10 MiB 轮转，保留 10 个备份。

### 2.2 配置不会自动保存

最小启动脚本会读取配置并在内存中补齐默认值，**不会自动生成或保存 `clovers.toml`**。可以手动创建该文件，也可以在启动脚本中显式保存：

```python
import asyncio

from clovers.config import Config as CloversConfig
from clovers_client.console import Client

client = Client()
CloversConfig.environ().save()
asyncio.run(client.run())
```

`save()` 会把当前内存配置写入文件，包括已同步的默认值。

需要更换配置文件路径时，在启动 Python 前设置环境变量 `CLOVERS_CONFIG_FILE`。例如 PowerShell：

```powershell
$env:CLOVERS_CONFIG_FILE = "console.toml"
python bot.py
```

配置在导入和初始化阶段读取。修改文件后重启进程生效；公开群组和令牌另有专门的重载方法。

### 2.3 直接传入配置对象

也可以不依赖 `[clovers]`，显式传入 console 的配置对象：

```python
import asyncio

from clovers_client.console import Client
from clovers_client.console.config import Config

config = Config(
    BOT_NICKNAME="小四叶",
    host="127.0.0.1",
    port=12000,
    plugin_dirs=["plugins"],
)

asyncio.run(Client(config).run())
```

显式构造的 `Config(...)` 使用模型默认值和传入值，不会自动合并 TOML 的 `[clovers]` 配置，也不会自动保存到文件。

项目还有一个可供扩展使用的 `clovers_client.Config` 基类，它继承 Pydantic `BaseModel`。`YourConfig.sync_config("配置段名")` 会读取该配置段、校验字段并把默认值同步到内存配置，返回 `YourConfig` 实例；要落盘仍需调用 `CloversConfig.environ().save()`。

## 3. 事件属性

```python
from clovers_client import Event
```

这里的 `Event` 是给插件做类型标注的协议；实际事件由 Clovers 核心创建并传给响应器，无需自行实例化。

### 3.1 基础属性

| 属性 | 类型 | 说明 |
| --- | --- | --- |
| `message` | `str` | 用于匹配指令的文本；console 可能已移除开头的机器人昵称 |
| `args` | `Sequence[str]` | 指令匹配得到的参数；上文正则示例中的捕获组通过它读取 |
| `properties` | `dict` | 已经由适配器求值的扩展属性 |

基础属性不需要额外声明。读取下面的扩展属性前，需要在 `plugin.handle()` 的 `properties` 参数中声明：

```python
@plugin.handle(r"^我是谁$", properties=["nickname", "group_id", "permission"])
async def whoami(event: Event):
    place = "私聊" if event.group_id is None else f"群组 {event.group_id}"
    return Result("text", f"{event.nickname}，当前位于{place}，权限等级为 {event.permission}。")
```

核心会在执行响应器前调用适配器方法，并把结果写入 `event.properties`，此后可以用 `event.nickname` 这样的属性方式读取。类型标注本身不会加载属性。若忘记声明，访问尚未加载的属性可能触发 `AttributeError`；若声明了当前适配器没有实现的属性，启动时会记录警告并跳过该响应器。

### 3.2 clovers-client 约定的属性

| 属性 | 类型 | 含义及 console 行为 |
| --- | --- | --- |
| `to_me` | `bool` | 是否指向机器人；console 根据 @ 列表和消息开头的机器人昵称判断 |
| `at` | `list[str]` | 消息中的 @ 目标列表；console 中机器人目标使用机器人昵称 |
| `image_list` | `list[str]` | 图片地址；console 会把能读取的本地 `/download/` 图片转换为 data URL，并过滤读取不到的本地图片 |
| `user_id` | `str` | 发送者 ID，对应 console 的 `senderId` |
| `nickname` | `str` | 发送者昵称，对应 `senderName` |
| `avatar` | `str` | 发送者头像地址 |
| `group_id` | `str \| None` | 群组 ID；console 的 `"private"` 转换为 `None` |
| `group_avatar` | `str \| None` | 群头像；console 当前直接返回消息中的字符串，也可能是空字符串 |
| `bot_nickname` | `str` | 客户端配置的机器人昵称 |
| `permission` | `Literal[0, 1, 2, 3]` | 权限等级，映射见下表 |
| `flat_context` | `list[FlatContextUnit] \| None` | 扁平化上下文；内置 console 适配器尚未实现 |

| 等级 | 约定 | console 对应值 |
| --- | --- | --- |
| `0` | 普通用户，无管理权限 | `Member` |
| `1` | 管理员 | `Admin` |
| `2` | 群主 | `Owner` |
| `3` | 超级管理员 | `SuperUser`，需要有效令牌 |

console 会校验 `SuperUser` 的令牌，校验失败时降为 `Member`；`Admin` 和 `Owner` 当前直接取自收到的消息字段。插件编写者应按这个实际行为使用权限值。

若只希望指向机器人的消息触发响应，可以声明 `to_me` 并添加规则：

```python
@plugin.handle(r"^帮助$", ["to_me"], rule=lambda event: event.to_me)
async def help_message(event: Event):
    return Result("text", "发送 ping 测试连接。")
```

在 console 中可以 @ 机器人后发送 `帮助`，也可以发送 `Bot酱帮助`。昵称前缀去除后不会额外去除空格，因此这个精确匹配示例中昵称与指令之间不加空格。普通私聊本身不会自动使 `to_me` 为 `True`。

### 3.3 相关数据结构

下面的类型可从 `clovers_client.event` 导入：

| 类型 | 字段 |
| --- | --- |
| `FlatContextUnit` | `nickname: str`、`user_id: str`、`text: str`、`images: list[str]` |
| `MemberInfo` | `user_id: str`、`group_id: str`、`nickname: str`、`card: str`、`avatar: str`、`last_sent_time: int` |

这些是 `TypedDict` 数据结构，运行时使用普通字典。是否能取得上下文或成员信息，取决于适配器是否实现相关能力。

## 4. 发送消息与返回结果

### 4.1 两种发送方式

响应器可以返回一个结果，由框架发送：

```python
@plugin.handle(r"^返回消息$")
async def reply(event: Event):
    return Result("text", "这是一条回复。")
```

也可以在响应器执行期间主动发送：

```python
@plugin.handle(r"^主动发送$")
async def send_now(event: Event):
    await event.send("text", "开始处理。")
    return Result("text", "处理完成。")
```

`Result(key, data)` 从 `clovers` 导入。`key` 选择适配器发送方法，`data` 是该方法的数据。

底层 `event.send(key, message)` 对未实现的方法会返回 `None`。如果调用的是可选扩展能力，应先检查，再等待：

```python
pending = event.send("console", ["notice", "info", "提示", "处理完成"])
if pending is not None:
    await pending
```

直接返回 `Result` 时，响应器的结果分发会查找对应发送方法，所以应确认适配器支持这个 `key`。

### 4.2 发送方法

| `key` | `data` 类型 | 含义与 console 支持情况 |
| --- | --- | --- |
| `"at"` | `str` | @ 指定目标 |
| `"text"` | `str` | 文本消息 |
| `"image"` | `FileLike` | 图片消息 |
| `"list"` | `Sequence[SingleResult]` | 合并 @、文本和图片为一条消息 |
| `"voice"` | `FileLike` | console 按文件下载链接发送 |
| `"video"` | `FileLike` | console 按文件下载链接发送 |
| `"file"` | `FileLike` | 文件下载链接 |
| `"console"` | `list[str]` | console 系统消息 |
| `"segmented"` | `AsyncGenerator[OverallResult, None]` | 按异步生成器顺序分段发送 |
| `"private_message"` | `PrivateMessage` | 指定私聊目标；console 只允许给本次事件发送者发送 |
| `"group_message"` | `GroupMessage` | 指定目标群组 |
| `"merge_forward"` | `Sequence[SingleResult \| SequenceResult]` | 合并转发约定；内置 console 适配器尚未实现 |

`FileLike` 定义为 `str | bytes | BytesIO | Path`，可从 `clovers_client.result` 或 `clovers_client.utils` 导入。不同消息类型对字符串的解释不同：

- 图片中的字符串直接作为图片地址；读取本地图片请传 `Path("图片.png")`、`bytes` 或 `BytesIO`。
- 文件中的 `http` 开头字符串作为远程链接，其余字符串作为本地文件路径；也支持 `Path`、`bytes` 和 `BytesIO`。
- console 发送本地文件时会写入 `data_dir/stores_dir/file/`。当前实现不会自动创建其中的 `file` 子目录，首次发送本地文件、语音或视频前，需要自行创建它。

### 4.3 组合消息与分段发送

组合消息使用 `"list"`：

```python
@plugin.handle(r"^组合消息$", ["user_id"])
async def mixed(event: Event):
    return Result(
        "list",
        [
            Result("at", event.user_id),
            Result("text", "第一行"),
            Result("text", "第二行"),
        ],
    )
```

console 将文本用换行连接，把 @ 和图片分别收集到对应数组中；它不会保留各类片段在列表中的交错位置。`"list"` 的元素只支持 `"at"`、`"text"` 和 `"image"`。

分段发送使用异步生成器：

```python
import asyncio


@plugin.handle(r"^分段消息$")
async def segmented(event: Event):
    async def messages():
        yield Result("text", "第一段")
        await asyncio.sleep(1)
        yield Result("text", "第二段")

    return Result("segmented", messages())
```

console 当前的分段分发支持 `"at"`、`"text"`、`"image"`、`"list"`、`"file"`、`"console"`，以及继续分发 `"segmented"`。虽然 `OverallResult` 类型也包含语音和视频，但此处的内部转发函数没有处理 `"voice"` 和 `"video"`；需要在分段、私聊或群组转发中发送时，请使用 `"file"`。

### 4.4 指定私聊或群组

```python
@plugin.handle(r"^私聊回复$", ["user_id"])
async def private_reply(event: Event):
    return Result(
        "private_message",
        {
            "user_id": event.user_id,
            "data": Result("text", "这条消息只发送到当前连接的私聊。"),
        },
    )


@plugin.handle(r"^发到大厅$")
async def group_reply(event: Event):
    return Result(
        "group_message",
        {
            "group_id": "lobby",
            "data": Result("text", "大厅你好！"),
        },
    )
```

`PrivateMessage` 包含 `user_id` 和 `data`，`GroupMessage` 包含 `group_id` 和 `data`；两者的 `data` 类型都是 `OverallResult | SegmentedResult`。

console 的私聊目标只能是当前事件发送者，其他用户 ID 会触发 `ValueError`。群组目标如果在 `public_groups` 中，消息会广播到全部 WebSocket 连接；否则仅发送到触发事件的连接。console 不会通过一个用户 ID 查找并向任意其他在线用户投递私聊。

### 4.5 结果类型别名

以下别名用于类型标注，实际结果仍通过 `clovers.Result(key, data)` 构造：

| 从 `clovers_client` 导出的类型 | 包含的结果 |
| --- | --- |
| `SingleResult` | `"at"`、`"text"`、`"image"` |
| `SequenceResult` | `"list"` |
| `OverallResult` | `SingleResult`、`SequenceResult`、`"file"`、`"voice"`、`"video"`、`"console"` |
| `SegmentedResult` | `"segmented"` |
| `PrivateResult` | `"private_message"` |
| `GroupResult` | `"group_message"` |
| `MergeForwardResult` | `"merge_forward"` |

`SequenceMessage`、`SegmentedMessage`、`PrivateMessage`、`GroupMessage`、`MergeForwardMessage` 等数据类型可以从 `clovers_client.result` 导入。

## 5. 调用适配器能力

`event.call(key, *args)` 用于调用适配器方法。当前 Clovers 运行时接收位置参数；不要向它传递业务关键字参数。

`clovers_client.Event` 约定了以下调用：

| 调用 | 等待后的结果 | 内置 console |
| --- | --- | --- |
| `event.call("flat_context")` | `list[FlatContextUnit]` | 未实现 |
| `event.call("group_member_info", group_id, user_id)` | `MemberInfo` | 未实现 |
| `event.call("group_member_list", group_id)` | `list[MemberInfo]` | 未实现 |

方法不存在时，`call()` 返回 `None`，不能直接 `await None`。例如，在一个已声明 `group_id` 的响应器中：

```python
@plugin.handle(r"^群成员数$", ["group_id"])
async def member_count(event: Event):
    if event.group_id is None:
        return Result("text", "请在群组中使用。")

    pending = event.call("group_member_list", event.group_id)
    if pending is None:
        return Result("text", "当前适配器未提供群成员查询。")

    members = await pending
    return Result("text", f"共有 {len(members)} 位成员。")
```

属性方法和调用方法共用适配器的调用注册表，所以也可以按需查询已经实现的属性，例如 `await event.call("nickname")`。这种调用直接返回计算结果，不会自动把结果写入 `event.properties`；后续若要通过 `event.nickname` 读取，仍应声明属性。

## 6. 扩展适配器

适配器由 `clovers.Adapter` 定义。通过 `property_method()`、`call_method()` 和 `send_method()` 注册新能力，console 客户端会把额外适配器的方法合并到自己的适配器中。

下面给出一个可以直接加入前文工程的扩展示例。

### 6.1 编写扩展模块

在 `bot.py` 同级新建 `console_extra.py`：

```python
from clovers import Adapter
from clovers_client.console import Client

ADAPTER = Adapter("console-extra")


@ADAPTER.property_method("platform")
async def platform() -> str:
    return "console"


@ADAPTER.call_method("group_name")
async def group_name(group_id: str, /, client: Client) -> str:
    group = client.public_groups.get(group_id)
    return group["groupName"] if group else group_id


@ADAPTER.send_method("notice")
async def notice(message: str, send):
    await send(
        {
            "type": "system",
            "data": ["notice", "info", "扩展适配器", message],
        }
    )
```

console 调度事件时提供四项上下文，适配器方法按参数名声明需要的项：

| 参数名 | 内容 |
| --- | --- |
| `recv` | 解析后的 `MessageEvent` 原始消息字典 |
| `send` | 当前事件的发送函数，已经选择广播或单播 |
| `ws` | 当前 FastAPI `WebSocket` 连接 |
| `client` | 当前 console 客户端 |

调用方法的业务参数放在 `/` 前面，使用位置参数传入；例如上面的 `group_id`。发送方法的第一个参数接收 `event.send()` 的消息数据。方法返回协程，属性方法通过协程返回属性值。

### 6.2 配置并使用扩展

修改现有 `clovers.toml` 的同一个 `[clovers]` 配置段，不要重复创建段或字段：

```toml
[clovers]
adapters = ["console_extra"]
plugin_dirs = ["plugins"]
```

在 `plugins/extra_demo.py` 中添加：

```python
from clovers import Event, Plugin, Result

plugin = Plugin()


@plugin.handle(r"^扩展测试$", ["platform", "group_id"])
async def extra_demo(event: Event):
    platform = event.properties["platform"]
    group_id = event.properties["group_id"]
    group_name = "私聊"
    if group_id is not None:
        pending = event.call("group_name", group_id)
        if pending is not None:
            group_name = await pending

    pending = event.send("notice", f"当前平台：{platform}")
    if pending is not None:
        await pending

    return Result("text", f"当前会话：{group_name}")
```

重启服务器后，发送 `扩展测试` 即可调用新增属性、调用方法和发送方法。这里用 Clovers 的基础 `Event` 标注并通过 `properties` 读取自定义字段；扩展也可以自行编写更具体的事件类型协议。

适配器模块需要暴露 `ADAPTER`、`adapter` 或 `__adapter__` 中的一个 `Adapter` 实例。也可以使用 `adapter_dirs` 扫描本地适配器目录，或在运行前执行：

```python
client.load_adapter(["console_extra"])
client.load_plugin(["plugins.extra_demo"])
```

内置方法先注册。同名方法再次注册时会记录警告并忽略，不会覆盖已有实现；扩展时应使用新名称。这里的上下文参数属于 console，接入其他平台时需要根据该平台客户端提供的上下文实现方法。

## 7. console 服务配置与管理

### 7.1 数据目录与公开群组

默认数据目录结构如下：

```text
data/CloversConsole/
├── auth_tokens.json
├── public_groups_config.json
└── stores_dir/
```

`stores_dir` 存放上传内容，默认头像地址对应其中的 `bot_avatar.png`，需要使用者自行提供该文件或修改 `BOT_AVATAR_URL`。

首次初始化会生成 `public_groups_config.json` 的空群组占位内容。可以改为：

```json
[
  {
    "groupId": "lobby",
    "groupName": "大厅",
    "groupAvatar": ""
  }
]
```

群组 ID 为空的条目不会进入公开群组映射。修改后重启服务器，或调用 `reload_public_groups`。

发往公开群组的原始消息和机器人回复会广播到所有连接，并进入内存消息历史。其他群组的消息只发回当前连接，不进入该广播历史。历史使用有长度限制的队列，服务器重启后不会保留。

### 7.2 超级管理员令牌

`auth_tokens.json` 是令牌字符串数组，首次生成时为 `[]`：

```json
[
  "replace-with-your-own-random-token"
]
```

请换成自己生成的随机令牌。修改后重启，或通过已有有效令牌调用 `reload_auth_tokens`。第一次设置令牌时直接重启即可。

令牌有两个用途：

- WebSocket 消息携带 `permission: "SuperUser"` 时，通过 `authToken` 字段提交令牌。
- 请求管理接口 `/action` 时，通过 `Authorization: Bearer <token>` 请求头提交令牌。

管理接口的四个动作如下：

| `action` | 行为 | `args` |
| --- | --- | --- |
| `reload_public_groups` | 重新读取公开群组文件 | 不需要 |
| `reload_auth_tokens` | 重新读取令牌文件 | 不需要 |
| `broadcast` | 向所有连接发送系统消息 | JSON 编码的字符串数组 |
| `shutdown` | 请求服务器关闭并关闭 WebSocket 连接 | 可选的关闭原因 |

例如，在另一个 PowerShell 窗口中重载公开群组：

```powershell
$headers = @{ Authorization = "Bearer replace-with-your-own-random-token" }
Invoke-RestMethod -Uri "http://127.0.0.1:11000/action?action=reload_public_groups" -Headers $headers
```

关闭服务器：

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:11000/action?action=shutdown" -Headers $headers
```

重载公开群组会更新服务器内存中的配置，不会主动向已经连接的网页推送新的群组列表；需要时重新连接，或通过系统广播发送更新。

### 7.3 HTTP / WebSocket 接口

| 地址 | 用途 |
| --- | --- |
| `GET /` | console 网页静态资源 |
| `WS /ws` | 接收聊天消息、系统通知和机器人回复 |
| `GET /action` | 管理动作，要求 Bearer 令牌 |
| `POST /upload` | 上传文件，multipart 表单字段为 `file`；要求文件有 Content-Type，大小上限为 10 MiB，返回下载路径文本 |
| `GET /download/{name}` | 下载 `stores_dir` 内的文件；加 `?check=true` 可检查是否存在 |
| `GET /message/{message_id}` | 读取一条广播历史消息；不存在时返回 404 |
| `GET /message_history/{message_id}` | 返回给定消息之后的广播记录，按从旧到新排列；结果的每一项仍是 JSON 字符串 |

历史查询遇到指定 ID 即停止收集；如果队列中没有该 ID，会返回队列里全部现存消息。历史并非按群组单独存储。

当前只有 `/action` 使用 Bearer 令牌校验；WebSocket 连接、上传、下载和历史查询没有统一的登录校验。将 `host` 改为 `0.0.0.0` 供其他设备使用时，应按实际访问需求配置外层访问控制。

### 7.4 不依赖网页的连接验证

如果需要检查服务器和插件是否正常，可以在保持 `bot.py` 运行的同时，新建 `check_console.py`：

```python
import asyncio
import json

from websockets.asyncio.client import connect


async def main():
    async with connect("ws://127.0.0.1:11000/ws") as ws:
        await ws.send(
            json.dumps(
                {
                    "type": "user",
                    "text": "ping",
                    "images": [],
                    "at": [],
                    "senderId": "demo-user",
                    "senderName": "测试用户",
                    "avatar": "",
                    "permission": "Member",
                    "groupId": "private",
                    "groupName": "",
                    "groupAvatar": "",
                    "echo": "ping-check",
                }
            )
        )
        async with asyncio.timeout(10):
            while True:
                data = json.loads(await ws.recv())
                if data.get("echo") == "ping-check" and data.get("text") == "pong":
                    print("收到机器人回复：", data["text"])
                    return


asyncio.run(main())
```

在另一个终端执行 `python check_console.py`，应输出 `收到机器人回复： pong`。连接后会先收到系统通知，发送的原始消息也会回传，因此示例按 `echo` 和回复文本筛选消息。

这个测试需要加载第 1 节的 `ping` 插件。它只验证 Python 服务和插件通信，不涉及网页的实现。

## 8. 常用客户端属性和方法

使用者可以保留 `client = Client()` 实例，用于自定义启动程序或在适配器中访问服务器状态：

| 属性或方法 | 说明 |
| --- | --- |
| `BOT_NICKNAME`、`BOT_AVATAR_URL` | 机器人名称和头像 |
| `host`、`port` | 服务监听地址与端口 |
| `data_dir`、`stores_dir` | 已解析的数据路径和上传存储路径，均为 `Path` |
| `public_groups` | 以群组 ID 为键的公开群组映射 |
| `auth_tokens` | 已加载的有效令牌集合 |
| `ws_connects` | 当前连接集合 |
| `messages` | 有长度限制的广播消息队列，元素为 `(message_id, JSON字符串)`，最新消息在前 |
| `adapter`、`plugins` | 从 Clovers 核心继承的适配器和插件加载器 |
| `is_ready` | Clovers 核心是否已启动 |
| `load_adapter(adapter_list, adapter_dirs)` | 加载额外适配器，应在加载依赖它的插件之前调用 |
| `load_plugin(plugin_list, plugin_dirs)` | 加载插件，正常用法是在 `run()` 之前调用 |
| `reload_public_groups()` | 同步重新读取公开群组文件 |
| `reload_auth_tokens()` | 同步重新读取令牌文件 |
| `await console_broadcast(data)` | 向所有连接发送 `list[str]` 系统消息，不写入消息历史 |
| `await run()` | 启动插件生命周期与 HTTP / WebSocket 服务，等待服务结束 |

`startup()` / `shutdown()` 是继承自 Clovers 的核心生命周期方法。正常运行 console 时由 `run()` 管理，无需在 `run()` 前手动调用 `startup()`；单独调用核心的 `shutdown()` 也不等于关闭 Web 服务。

## 9. 常见问题

- **导入时报缺少 FastAPI、uvicorn 等模块**：确认在启动脚本所用的同一 Python 环境中安装了 `clovers-client[console]`。
- **没有生成 `clovers.toml`**：这是默认行为；手动创建文件，或使用第 2 节的显式保存代码。
- **能发消息但没有机器人回复**：确认加载了插件、终端没有插件导入警告，并从包含配置和插件目录的工作目录启动。测试 `ping` 时不要添加空格或其他文字。
- **访问事件属性时报错，或日志提示缺少 required methods**：检查响应器是否声明了需要的属性，以及当前适配器是否实现它。内置 console 没有 `flat_context` 和群成员查询。
- **发送本地文件失败**：确认源文件存在，并已创建所配置数据目录下的 `stores_dir/file` 子目录。
- **启动时提示 `console/page` 目录不存在**：`run()` 会挂载 Python 包内的 `clovers_client/console/page` 静态资源。源码或安装产物必须包含配套的已构建网页资源；只安装 Python 依赖不会替你构建网页。本文不涉及网页工程的实现。
- **其他设备打不开页面**：默认只监听本机；需要调整 `host`，使用服务器的实际地址和配置端口访问，并确认系统允许该端口连接。
- **端口已被占用**：修改 `[clovers]` 的 `port` 或显式配置对象中的端口，并同步调整访问地址。
