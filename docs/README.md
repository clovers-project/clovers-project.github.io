# 概述

_✨ 高度自定义的聊天平台 Python 异步机器人指令-响应插件框架 ✨_

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/clovers.svg)](https://pypi.python.org/pypi/clovers)
[![pypi download](https://img.shields.io/pypi/dm/clovers)](https://pypi.python.org/pypi/clovers)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Github](https://img.shields.io/badge/GitHub-Clovers-00CC33?logo=github)](https://github.com/clovers-project/clovers)

- 本项目遵循着高度自定义的理念。因此本文所有的范例并不作为任何标准。希望你可以随心所欲的遵循自己的风格。
- 本项目无法单独使用，需要寄生在其他框架或循环中，比如 [NoneBot2](https://nonebot.dev/)
- 如果你有更好的想法，[欢迎提 issue 或 pr。](https://github.com/clovers-project/clovers)
- **注意事项：确保你的 Python 版本 >= 3.12**

# 其他的介绍

- Clovers 实例管理多个适配器和插件，但是不与响应对接。
- 因为一般来说一个适配器适配一种响应，所以需要与响应对接的其实是 Leaf 实例，Leaf 负责管理单个适配器与插件
- 可以使用 Clovers 实例生成 Leaf 实例，也可以直接使用 Leaf 类创建实例。
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

以 Nonebot2 框架作为宿主,并且使用 `nonebot.adapters.onebot.v11` 适配器和 `nonebot_plugin_clovers` 预制方案为例。

创建一个 NoneBot 项目之后在 `\src\plugins` 新建一个本地插件（本地插件的位置是你指定的）

例如你创建的项目名为 `connect_to_the_clovers.py`

```python
from nonebot import on_message, get_driver
from nonebot.matcher import Matcher
from nonebot_plugin_clovers import clovers, extract_command
from nonebot.adapters.onebot.v11 import Bot, MessageEvent
from nonebot_plugin_clovers.adapters.onebot.v11 import __adapter__ as adapter


clovers.register_adapter(adapter)
leaf = clovers.leaf(adapter.name)
driver = get_driver()
driver.on_startup(leaf.startup)
driver.on_shutdown(leaf.shutdown)

main = on_message(priority=20, block=False)


@main.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    message = extract_command(event.get_plaintext())
    if await leaf.response(message, bot=bot, event=event):
        matcher.stop_propagation()
```

在 nb 项目文件夹下 clovers.toml 中填写配置

```toml
# clovers.toml
[clovers]
plugins = [ "clovers_tabletop_helper",]
plugin_dirs = [ "./clovers_library/plugins",]
adapters = []
adapters_dirs = [ "./clovers_library/adapters",]
```

_注：此是 nonebot_plugin_clovers 的配置，并不是 clovers 项目的标准_

在 plugins 配置填写所加载插件的包名

在 plugin_dirs 内文件夹下放入本地 clovers 插件

在 adapters 配置填写所加载 adapter 的包名

在 adapters_dirs 内 文件夹下放入本地 clovers 适配器

即可使用。

## 发生了什么

`nonebot_plugin_clovers` 是一个寄生在 NoneBot 框架下的预置方案，内含一些基础的 adapter.Adapter 实例

通过 NoneBot2 的响应器获取指令使 clovers 实例内插件响应

但是 clovers 的理念是完全的自定义，所以 `nonebot_plugin_clovers` 仅作为一种范例，并不作为任何标准。

更推荐的是自行[编写适配器](#编写适配器)

# 从插件开始

你需要编写一个模块，这个模块需要包含一个`__plugin__`属性，这个属性是一个 plugin.Plugin 实例

关于 Plugin 类的详细介绍可以参考[文档](/document#pluginplugin)

## 开始编写插件

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
@plugin.handle({"其他测试"})
async def _(event: Event):
    pass
```

## 创建 Plugin 实例的参数

| 参数名       | 类型                             | 描述                                   |
| ------------ | -------------------------------- | -------------------------------------- |
| name         | str                              | 插件名称                               |
| priority     | int                              | 插件优先级                             |
| block        | bool                             | 如果本插件有响应，是否阻断后续插件触发 |
| build_event  | Optional[Callable[[Event],Any]]  | 构建 event 的方法                      |
| build_result | Optional[Callable[[Any],Result]] | 构建 result 的方法                     |

## 任务和事件参数

`startup` 在插件初始化时执行，无参数。

`shutdown` 在插件关闭时执行，无参数。

`handle` 指令响应任务，由指令触发，获取到事件参数 `event` ， `event`并不是某个特定的类型。而是原始 `Event` 实例发送给 `build_event` 构建的返回值。

由此可见原始 `Event` 类你在指令响应任务的函数中唯一获得的参数，你需要的所有东西都在这里。

关于 Event 类的详细介绍可以参考[文档](/document#pluginevent)

## 指令-响应任务的指令

指令-响应任务的 `commands` 参数可以是字符串，也可以是字符串列表，也可以是一个 re.Pattern 实例

当指令是字符串列表时，handle 装饰器会认为这个指令是一个指令列表，那么它会对字符串进行 startswith 判断。

如果成功触发响应，那么 event.args 会是原指令去掉指令部分后的字符串并按照空格分割为列表。

```python
# 触发指令为"你好 世界"时，输出 ["世界"]
# 触发指令为"helloworld with extra args"时，输出 ["world","with","extra","args"]
@plugin.handle(["你好", "hello"])
async def _(event: Event):
    print(event.args)
```

当指令是字符串时，handle 装饰器会认为这个指令是一个正则字符串，那么它会对指令进行正则匹配。

如果成功触发响应，那么 event.args 会是正则字符串中的 group 列表

```python
# 触发指令为"i love you"时，输出 ["i "," you"] 使用时注意去掉参数里的空格
# 触发指令为"you love me"时,输出 ["you "," me"]
# 触发指令为"make love"时,输出 ["make ", None]
@plugin.handle(r"^(.+)love(.*)")
async def _(event: Event):
    print(event.args)
```

## 指令-响应任务的响应

指令-响应任务函数的返回值可以是任意类型,这个返回值会发送给 build_result 方法构建成 Result 实例。

如果你的插件的 build_result is None 那你就必须返回一个 Result 实例。

就像你的 build_event is None ,你的参数会是原始的 Event 实例那样。

关于 Result 类的详细介绍可以参考[文档](/document#pluginresult)

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
    rule=lambda e: e.properties["to_me"],
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
@plugin.temp_handle("temp_handle1", ["user_id", "group_id"], 30)
async def _(event: Event, finish):
    if i_should_finish:
        finish()
```

临时任务没有优先级，而且是最优先触发。

临时任务可以在任务中注册,在注册时需要传入一个字符串 `key` 作为这个临时任务的键 。

**注意，一般任务也可以在任务中注册，但是不会生效并且可能导致未定义的行为**

`key` 临时任务 key

如果这个 key 被注册过，即使之前的任务没有超时也没有结束，那么也会被新注册的任务覆盖。

如果你有对临时任务不被覆盖的强烈需求，请使用 UUID 作为键名

`timeout` 任务超时时间（秒）

temp_handle 会被任意消息触发，请传入规则或在响应函数中内置规则。

temp_handle 任务的参数除了 event，你还会获得一个 Callable 参数 finish，它的功能是结束本任务。如果你不结束，在临时任务超时前每次消息都会触发。

## 插件配置文件

配置文件存放在一个 toml 文件里，文件由你指定

关于配置的详细介绍可以参考[文档](/document#config)

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
from clovers.config import config as clovers_config

config_key = __package__  # 或者你自定义的任何key
default_config = {"nickname": "小叶子", "timeout": 600}
# 各种方法获取配置
config_data = clovers_config.get(config_key, {})
default_config.update(config_data)
# 把配置存回总配置
clovers_config[config_key] = config_data
```

当然，也许你更喜欢这样做

```python
from pydantic import BaseModel


class Config(BaseModel):
    nickname: str = "小叶子"
    timeout: int = 600


from clovers.config import config as clovers_config

config_key = __package__  # 或者你自定义的任何key
config_data = Config.model_validate(clovers_config.get(config_key, {}))
clovers_config[config_key] = config_data.model_dump()
```

为了更方便的修改配置，你可以保存当前的配置，这样所有配置项都会出现在配置文件里

```python
@plugin.startup
async def _():
    clovers_config.save()
```

# 编写适配器

你需要编写一个模块，这个模块需要包含一个`__adapter__`属性，这个属性是一个 adapter.Adapter 实例

关于 Adapter 类的详细介绍可以参考[文档](/document#adapteradapter)

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

property 方法的参数是 clovers 实例响应时传入的，我们可以传入任意参数，请参考 [使用 Clovers 框架](#使用-clovers-框架) 3. 在运行阶段先启动实例再执行响应任务

下面是 nonebot_plugin_clovers.adapters.onebot.v11 中的一个例子

```python
@adapter.property_method("user_id")
async def _(event: MessageEvent):
    return event.get_user_id()
```

这样，如果 handle 声明了 `properties=["user_id"]` 参数，那么原始 Event 实例的 `event.properties["user_id"]` 就会是 `event.get_user_id()` 的返回值

诸如此类的方法，都需要在适配器方法中定义

## 发送消息 send_method 方法

在[指令-响应任务的响应](#指令-响应任务的响应)的示例中，我们使用了返回的 `Result` 类实例的 `send_method` 标记为 `text`

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

如果希望发送 "你好，世界" ,你除了可以让函数返回 `Result("text", "你好，世界")`之外，你也可以这样用

```python
@plugin.handle(["测试"])
async def _(event: Event):
    await event.call("text", "你好，世界")
```

如果 call_method, property_method, send_method 注册了同名的方法

那么 call 会调用 call_method 注册的方法

返回的 Result 会调用 send_method 注册的方法

声明的 properties 会调用 property_method 注册的方法

如果 property_method, send_method 注册了同名的方法，那么 call 会调用 第一个注册的方法，但是不建议使用这个特性。

# 使用 Clovers 框架

## 配置日志记录器

可以不配置，但可能无法输出日志

```python
from clovers.logger import logger as clovers_logger
clovers_logger.setLevel(log_level)
clovers_logger.addHandler(hdlr)
```

clovers.logger.logger 实际上是 logging.getLogger("clovers")，请根据宿主的需求进行配置

接下来进程内所有日志都依据此时的配置

## 加载插件及适配器

<details close>
<summary>  使用多个适配器对接多个响应 </summary>

1. 创建一个 Clovers 实例

```python
from clovers import Clovers

clovers = Clovers()

```

2. 向 Clovers 实例注入适配器

**创建一个适配器，并编写适配器方法**

```python

adapter = Adapter("ExampleAdapter")
# do something
clovers.register_adapter(adapter)

```

**从其他模块导入适配器**

```python

from other_moudle import __adapter__ as adapter

clovers.register_adapter(adapter)

```

或者

```python

clovers.load_adapter("other_moudle")

```

**从自定义位置加载适配器**

```python

from clovers.tools import list_modules

clovers.load_adapters(list_modules("path/to/adapters"))

```

3. 加载插件

**创建一个插件并编写响应**

```python

plugin = Plugin("ExamplePlugin")
# do something
clovers.register_plugin(plugin)

```

**从其他模块导入插件**

```python

from other_moudle import __plugin__ as plugin

clovers.register_plugin(plugin)

```

或者

```python

clovers.load_plugin("other_moudle")

```

**从自定义位置加载插件**

```python

from clovers.tools import list_modules

clovers.load_plugins(list_modules("path/to/plugins"))

```

4. 编写通用的适配器方法

```python

@clovers.adapter.property_method("xxx")
async def *(event): ...

```

被这个 clovers 实例管理的适配器方法都会有这个方法，除非适配器有同名方法。

5. 创建 Leaf 实例

```python

leaf = clovers.leaf("适配器的名字")

```

被 clovers 实例创建的 Leaf 实例都已经注册好了插件，可以直接对接适配器支持的响应

</details>

<details open>
<summary>  使用单个适配器对接单个响应 </summary>

这里可以看作是上个例子的特殊情况，可以直接用上述方法。但是如果你没有对接多适配器的需求，这种方法是更推荐的。

1. 无论通过何种方法获取，首先你要先有一个适配器。然后用这个适配器创建一个 Leaf 实例

```python

from clovers import Leaf

leaf = Leaf(adapter)

```

2. 加载插件

**创建一个插件并编写响应**

```python

plugin = Plugin("ExamplePlugin")
# do something
leaf.plugins.append(plugin)

```

**从其他模块导入插件**

```python

from other_moudle import __plugin__ as plugin

leaf.plugins.append(plugin)

```

**从自定义位置加载插件**

```python

from clovers.tools import list_modules, load_module

leaf.plugins.extend(load_module(module,"__plugin__") for module in list_modules("path/to/plugins"))

```

3. 启动前先给加载的插件按照优先级排序

```python

leaf.plugins.sort(key=lambda x: x.priority)

```

被 clovers 实例创建的 Leaf 实例都已经注册好了插件，可以直接对接适配器支持的响应

</details>

## 启动与对接响应

现在你已经可以运行 Leaf 实例了

接下来使用 NoneBot 框架举例：

```python

from nonebot import on_message, get_driver
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11 import Bot, MessageEvent

driver = get_driver()
driver.on_startup(leaf.startup)
driver.on_shutdown(leaf.shutdown)

main = on_message(priority=20, block=False)


@main.handle()
async def _(bot: Bot, event: MessageEvent, matcher: Matcher):
    if await leaf.response(event.get_plaintext(), bot=bot, event=event):
        matcher.stop_propagation()

```

leaf 是上述操作中创建好的 Leaf 实例，上面的例子没有体现 leaf 的创建过程。

总体来说 Leaf 实例对接响应需要注意的有：

在合适的时机执行 leaf.startup 与 leaf.shutdown 任务。

把接收到的消息纯文本传入 leaf.response 以触发响应。

传入 leaf.response 的额外的关键字参数是 leaf.adapter 中全部方法需要的所有参数。

leaf.response 的返回值是 int ,即这次的触发响应了几条消息。
