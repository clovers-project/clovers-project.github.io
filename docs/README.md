# 概述

_✨ 高度自定义的聊天平台 Python 异步机器人指令-响应插件框架 ✨_

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/clovers.svg)](https://pypi.python.org/pypi/clovers)
[![pypi download](https://img.shields.io/pypi/dm/clovers)](https://pypi.python.org/pypi/clovers)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Github](https://img.shields.io/badge/GitHub-Clovers-00CC33?logo=github)](https://github.com/clovers-project/clovers)
[![LICENSE](https://img.shields.io/github/license/clovers-project/clovers.svg)](https://github.com/clovers-project/clovers)

- 本项目遵循着高度自定义的理念。因此本文所有的范例并不作为任何标准。希望你可以随心所欲的遵循自己的风格。
- 本项目可以[独立运行](https://github.com/clovers-project/clovers-client)，也可以寄生在其他框架中，比如 [NoneBot2](https://nonebot.dev/)
- 如果你有更好的想法，[欢迎提 issue 或 pr。](https://github.com/clovers-project/clovers)
- **注意事项：确保你的 Python 版本 >= 3.12**

# 其他的介绍

- 欢迎使用 [clovers-client](./clovers-client) 快速创建一个 Clovers 机器人。
- 在响应器中使用到的额外参数都需要在注册响应器时声明
- 除了指令字符串，其他所有事件信息都是额外参数，需要自定义获取方法。
- 项目的主题色是 <span style="color:#FFFFFF;background-color:#00CC33;">#00CC33</span> 🍀

# 快速开始

## 安装 Clovers CLI

## 创建一个 Clovers 机器人项目

_在使用前需要安装 Clovers CLI 安装方法见[此处](/clovers-cli.md)_

```bash
clovers create <项目名称>
cd <项目名称>
clovers plugin add <插件名>
clovers run
```

下面是一个示例：创建一个使用 `onebot` 协议的 `clovers` 项目

<script>
  const link = document.createElement("link");
  link.rel = "stylesheet";
  link.type = "text/css";
  link.href = "asserts/asciinema-player.css";
  document.head.appendChild(link);
  const script = document.createElement("script");
  script.src = "asserts/asciinema-player.min.js";
  document.body.appendChild(script);
  asciinema_config = {
    cols: 128,
    rows: 24,
    theme: "nord",
  };
  script.onload = () => {
    window.AsciinemaPlayer.create(
      "/casts/create.cast",
      document.getElementById("create"),
      asciinema_config
    );
  };
</script>

<div id="create" style="width: 50vw"></div>

_示例中提示报错是由于未连接到协议服务端。如果在 `ws://127.0.0.1:3001` 存在协议端(如 [LLOneBot](https://github.com/LLOneBot/LLOneBot))即可正常使用。_

# 使用 NoneBot2 框架

在 NoneBot 项目路径下执行以下命令安装 `nonebot_plugin_clovers` 插件。

```bash
nb plugin install nonebot-plugin-clovers
```

随后在 NoneBot 项目的 `.env` `.env.dev` `.env.prod` 之一添加以下配置项

```dotenv
# 协议端是否在本地运行，如协议端不在本地，那么机器人发送的 file 类型资源会转换成 base64 资源
CLOVERS__IS_LOCAL=true
# 使用的适配器， ~代表内置适配器
CLOVERS__USING_ADAPTERS=["~uninfo"]
# clovers 的优先级
CLOVERS__PRIORITY=100
# 加载的 plugins 插件
CLOVERS__PLUGINS=["clovers-aichat", "clovers-divine"]
# 加载的 plugins 本地插件位置
CLOVERS__PLUGIN_DIRS=["./src/clovers/plugins"]
```

_示例中 NoneBot Clovers Client 的[配置项](/nonebot-plugin-clovers?id=配置插件) 使用了 `nonebot_plugin_clovers.adapters.uninfo`_

在 NoneBot 项目根目录创建 `clovers.toml` 文件，并填写以下内容

```toml
# clovers.toml
[clovers]
plugins = ["clovers-aichat", "clovers-divine"]
plugin_dirs = ["./src/clovers/plugins"]
```

- 安装 `nonebot_plugin_clovers` 插件的 NoneBot 项目本身可视为一个 Clovers 项目。

- [NoneBot Clovers Client](/nonebot-plugin-clovers.md) 是一个寄生在 NoneBot 框架下 clovers 客户端，包名为 `nonebot_plugin_clovers` 属于 NoneBot 插件。

- NoneBot Clovers Client 会在 NoneBot 项目中运行一个 CloversCore 实例, 通过 NoneBot2 的响应器获取指令使 clovers 实例内插件响应。

# 配置文件

你可以用任何你你喜欢的方式配置你的项目，但 clovers 提供了一个 `Config` 类。

clovers 项目的配置文件为项目根目录下的 `clovers.toml`

在项目的 `clovers.toml` 文件中添加配置（示例）如下：

```toml
[clovers_plugin_demo] # 这里是你的包名
nickname = "小叶子"
```

`Config` 是一个字典的子类，通过调用 `Config.environ()` 获取全局配置实例。

我们建议使用包名当键，你可以用以下方式获取你的配置。

```python
config = Config.environ()
plugin_config = config[__package__]
nickname = plugin_config["nickname"] # 这里会读到你的配置：小叶子
```

上面是一个简单的例子，其实我们更推荐的做法是使用 pydantic 进行类型验证。

```python
from pydantic import BaseModel
from clovers.config import Config as CloversConfig


class Config(BaseModel):
    nickname: str = "bot"

    @classmethod
    def sync_config(cls, config_key: str):
        clovers_config: dict = CloversConfig.environ().setdefault(config_key, {})
        clovers_config.update((__config := cls.model_validate(clovers_config)).model_dump())
        return __config


assert __package__ # 你的项目不会被作为脚本执行，所以这里一定不是 None
config = Config.sync_config(__package__)
nickname = config.nickname
```

你可以保存当前的配置。当然这只有你在代码中修改过配置才有意义。

```python
Config.environ().save()
```

# 编写 Clovers 插件

在任意 Python 导入路径下，只要包含名为 `PLUGIN` 且类型为 `Plugin` 实例的属性，都可作为 Clovers 插件加载。

关于插件的配置，我们推荐使用 `Config` 类（参考[配置文件](#配置文件)章节）

## 开始

| 参数名       | 类型                              | 描述                                   |
| ------------ | --------------------------------- | -------------------------------------- |
| name         | Optional[str]                     | 插件名称                               |
| priority     | int                               | 插件优先级                             |
| block        | bool                              | 如果本插件有响应，是否阻断后续插件触发 |
| build_event  | Optional[Callable[[Event], Any]]  | 构建 event 的方法                      |
| build_result | Optional[Callable[[Any], Result]] | 构建 result 的方法                     |

1. name 插件名称，默认为空，在 startup 后会更新为插件所在导入路径名
2. priority 插件优先级，默认为 0
3. block 默认为 True，但响应任务可单独定义是否阻断后续插件触发
4. build_event 构建 event 的方法。如果你不想在任务函数内使用原始的 event 可以用 build_event 对 event 进行处理。
5. build_result 构建 result 的方法，如果你觉得返回 Result 实例太过繁琐，你可以使用 build_result 方法对任务返回值进行再处理。

PLUGIN 实例有三个装饰器，分别为启动、关闭、指令-响应任务。

```python
from clovers import Plugin

PLUGIN = Plugin("MyPlugin")  # 创建 Plugin 实例

# 启动时的任务
@PLUGIN.startup
def _():
    print(f"{PLUGIN.name} 启动")


# 关闭时的任务
@PLUGIN.shutdown
def _():
    print(f"{PLUGIN.name} 关闭")


# 指令-响应任务
@PLUGIN.handle(["测试"])
async def _(event: Event):
    pass
```

## 启动/关闭任务

- 使用 @PLUGIN.startup 装饰的函数会在 CloversCore 启动时触发执行
- 使用 @PLUGIN.shutdown 装饰的函数会在 CloversCore 关闭时触发执行
- 启动/关闭任务没有参数
- 如果启动/关闭任务是一个异步函数，那么 CloversCore 会等待其执行完毕
- 注意：即使存在多个加载本插件的 CloversCore 实例（如 CloversMuliCore），启动/关闭任务也只会执行一次

## 指令-响应任务

使用 @PLUGIN.handle 装饰的函数会在 CloversCore 收到与插件匹配的指令时触发执行

### 指令-响应任务的参数

除非你定义了插件的 `build_event`，PLUGIN.handle 装饰的函数的参数是一个 `Event` 类型的实例。

**Event 实例属性与方法介绍：**

- 属性
  - `message` 类型为 `str`: 触发响应的信息原文。
  - `args` 类型为`list[str]`: 从原文中解析的指令参数。将会在下面的[指令](#指令-响应任务的指令)章节进行介绍。
  - `properties` 额外属性: event 会有该任务的装饰器 `properties` 参数添加的属性，详见[获取平台参数](#指令-响应任务获取平台参数)。
- 方法
  - `call` 定义为 `def call(key: str, *args) -> Coroutine | None: ...`
    - `event.call` 会调用适配器同名的 call 方法。
    - `key` 参数是适配器 call 方法注册的 `key`。
    - `*args` 是传入适配器的参数，传入适配器的参数只能是位置参数。
    - 如果 `event.call` 返回了 `None` 则表示适配器不存在同名 call 方法。
    - 如果 `event.call` 返回了一个 `Coroutine`，则 `await` 后返回适配器同名 call 方法的返回值。
  - `send` 定义为 `def send(key: str, message: Any) -> Coroutine[Any, Any, None] | None: ...`
    - `event.send` 会调用适配器同名的send方法。
    - `key` 参数是适配器send方法注册的 `key`。当适配器不存在同名send方法时，此方法会返回 `None`。
    - `message` 传入适配器该方法的参数，表示使用适配器send方法发送的消息。
    - 如果 `event.send` 返回 `None`，则表示适配器不存在同名 send 方法。
    - 如果 `event.send` 返回 `Coroutine` 则 `await` 是执行该发送方法，并返回 `None`。

**插件的 build_event 方法：**

build_event 的参数是触发响应的 `Event` 实例。如果你定义了插件的 build_event 方法，任务函数的参数将变为 build_event 的返回值。

下面是一个例子：

```python
from clovers import Plugin, EventType as Event


class MyEvent:
    def __init__(self, event: Event):
        self.event = event

    def args_to_int(self):
        try:
            return int(self.event.args[0])
        except (ValueError, IndexError):
            return 0


PLUGIN = Plugin(build_event=MyEvent)


@PLUGIN.handle(["测试"])
async def _(event: MyEvent):
    print(event.args_to_int()) # 0
```

_理论上 `build_event` 可以返回任何类型的数据_

### 指令-响应任务的返回值

除非你定义了插件的 `build_result`，PLUGIN.handle 装饰的函数应该返回一个 `Result` 实例或 `None`。

返回值意味着使用适配器向平台发送消息。

**Result 实例属性与方法介绍：**

- 属性
  - `key`: 响应需要调用的适配器同名 send 方法
  - `data`: 传入适配器该方法的参数。
- 方法
  - `send`: 定义为 `async def send(event: Event) -> None: ...`
    - `event` 参数是本响应的 `Event` 对象。
    - 如果适配器不存在 `result.key` 的同名 send 方法则会静默失败。

**插件的 build_result 方法**

`build_result` 需要返回一个 `Result` 实例或 `None`，`build_result` 的参数是 PLUGIN.handle 装饰的函数的返回值。

下面是一个例子，会根据类型自动将数据转换成 Result：

```python
from clovers import Plugin


def build_result(result):
    if isinstance(result, str):
        return Result("text", result)
    if isinstance(result, BytesIO):
        return Result("image", result)
    if isinstance(result, AnyTypeYouNeed):
        return Result("any_you_want", result)
    return result


PLUGIN = Plugin(build_result=build_result)


@PLUGIN.handle(["测试"])
async def _(event: Event):
    return "你好"  # 这里 CloversCore 会接收到 Result("text", "你好")
```

### 指令-响应任务的指令

PLUGIN.handle 装饰器的 `command` 参数类型为 `str | Iterable[str] | re.Pattern[str] | None`

1. 当指令为 `str` 时，handle 装饰器会认为这是一个正则字符串，于是注册为正则匹配
2. 当指令为 `Iterable[str]` 时，handle 装饰器会认为这是一个指令列表， 于是注册为 str.startswith 匹配。
3. 当指令为 `re.Pattern[str]` 时，handle 装饰器会认为这是一个正则对象，于是注册为正则匹配
4. 当指令为 `None` 时，handle 装饰器将其注册为全匹配，所有指令都会触发

指令列表匹配触发了响应时，event.args 会是原指令去掉指令部分后的字符串并按照空格分割为列表。

```python
# 触发指令为"你好 世界"时，输出 ["世界"]
# 触发指令为"helloworld with extra args"时，输出 ["world", "with", "extra", "args"]
@PLUGIN.handle(["你好", "hello"])
async def _(event: Event):
    print(event.args)
```

正则匹配触发了响应时，event.args 会是正则匹配的groups。

```python
# 触发指令为"i love you"时，输出 ["i ", " you"] 使用时注意去掉参数里的空格
# 触发指令为"you love me"时, 输出 ["you ", " me"]
# 触发指令为"my love"时, 输出 ["my ", None]
@PLUGIN.handle(r"^(.+)love(.*)")
async def _(event: Event):
    print(event.args)
```

### 指令-响应任务获取平台参数

PLUGIN.handle 装饰器的 `properties` 参数类型为 `Iterable[str]`

event的属性只有 `message` 触发指令的消息 和 `args` 上文所述的从指令中解析出来的参数

当然这些不会是你需要的所有参数。如果你在插件中需要获取一些平台参数，那么需要在注册 plugin.handle 时声明

在 `properties` 中声明的需要的参数会由适配器注入，直接使用未声明的参数会抛出 KeyError

```python
@PLUGIN.handle(["测试A"], properties=["user_id", "group_id"])
async def _(event: Event):
    print(event.user_id)
    print(event.group_id)
    print(event.others)  # KeyError
```

当然你也可以不事先声明，而在函数中直接使用 `event.call` 获取参数

```python
@PLUGIN.handle(["测试B"], properties=["group_id"])
async def _(event: Event):
    coro = event.call("user_id")
    if coro is None:
        return
    user_id = await coro
    ...
```

有些方法必须带参数，无法在定义时声明，这时你需要使用 `event.call`

```python
@PLUGIN.handle(["测试C"], properties=["user_id", "group_id"])
async def _(event: Event):
    coro = event.call("group_member_info", "744751179", "1048827424")
    if coro is None:
        return
    member = await coro
    ...
```

_以 `event.user_id` 为例，其与 `await event.call("user_id")` 都是适配器中名为 `"user_id"` 的 call 方法的返回值_

### 指令-响应任务的规则

PLUGIN.handle 装饰器的 `rule` 参数类型为 `Rule.Ruleable | Rule | None`

我们常用 `Callable[[Event], bool]` 和 `list[Callable[[Event], bool]]` 两种

- rule 是参数为 `event`，返回值为 `bool` 的**同步**函数, 或**此类函数的列表**。
- 当装饰器定义了 rule 参数，那么**除了满足指令匹配**，还要让 rule 函数返回 True 才会触发响应
- 如果是函数列表，则所有函数**全部返回 True** 才会触发响应
- 传给 rule 的参数是 build_event 的返回值
- 如果 rule 需要平台参数，那么必须在 `properties` 中声明。

下面是一个通过 rule 定义为必须 @机器人才能触发的任务

```python
@PLUGIN.handle(
    ["其他功能"],
    properties=["to_me"],
    rule=lambda e: e.to_me,
    priority=10,
    block=False,
)
async def _(event: Event):
    pass
```

### 指令-响应任务的优先级

在多插件环境下，一个指令可能会同时命中多个插件中的多个任务（Handle）。为了精确控制它们的执行顺序，我们需要通过优先级机制进行调度。

Plugin 类构造函数的 `priority` 参数类型为 `int`，定义了插件优先级 (pPri)。

PLUGIN.handle 装饰器的 `priority` 参数类型为 `int`，定义了任务优先级 (hPri)。

**规则**

- 如果一个指令匹配到多个任务，首先比较插件优先级 (pPri)，越小的越先执行。
- 如果任务的优先级相同，则比较任务优先级 (hPri)，越小的越先执行。
- 如果任务的pPri与hPri都相同，则会并发执行。

### 指令-响应任务的阻断

如果一个指令同时命中了多个任务，为了精确控制任务执行完成后，后续任务是否继续执行，我们需要通过阻断机制进行控制。

Plugin 类构造函数的 `block` 参数类型为 `bool`，定义了插件级阻断 (pBlk)。

PLUGIN.handle 装饰器的 `block` 参数类型为 `bool | tuple[bool, bool]`

- `block` 为 `bool` 时定义该任务的任务级阻断 (pBlk)
- `block` 为 `tuple[bool, bool]` 时表示该任务不使用本插件的阻断定义，独自定义该任务的插件级阻断 (pBlk)与任务级阻断 (pBlk)。

**规则**

| 插件阻断 (pBlk) | 任务阻断 (hBlk) | 阻断结果                                                                           |
| --------------- | --------------- | ---------------------------------------------------------------------------------- |
| True            | True            | 后续任务都被阻断。                                                                 |
| True            | False           | **本插件优先级内**的后续任务会**继续触发**，但**后续插件优先级**的任务会**被阻断** |
| False           | True            | **本插件优先级内**的后续任务会**被阻断**，但**后续插件优先级**的任务会**继续触发** |
| False           | False           | 后续任务都继续执行。                                                               |

_当并发执行的任务存在不同的阻断规则时，合并的阻断规则为按位取或。_

指令-响应任务函数的返回值代表指令触发的响应。
可以是任意类型, 这个返回值会发送给 build_result 方法构建成 Result 实例。

如果你的插件的 build_result is None 那你就必须返回一个 Result 实例。

就像你的 build_event is None, 你的参数会是原始的 Event 实例那样。

关于 Result 类的详细介绍可以参考[文档](/document)

接下来的示例是指令为 "测试" 回应 "你好" 的 插件指令-响应任务

```python
@PLUGIN.handle(["测试"])
async def _(event: Event):
    return Result("text", "你好")
```

适配器方法会根据你需要的参数构建 event.properties

有时你可能需要在函数中向平台传递一些参数才能拿到响应，那么这样的话不适用于提前声明

或者也许为了优化，并不是每次进入响应都需要使用某些参数

这样的话，你也可以使用 call 方法

```python
@PLUGIN.handle(["测试"], ["at"])
async def _(event: Event):
    at_user_id = event.properties["at"]
    # print(event.properties["group_id"]) # KeyError
    if condition:
        group_id = await event.call("group_id")
        member = await event.call("group_member_info", group_id, at_user_id)
```

## 临时任务

PLUGIN.temp_handle 装饰器的参数有 `properties` `timeout` `rule` `block` `state`

参数介绍

- `properties`: 与[指令-响应任务获取平台参数](#指令-响应任务获取平台参数)一致
- `timeout`: 类型为 `float | int` 临时任务的有效时间，从注册任务开始算起，单位为秒
- `rule`: 与[指令-响应任务的规则](#指令-响应任务的规则)一致
- `block`: 与[指令-响应任务的阻断](#指令-响应任务的阻断)一致
- `state`: 临时任务 handle 的 `state` 属性，可以是任意类型

_临时任务大部分行为都与普通任务一致，这里不过多赘述，仅介绍不同点。_

**临时任务的响应**

使用 @PLUGIN.temp_handle 装饰的函数匹配规则为 `None`，这意味着它会在收到任何指令时触发执行。

**临时任务的优先级**

临时任务只有插件优先级 (pPri)，在本 pPri 内，临时任务是先于普通任务执行的。

**临时任务的参数**

与普通任务不同，临时任务装饰的函数有两个参数: `event`, `handle`

`event` 与普通任务一致：为一个 `Event` 对象或 `build_event` 的返回值

`handle` 为一个 `TempHandle` 对象。`TempHandle`包含以下属性或方法：

- `state`: 临时任务 handle 的 `state` 属性，可以是任意类型，可随时注入或修改，用于记录当前任务的状态。
- `delay`: 定义为 `def delay(timeout: float | int):` 用于推迟临时任务的销毁时间。
- `finish`: 定义为 `def finish():` 立即销毁此临时任务。

**临时任务的注册**

这是与普通任务最大的不同，普通指令-响应任务在运行时创建会触发 RuntimeError，而临时任务被设计为在运行时创建。

下面是一个例子：

```python
@PLUGIN.handle(["响应测试"], ["user_id", "group_id"])
async def _(event: Event):
    user_id = event.user_id
    group_id = event.group_id
    code = "".join([random.choice("0123456789") for _ in range(4)])

    @PLUGIN.temp_handle(["nickname", "user_id", "group_id"], rule=lambda e: e.user_id == user_id and e.group_id == group_id)
    async def _(event: Event, handle: TempHandle):
        handle.finish()
        if event.message == code:
            return Result("text", "验证码验证成功")
        return Result("text", "验证码验证失败")

    return Result("text", f"请输入验证码：{code}")
```

## 插件间的依赖

当插件依赖其他 clovers 插件时，你除了需要 import 你需要的对象外，你还需要用插件的 require 方法来声明依赖。

```python
PLUGIN.require("clovers-apscheduler")
```

这样你依赖的插件无需声明加载也会正常启动。

**注意：声明依赖只针对 clovers 插件，不要利用 require 方法声明一般 python 模块**

# 编写 Clovers 适配器

**注意: 适配器是针对于特定 CloversCore 类的，而 CloversCore 是一个抽象类。因此在编写适配器时你必须清楚该 CloversCore 实现都给了适配器哪些参数。**

在任意 Python 导入路径下，只要包含名为 `ADAPTER` 且类型为 `Adapter` 实例的属性，都可作为 Clovers 适配器加载。

关于适配器的配置，我们推荐使用 `Config` 类（参考[配置文件](#配置文件)章节）

```python
from clovers import Adapter

ADAPTER = Adapter("MyAdapter")  # 创建 Adapter 实例
```

~~创建好了~~

ADAPTER 实例有三个装饰器，分别为获取参数、发送、调用。

## 获取参数 property_method 方法

在[指令-响应任务获取平台参数](#指令-响应任务获取平台参数)的示例中，我们声明获取了平台的 `user_id`, `group_id` 参数。

当然，这个参数不是凭空而来，它实际上是你编写的适配器方法获得的

所以你需要在适配器方法中定义这个参数的获取方法

下面是 `nonebot_plugin_clovers.adapters.onebot.v11` 中的一个例子

```python
@ADAPTER.property_method("user_id")
async def _(event: MessageEvent) -> str:
    return event.get_user_id()
```

这样，如果 handle 声明了 `properties=["user_id"]` 参数，那么任务接收到的 `event.user_id` 就是 `event.get_user_id()`

诸如此类的方法，都需要在适配器方法中定义

## 发送消息 send_method 方法

在[指令-响应任务的返回值](#指令-响应任务的返回值)的示例中，我们使用了 `key` 为 `text` 的 `Result` 实例。

发送消息也是适配器的工作，但是如果你不定义的话，适配器并不知道该怎么发送 `text` 消息

所以你需要在适配器方法中定义发送这种消息的方法

适配器会向 send 方法传入 `Result` 类实例的 `data` 属性作为第一个参数。

下面是 `nonebot_plugin_clovers.adapters.onebot.v11` 中的一个例子

```python
@ADAPTER.send_method("text")
async def _(message: str, /, bot: Bot, event: MessageEvent):
    await bot.send(event, MessageSegment.text(message))
```

## 获取响应 call_method 方法

在[指令-响应任务获取平台参数](#指令-响应任务获取平台参数)后两个示例中，我们使用 `event.call` 获取了两个平台参数。

其中 `user_id` 是 `property_method` 注册的，它不需要参数。

另一个 `group_member_info` 需要参数，需要用 call_method 注册。

下面是 `clovers_client.onebot.v11` 中的一个例子

```python
@ADAPTER.call_method("group_member_info")
async def _(group_id: str, user_id: str, /, call: OneBotV11API) -> MemberInfo:
    user_info = await call("get_group_member_info", {"group_id": int(group_id), "user_id": int(user_id)}, True)
    return {
        "group_id": group_id,
        "user_id": user_id,
        "avatar": f"https://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640",
        "nickname": user_info["nickname"],
        "card": user_info["card"],
        "last_sent_time": user_info.get("last_sent_time", 0),
    }

```

_注意由于 Clovers 框架的限制 `call_method` 注册的方法只接受位置参数_

_其实 `property_method` 与 `call_method` 只是名字不一样_

# 类型协议

适配器方法会根据插件声明的参数构建参数，处理响应结果。但是同名参数不一定是兼容的

假如：插件声明了需要参数 `user_id` 同时默认此参数是 `int` 类型。适配器声明了参数 `user_id`，但返回值是 `str` 类型。

插件拿到的 `user_id` 实际上是 `str` 类型，但由于适配器存在同名方法不会报错，所以可能会导致非常严重的问题。

为了避免这种情况 clovers 提供了一个类型协议，如果插件设置了类型协议则会进行类型响应过滤。

插件需要包含适配器的全部可能类型才会检查通过。

为了使用类型协议，适配器的代码中需要写完整的类型提示：

**参数类型**

参数类型会标注返回值类型。注意参数类型的纯位置参数个数必须是 0，否则会被识别为调用类型。

```python
@ADAPTER.property_method("user_id")
async def _(event: MessageEvent) -> str: ...
```

这样写会标记 `call["user_id"] = str`

**响应类型**

响应类型会标注第一个纯位置参数的类型，注意必须有纯位置参数分割符，否则不会提取类型协议。

```python
@ADAPTER.send_method("image")
async def _(message: bytes | BytesIO, /, bot: Bot, event: MessageEvent): ...
```

这样写会标记 `send["image"] = bytes | BytesIO`

**调用类型**

调用类型会标注纯位置参数的类型，注意必须有纯位置参数分割符，否则不会提取类型协议。

```python
@ADAPTER.call_method("group_member_info")
async def _(group_id: str, user_id: str, /, call: OneBotV11API) -> MemberInfo: ...
```

这样写会标记 `call["group_member_info"] = Callable[str, str, Coroutine[Any, Any, MemberInfo]]`

而插件需要定义并设置类型协议：

```python
from clovers import EventType
from typing import Protocol


class Event(EventType, Protocol):
    user_id: str

    @overload
    async def send(self, key: Literal["image"], message: bytes | BytesIO): ...

    @overload
    def call(self, key: Literal["group_member_info"], group_id: str, user_id: str) -> Coro[MemberInfo] | None: ...

    def send(self, key: str, message: Any):
        raise NotImplementedError

    def call(self, key: str, *args: Any, **kwargs):
        raise NotImplementedError


PLUGIN.protocol = Event
```

_根据惯用例，作为类型协议的类还会被当做 event 参数的类型标注。_

# 响应处理器

`CloversCore` 是整个框架的消息调度中心，它作为一个抽象基类，作用为与底层平台交互，并为响应器提供所需要的参数。

## 响应处理器的入口

`CloversCore.dispatch` 是 Clovers 框架的入口，在任何实现中，外部驱动都需要以关键字参数的形式为 `dispatch` 传入所有需要的数据。

`CloversCore.dispatch` 返回一个 `Task[int] | None` 如果返回 `None` 则表示 dispatch 被跳过，`await task` 返回的 `int` 表示 dispatch 触发的 `handle` 个数。

这是 `nonebot-plugin-clovers` 中，NoneBot 驱动 Clovers 的入口:

```python
async def handler(bot, event, matcher):
    if (coro := self.dispatch(bot=bot, event=event)) and await coro:
        matcher.stop_propagation()
```

_NoneBot 为 `dispatch` 提供了 `bot` 和 `event` 参数，这意味着 Clovers 适配器可以使用这两个参数实现 NoneBot 绝大部分与协议端的交互。_

这是简化的 `clovers-client.onebot.v11` 中，websockets 驱动 Clovers 的入口:

```python
while self._ready:
    ...
    async for recv_data in ws_connect:
        recv = json.loads(recv_data)
        if not recv.get("post_type") == "message":
            continue
        self.dispatch(call=self.call_api, recv=recv, client=self)
    ...
```

_主循环会为 `dispatch` 提供 `call_api` 的能力与 `ws_connect` 收到的消息体。_

## 消息提取

`CloversCore.extract_message` 是 `CloversCore` 唯一的抽象方法，其参数是 `CloversCore.dispatch` 接收的所有关键字参数。

你需要根据当前适配的平台规则，使用**所有**这些参数并从中提取出一个 `str` 格式的纯文本信息信息用来触发插件匹配，或者返回一个 `None` 来跳过 dispatch。

**再次强调：即使用不到某些参数，`CloversCore.extract_message` 也必须接收所有 `CloversCore.dispatch` 传入的参数。**

## 启动与停止

在进行 `dispatch` 之前，`CloversCore` 必须被启动，而在关闭实例时，`CloversCore` 应该被停止。

_更准确的说，`startup` 包含初始化逻辑，必须被执行。而 `shutdown` 仅做了等待未完成事件与触发插件 `shutdown` 任务。假如 Clovers 是一个 forever loop 那么 `shutdown` 其实并不是很重要。_

启动与关闭的方法有异步上下文与函数调用两种。

1. 异步上下文

   ```python
   clovers: CloversCore = ...

   async with clovers:
       ...
   ```

   一般用于 `CloversCore` 自行管理生命周期的独立客户端场景。

2. 函数调用

   ```python
   clovers: CloversCore = ...

   await clovers.startup()
   ...
   await clovers.shutdown()
   ```

   一般用于 `CloversCore` 被其他框架管理生命周期的寄生场景。

## 多核响应处理器

多核响应处理器 `CloversMultiCore` 是一个非常简单的类，其内部有多个 `CloversCore` 实例，用于多平台场景。

多核响应处理器的实例化参数是多个 `CloversCore` 实例，这些实例会形成一个元组存在在 `CloversMultiCore.cores` 中。

`CloversMultiCore.locate_core` 是其唯一抽象方法，用于根据 `CloversCore.dispatch` 传入的参数，返回针对于这个参数的 `CloversCore` 实例。

归功于这种机制，每次 `CloversMultiCore.dispatch` 只能由一个 `CloversCore` 响应。

# 最小可运行示例

本章是一个最简单的 Clovers 框架实现，包含适配器，插件，响应处理器，类型提示和协议。

```python
# main.py
from clovers import CloversCore
from my_adapter import ADAPTER
from my_plugin import PLUGIN


class MyClovers(CloversCore):
    def extract_message(self, message: str, **ignore):
        return message


async def main():
    clovers = MyClovers("MyClovers")
    clovers.adapter.mixin(ADAPTER)
    clovers.plugins.append(PLUGIN)
    async with clovers:
        while True:
            coro = clovers.dispatch(message=input("请输入消息："), bot_nickname="MyBot")
            if coro:
                await coro


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

这是 `my_adapter.py` 内定义的适配器，用三种装饰器添加了三种方法。

```python
# my_adapter.py
from datetime import datetime
from clovers import Adapter


ADAPTER = Adapter("MyAdapter")


@ADAPTER.send_method("text")
async def _(text: str, /):
    print(text)


@ADAPTER.property_method("bot_nickname")
async def _(bot_nickname: str) -> str:
    return bot_nickname


@ADAPTER.call_method("datetime")
async def _(format: str) -> str:
    return datetime.now().strftime(format)

```

这是 `my_plugin.py` 内定义的插件，包含类型提示和协议。

```python
from clovers import EventType, Plugin, Result
from typing import Protocol, Literal


class Event(EventType, Protocol):
    bot_nickname: str

    async def send(self, key: Literal["text"], data: str): ...

    async def call(self, key: Literal["datetime"], format: str) -> str: ...


PLUGIN = Plugin[Event]("MyPlugin", build_result=lambda data: Result("text", data))
PLUGIN.protocol = Event


@PLUGIN.startup
def _():
    print(f"{PLUGIN.name} 启动")


@PLUGIN.handle(["测试"], ["bot_nickname"])
async def _(event: Event):
    await event.send("text", f"Hello, {event.bot_nickname}")
    return f"现在的时间是：{await event.call("datetime","%Y-%m-%d %H:%M:%S")}"
```

运行结果：

```txt
MyPlugin 启动
请输入消息：测试
Hello, MyBot
现在的时间是：2026-04-12 01:18:28
请输入消息：
```
