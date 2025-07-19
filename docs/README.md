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

- Leaf 负责单个适配器下插件的响应，Client 负责管理插件的启动和运行逻辑。上述类型为基类。
- 如果需要创建只有一个适配器的客户端可以在实现类里面同时继承 (Leaf, Client), 也可以继承 LeafClient。
- 在响应器中使用到的额外参数都需要在注册响应器时声明
- 除了指令字符串，其他所有事件信息都是额外参数，需要自定义获取方法。
- 项目的主题色是 <span style="color:#FFFFFF;background-color:#00CC33;">#00CC33</span> 🍀

# 安装

<details open>
<summary>pip</summary>

```bash
pip install clovers
```

</details>

<details>
<summary>poetry</summary>

```bash
poetry add clovers
```

</details>

# 快速开始

使用 Clovers CLI

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

```bash
clovers create <项目名称>
cd <项目名称>
clovers plugin add <插件名>
clovers run
```

下面是一个示例：创建一个使用 `onebot` 协议的 `clovers` 项目

<div id="create" style="width: 50vw"></div>

_示例中提示报错是由于未连接到协议服务端。如果在 `ws://127.0.0.1:3001` 存在协议端(如 [LLOneBot](https://github.com/LLOneBot/LLOneBot))即可正常使用。_

# 使用 NoneBot2 框架

1. [NoneBot Clovers Client](/nonebot-plugin-clovers.md) 是一个寄生在 NoneBot 框架下 clovers 客户端，包名为 `nonebot_plugin_clovers` 属于 NoneBot 插件。

2. NoneBot Clovers Client 会在 NoneBot 项目中运行一个 CloversClient 实例, 通过 NoneBot2 的响应器获取指令使 clovers 实例内插件响应。

3. 安装 `nonebot_plugin_clovers` 插件的 NoneBot 项目本身可视为一个 Clovers 项目。

下面以 Nonebot2 框架作为宿主, 并且使用 `nonebot.adapters.onebot.v11` 适配器和 `nonebot_plugin_clovers` 插件为例。

_NoneBot Clovers Client 的[配置项](/nonebot-plugin-clovers?id=配置插件) 使用了 `nonebot_plugin_clovers.adapters.onebot.v11` 但是 clovers 的理念是完全的自定义，所以 `nonebot_plugin_clovers` 内部的自带的适配器仅作为一种示范，不作为任何标准，更推荐的是自行[编写适配器](#适配器-adapter)_

## 安装 NoneBot Clovers Client

<details open>

<summary> 使用 nb-cli (推荐) </summary>

在 NoneBot 项目路径下执行以下命令安装 `nonebot_plugin_clovers` 插件。

```bash
nb plugin install nonebot-plugin-clovers
```

</details>

<details>

<summary> 手动安装 </summary>

使用一个你喜欢的包管理器安装 nonebot-plugin-clovers

```bash
pip install nonebot-plugin-clovers
```

打开 NoneBot 项目目录下的 pyproject.toml 文件，添加 nonebot_plugin_clovers 到 plugins

```toml
# pyproject.toml
[tool.nonebot]
...
plugins = ["nonebot_plugin_clovers"]
```

</details>

## 使用 NoneBot 插件加载 clovers 插件

创建一个 NoneBot 项目之后在 `\src\plugins` 新建一个 nb 本地插件（本地插件的位置是你指定的）

例如你创建的项目名为 `connect_to_clovers.py`

```python
from nonebot import require

require("nonebot_plugin_clovers").client.load_plugin("clovers_setu_collection")
# 你还可以继续加载其他插件
```

_这样你就成功加载了 [clovers_setu_collection](https://github.com/clovers-project/clovers-setu-collection) 作为 Nonebot 插件, [nonebot_plugin_setu_collection](https://github.com/KarisAya/nonebot_plugin_setu_collection)_ 就是这样做的

## 使用 CloversClient 配置加载 clovers 插件

<details open>

<summary> 使用 Clovers CLI </summary>

在 NoneBot 项目下执行

```bash
clovers plugin add <插件名>
```

</details>

<details>

<summary> 手动安装 </summary>

使用你喜欢的依赖管理器安装 clovers 插件后，在 nb 项目文件夹下创建 clovers.toml, 填写如下配置

```toml
# clovers.toml
[clovers]
plugins = ["<插件名>"]
```

效果相同

</details>

# 插件 Plugin

编写一个模块，这个模块需要包含一个 `__plugin__` 属性，这个属性是一个 plugin.Plugin 实例

关于 Plugin 类的详细介绍可以参考[文档](/document)

## 开始

```python
from clovers import Plugin

plugin = Plugin()  # 创建 Plugin 实例

__plugin__ = plugin  # 暴露 __plugin__ 属性
```

你可以给插件添加多个任务，当 clovers 运行时，这些任务就会生效。

```python
# 启动时的任务
@plugin.startup
async def _():
    pass


# 关闭时的任务
@plugin.shutdown
async def _():
    pass


# 指令-响应任务
@plugin.handle(["测试"])
async def _(event: Event):
    pass
```

你也可以使用为其他插件的`__plugin__`属性添加响应

```python
from some_plugin import __plugin__ as plugin


# do something
@plugin.handle(["其他测试"])
async def _(event: Event):
    pass
```

## 创建 Plugin 实例的参数

| 参数名       | 类型                              | 描述                                   |
| ------------ | --------------------------------- | -------------------------------------- |
| name         | str                               | 插件名称                               |
| priority     | int                               | 插件优先级                             |
| block        | bool                              | 如果本插件有响应，是否阻断后续插件触发 |
| build_event  | Optional[Callable[[Event], Any]]  | 构建 event 的方法                      |
| build_result | Optional[Callable[[Any], Result]] | 构建 result 的方法                     |

如果你不想在任务函数内使用原始的 event, 你也可以自建 event 类, 然后在创建 plugin 实例时注入 build_event 方法。

```python
from clovers import Plugin, Event as CloversEvent
class Event:
    def __init__(self, event: CloversEvent):
        self.event: CloversEvent = event

    @property
    def raw_command(self):
        return self.event.raw_command

    @property
    def args(self):
        return self.event.args

    @property
    def user_id(self) -> str:
        return self.event.properties["user_id"]

plugin = Plugin(build_event=lambda event: Event(event))

@plugin.handle(["测试"], ["user_id"])
async def _(event: Event):
    print(event.user_id) # "123456"
```

`build_result` result 的构建方法

当然如果你认为返回 Result 实例太过繁琐，你也可以使用 build_result 方法

```python
from clovers import Plugin
def build_result(result):
    if isinstance(result, str):
        return Result("text", result)
    if isinstance(result, BytesIO):
        return Result("image", result)
    if isinstance(result, AnyTypeYouNeed):
        return Result("any_method_you_want", result)
    return result

plugin = Plugin(build_result=build_result)

@plugin.handle(["测试"])
async def _(event: Event):
    return "你好"
```

## 任务和事件参数

`startup` 在插件初始化时执行，无参数。

`shutdown` 在插件关闭时执行，无参数。

`handle` 指令响应任务，由指令触发，获取到事件参数 `event` ， `event`并不是某个特定的类型。而是原始 `Event` 实例发送给 `build_event` 构建的返回值。

由此可见原始 `Event` 类你在指令响应任务的函数中唯一获得的参数，你需要的所有东西都在这里。

关于 Event 类的详细介绍可以参考[文档](/document)

## 指令-响应任务的指令

指令-响应任务的 `commands` 参数可以是字符串，也可以是字符串列表，也可以是一个 re.Pattern 实例

当指令是字符串列表时，handle 装饰器会认为这个指令是一个指令列表，那么它会对字符串进行 startswith 判断。

如果成功触发响应，那么 event.args 会是原指令去掉指令部分后的字符串并按照空格分割为列表。

```python
# 触发指令为"你好 世界"时，输出 ["世界"]
# 触发指令为"helloworld with extra args"时，输出 ["world", "with", "extra", "args"]
@plugin.handle(["你好", "hello"])
async def _(event: Event):
    print(event.args)
```

当指令是字符串时，handle 装饰器会认为这个指令是一个正则字符串，那么它会对指令进行正则匹配。

如果成功触发响应，那么 event.args 会是正则字符串中的 group 列表

```python
# 触发指令为"i love you"时，输出 ["i ", " you"] 使用时注意去掉参数里的空格
# 触发指令为"you love me"时, 输出 ["you ", " me"]
# 触发指令为"make love"时, 输出 ["make ", None]
@plugin.handle(r"^(.+)love(.*)")
async def _(event: Event):
    print(event.args)
```

## 指令-响应任务的响应

指令-响应任务函数的返回值可以是任意类型, 这个返回值会发送给 build_result 方法构建成 Result 实例。

如果你的插件的 build_result is None 那你就必须返回一个 Result 实例。

就像你的 build_event is None, 你的参数会是原始的 Event 实例那样。

关于 Result 类的详细介绍可以参考[文档](/document)

接下来的示例是指令为 "测试" 回应 "你好" 的 插件指令-响应任务

```python
@plugin.handle(["测试"])
async def _(event: Event):
    return Result("text", "你好")
```

## 指令-响应任务获取平台参数

如果你在插件中需要获取一些平台参数，那么需要在注册 plugin.handle 时事先声明需要的参数

```python
@plugin.handle(["测试"], properties=["user_id", "group_id"])
async def _(event: Event):
    print(event.properties["user_id"])
    print(event.properties["group_id"])
    print(event.properties["others"])  # KeyError
```

也可以这样

```python
@plugin.handle(["测试"], properties=["user_id", "group_id"])
async def _(event: Event):
    print(event.user_id)
    print(event.group_id)
    print(event.others)  # KeyError
```

适配器方法会根据你需要的参数构建 event.properties

有时你可能需要在函数中向平台传递一些参数才能拿到响应，那么这样的话不适用于提前声明

或者也许为了优化，并不是每次进入响应都需要使用某些参数

这样的话，你也可以使用 call 方法

```python
@plugin.handle(["测试"], ["at"])
async def _(event: Event):
    at_user_id = event.properties["at"]
    # print(event.properties["group_id"]) # KeyError
    if condition:
        group_id = await event.call("group_id")
        member = await event.call("group_member_info", group_id, at_user_id)
```

## 指令-响应任务的规则

```python
@plugin.handle(
    ["其他功能"],
    properties=["to_me"],
    rule=lambda e: e.to_me,
    priority=10,
    block=False,
)
async def _(event: Event):
    pass
```

- rule 是参数为 event，返回值为 bool 的函数, 或此类函数的列表。
- 如果是函数列表，则所有函数的检查都通过才会触发任务
- 需要注意的是，传给 rule 的参数是 build_event 的返回值，并不是原始的 Event 类实例，除非你的 build_event is None

## 临时任务

```python
from clovers import Event, Plugin, Result, TempHandle

plugin = Plugin("Test", build_result=lambda msg: Result("text", msg))


async def confirm(event: Event, handle: TempHandle):
    handle.finish()
    if event.message == "是":
        return "已确定"
    else:
        return "已取消"


@plugin.handle(["创建任务"], ["user_id", "group_id"])
async def _(event: Event):
    user_id = event.properties["user_id"]
    group_id = event.properties["group_id"]
    plugin.temp_handle(
        ["user_id", "group_id"],
        rule=lambda e: e.properties["user_id"] == user_id and e.properties["group_id"] == group_id,
    )(confirm)
    return "任务已创建，请输入 是 | 否 进行确认"


__plugin__ = plugin
```

临时任务没有优先级，而且是最优先触发。

**注意，一般任务也可以在任务中注册，但是不会生效并且可能导致未定义的行为**

`timeout` 任务超时时间（秒）

temp_handle 会被任意消息触发，请传入规则或在响应函数中内置规则。

temp_handle 任务的参数除了 event，你还会获得一个 handle 参数，它的功能是结束临时任务或延长本任务的超时时间。如果你不结束，在临时任务超时前每次消息都会触发。

## 插件的优先级和阻断

当一个指令可以触发多个任务时，会涉及到响应触发顺序和阻断。

### 优先级 priority

插件有两种优先级，一种是插件优先级 (pPri)，一种是任务优先级 (hPri)。

(pPri) 高的任务先触发，(pPri) 相同，(hPri) 高的先触发。

同一优先级插件的所有同级任务都会同时触发。

### 阻断 block

阻断有两种，一种是插件优先级阻断 (pBlk)，一种是任务优先级阻断 (hBlk)。

下面的例子都是一次指令触发了多个响应的情况。

当 (pBlk) 为 True, (hBlk) 为 True 时：阻断低于当前 (pPri) 和当前 (pPri) 内低于当前 (hPri) 的任务。

当 (pBlk) 为 True, (hBlk) 为 False 时：阻断低于当前 (pPri) 的任务，但会继续触发当前 (pPri) 内低于当前 (hPri) 的任务。

当 (pBlk) 为 False, (hBlk) 为 True 时：阻断当前 (pPri) 内低于 (hPri) 的任务，但会继续触发低于当前 (pPri) 的任务。

当 (pBlk) 为 False, (hBlk) 为 False 时：不阻断

## 插件配置文件

配置文件存放在一个 toml 文件里，文件由你指定

关于配置的详细介绍可以参考[文档](/document)

下面是配置一个例子

clovers.toml

```toml
[clovers_AIchat]
nickname = "小叶子"
timeout = 600
```

插件获取的配置会是一个字典。

为便于插件间的配置互相获取，建议在插件中使用类似下面的代码加载配置

```python
from clovers.config import Config as CloversConfig

config_data: dict = CloversConfig.environ().setdefault(__package__, {})
default_config = {"nickname": "小叶子", "timeout": 600}
config_data.update({k: v for k, v in default_config.items() if k not in config_data})
```

当然，更推荐的做法是使用 pydantic 进行类型验证。

```python
from pydantic import BaseModel
from clovers.config import Config as CloversConfig


class Config(BaseModel):
    ...

    @classmethod
    def sync_config(cls):
        """获取 `CloversConfig.environ()[__package__]` 配置并将默认配置同步到全局配置中。"""
        __config_dict__: dict = CloversConfig.environ().setdefault(__package__, {})
        __config_dict__.update((__config__ := cls.model_validate(__config_dict__)).model_dump())
        return __config__
```

为了更方便的修改配置，你可以保存当前的配置，这样所有配置项都会出现在配置文件里

```python
@plugin.startup
async def _():
    clovers_config.save()
```

# 适配器 Adapter

你需要编写一个模块，这个模块需要包含一个`__adapter__`属性，这个属性是一个 adapter.Adapter 实例

关于 Adapter 类的详细介绍可以参考[文档](/document)

```python
from clovers import Adapter

adapter = Adapter()  # 创建 Adapter 实例

__adapter__ = adapter  # 暴露 __adapter__ 属性
```

~~创建好了~~

一个适配器可以有多个适配器方法

## 获取参数 property_method 方法

在[指令-响应任务获取平台参数](#指令-响应任务获取平台参数)的示例中，我们声明获取了平台的 `user_id`, `group_id` 参数。

当然，这个参数不是凭空而来，它实际上是你编写的适配器方法获得的

所以你需要在适配器方法中定义这个参数的获取方法

property 方法的参数是 clovers 实例响应时传入的，我们可以传入任意参数，请参考 [使用 Clovers 框架](#响应处理器-Leaf) 3. 在运行阶段先启动实例再执行响应任务

下面是 nonebot_plugin_clovers.adapters.onebot.v11 中的一个例子

```python
@adapter.property_method("user_id")
async def _(event: MessageEvent):
    return event.get_user_id()
```

这样，如果 handle 声明了 `properties=["user_id"]` 参数，那么原始 Event 实例的 `event.properties["user_id"]` 就会是 `event.get_user_id()` 的返回值

诸如此类的方法，都需要在适配器方法中定义

## 发送消息 send_method 方法

在[指令-响应任务的响应](#指令-响应任务的响应)的示例中，我们使用了返回的 `Result` 类实例的 `key` 标记为 `text`

发送消息也是适配器的工作，但是如果你不定义的话，适配器并不知道该怎么发送 `text` 消息

所以你需要在适配器方法中定义发送这种消息的方法

适配器会向 send 方法传入 `Result` 类实例的 `data` 属性作为第一个参数。

此外 send 方法会接受 clovers 响应时传入的额外关键字参数。

下面是简化的 nonebot_plugin_clovers.adapters.onebot.v11 中的一个例子

```python
@adapter.send_method("text")
async def _(message, /, bot: Bot, event: MessageEvent):
    await bot.send(event=event, message=MessageSegment.text(message))
```

## 获取响应 call_method 方法

在[指令-响应任务获取平台参数](#指令-响应任务获取平台参数)第二个示例中，我们 call 了两个获取响应方法

其中 group_id 是 property_method 注册的，它不需要参数，返回值等价于声明`properties=["group_id"]` 的 `event.properties["group_id"]`

另一个 group_member_info 需要参数，需要用 call_method 注册

下面是 nonebot_plugin_clovers.adapters.onebot.v11 中的一个例子

```python
@adapter.call_method("group_member_info")
async def _(group_id: str, user_id: str, /, bot: Bot):
    user_info = await bot.get_group_member_info(group_id=int(group_id), user_id=int(user_id))
    member_user_id = str(user_info["user_id"])
    user_info["group_id"] = str(user_info["group_id"])
    user_info["user_id"] = member_user_id
    user_info["avatar"] = f"https://q1.qlogo.cn/g?b=qq&nk={member_user_id}&s=640"
    return user_info
```

call_method 注册的方法只接受位置参数

此外 send_method 也会注册 call_method 方法，但是 send_method 只接受一个参数，也就是返回值 Result 实例的 data 部分

如果希望发送 "你好，世界", 你除了可以让函数返回 `Result("text", "你好，世界")`之外，你也可以这样用

```python
@plugin.handle(["测试"])
async def _(event: Event):
    await event.call("text", "你好，世界")
```

如果 call_method, property_method, send_method 注册了同名的方法

那么 call 会调用 call_method 注册的方法

返回的 Result 会调用 send_method 注册的方法

声明的 properties 会调用 property_method 注册的方法

如果 property_method, send_method 注册了同名的方法，那么 call 会调用第一个注册的方法，**但是非常不建议使用这个特性。**

# 类型协议 CloversProtocol

适配器方法会根据插件声明的参数构建参数，处理响应结果。但是同名参数不一定是兼容的

假如：插件声明了需要参数 `user_id` 同时默认此参数是 `int` 类型。适配器声明了参数 `user_id`，但返回值是 `str` 类型。

插件拿到的 `user_id` 实际上是 `str` 类型，但由于适配器存在同名方法不会报错，所以可能会导致非常严重的问题。

为了避免这种情况 clovers 提供了一个类型协议，如果插件设置了类型协议则会进行类型响应过滤。

插件需要包含适配器的全部可能类型才会检查通过。

```python
class AdapterProtocol:
    user_id: str

class PluginProtocol:
    user_id: str | int

print(check_compatible(AdapterProtocol, PluginProtocol)) # True
print(check_compatible(PluginProtocol, AdapterProtocol)) # False
```

`check_compatible` 只会检查两个协议都有的字段，如果插件声明了适配器不存在的字段，初始化行为是未定义而非不兼容

适配器的代码中如果写了完整的类型提示则不需要显示设置适配器的类型协议。

```python
@adapter.property_method("user_id")
async def _(event: Event) -> str:
    return event.get_user_id()
```

这样写相当于

```python
@adapter.property_method("user_id")
async def _(event: Event):
    return event.get_user_id()

class AdapterProtocol:
    user_id: str

adapter.set_protocol("properties", AdapterProtocol)
```

插件则需要显式设置协议

# 响应处理器 Leaf

Leaf 是一个用于处理适配器与插件的响应处理器基类。

继承这个类并实现 extract_message 方法即可创建一个可用的响应处理器

extract_message 接受的参数来自调用 response 方法时转入的参数，一般来说不同运行例有不同的参数。

```python
from clovers import Leaf as BaseLeaf


class MyLeaf(BaseLeaf):
    def extract_message(self, state: dict, **ignore):
        inputs = state.get("message")
        if inputs is None:
            return None
        if inputs.startswith(Bot_Nickname):
            inputs = inputs.lstrip(Bot_Nickname)
            state["to_me"] = True
        return inputs
```

使用方法

```python
leaf = MyLeaf("Sample")

asyncio.create_task(leaf.response(state=state, others=others))

```

这样就会触发响应

# 客户端 Client

上述响应处理器触发响应的代码一般是在某个循环里面持续运行，下面例举使用 clovers 客户端的情况。

clovers 框架提供了 `Client` 类，用于编写 clovers 客户端。

下面是 clovers_client 模块里面 onebot_v11 客户端的简化实现方法

```python
from clovers import Client as CloversClient


class MyClient(CloversClient):
    def __init__(self, url: str, ws_url: str, name="OneBot V11"):
        super().__init__()
        self.name = name
        self.url = url
        self.client = httpx.AsyncClient()
        self.ws_connect = websockets.connect(ws_url)

    async def post(self, endpoint: str, **kwargs) -> dict:
        resp = await self.client.post(url=f"{self.url}/{endpoint}", **kwargs)
        resp = resp.json()
        return resp

    async def run(self):
        ws = await self.ws_connect
        async with self:
            async with self.client:
                while self.running:
                    async for recv in ws:
                        asyncio.create_task(leaf.response(post=self.post, recv=json.loads(recv)))
        await ws.close()

```

## 运行

```python

# 配置日志记录器，不配置可能无法输出日志

from clovers.logger import logger as clovers_logger
clovers_logger.setLevel(log_level)
clovers_logger.addHandler(hdlr)

# 进行各种配置

asyncio.run(MyClient().run())
```

clovers.logger.logger 实际上是 logging.getLogger("clovers")，请依据需求配置

## 寄生

寄生依然需要配置日志记录器，但不执行 run 方法

根据下面是 QQbot PythonSDK 独立运行和寄生的区别

```python
class Client(CloversClient):
    async def run(self):
        async with self:
            async with QQBotClient(Intents(public_guild_messages=True, public_messages=True)) as client:
                await client.start(appid=appid, secret=secret)
async def main():
    await Client().run()
```

```python
class Client(CloversClient):
    async def run(self):
        raise RuntimeError("寄生客户端不支持运行")

async def main():
    async with QQBotClient(Intents(public_guild_messages=True, public_messages=True)) as qq_bot_client:
        async with Client():
            await qq_bot_client.start(appid=appid, secret=secret)
```

在寄生的情况下如果没有合适的地方使用 async with 上下文也可以使用 hook 的方式

```python
from nonebot import get_driver

clovers_client = Client()

get_driver().on_startup(clovers_client.startup)
get_driver().on_shutdown(clovers_client.shutdown)
```
