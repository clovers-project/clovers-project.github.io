# clovers

## clovers.Leaf

_属性：_

`adapter` 当前实例下的插件依靠此适配器中方法获取数据。

`plugins` 插件列表，在运行前载入。

`wait_for` 异步任务列表，在关闭任务时需等待此任务列表

`running` 是否正在运行

**response**

对指令进行响应

_参数：_

`command` 指令

`**extra` 适配方法需要的额外参数

_返回值：_

`int` 表示此指令触发了多少个响应

**startup**

启动任务

_参数：_

无

_返回值：_

`None`

**shutdown**

结束任务

_参数：_

无

_返回值：_

`None`

## clovers.Clovers

_属性：_

`adapter` 全局适配器，一个特殊的 Adapter 实例。此 leaf 方法创建的 Leaf 实例的适配器会与此混合。

`plugins` 插件列表，在运行 clovers 实例前载入。

`adapters` 适配器字典，key 为适配器名称，value 为适配器实例。

**leaf**

创建一个 clovers 预制的 Leaf 实例

_参数：_

`key` 适配器名称

_返回值：_

`clovers.Leaf`

**register_plugin**

注册插件

_参数：_

`plugin` plugin.Plugin 实例

_返回值：_

`None`

**load_plugin**

注册插件

_参数：_

`name` 插件名,可以是当前进程路径下的一个包名或者 Python lib 中的一个模块名。

_返回值：_

`None`

**load_plugins**

加载插件

_参数：_

`namelist` 插件名列表

_返回值：_

`None`

**register_adapter**

注册适配器

_参数：_

`adapter` adapter.Adapter 实例

_返回值：_

`None`

**load_adapter**

注册适配器

_参数：_

`name` 适配器名,可以是当前进程路径下的一个包名或者 Python lib 中的一个模块名。

_返回值：_

`None`

**load_adapters**

加载插件

_参数：_

`namelist` 适配器名列表

_返回值：_

`None`

# adapter

## adapter.Adapter

plugin.Adapter 类是响应器的核心

_属性：_

`name` 适配器名

`properties_lib` 属性方法字典

`sends_lib` 发送方法字典

`calls_lib` 调用方法字典

**property_method**

添加一个属性方法

_参数：_

`method_name` 属性方法名

_返回值：_

装饰器

**send_method**

添加一个发送方法

_参数：_

`method_name` 发送方法名

_返回值：_

装饰器

**call_method**

添加一个调用方法

_参数：_

`method_name` 调用方法名

_返回值：_

装饰器

**remix**

混合适配器方法，此适配器会获得参数适配器存在但自己不存在的方法

_参数：_

`adapter` 适配器实例

_返回值：_

`None`

**response**

获得适配器的响应

_参数：_

`handle` 将要用此适配器响应的指令响应任务

`event` 将要用此适配器处理的事件参数

`**kwargs` 此适配器需要的其它参数。

# plugin

## plugin.Result

`send_method` 控制适配器方法用什么方式发送你的数据。

`data` 要发送的原始数据。

## plugin.Event

`raw_command` 触发本次响应的原始字符串。

`args` 解析的参数列表。

`properties` 一个字典。包含了一些平台特有的参数。

`calls` 适配器的调用方法。

`extra` 适配器的额外参数。

**call**

调用适配器方法

_参数：_

`key` 调用的方法名。

`*args` 调用的位置参数。

_返回值：_

适配器方法的返回值。

## plugin.Handle

_属性：_

`func` 指令响应器的异步函数本体，参数为 plugin.Event 类型，返回值为 plugin.Result 类型。

`properties` 指令响应器声明的参数。

`block` 是否阻断插件内后续任务触发。

## plugin.PluginCommands

`str | Iterable[str] | re.Pattern | None` 的类型别名，是指令注册器可接受的参数类型。

## plugin.Plugin

plugin.Plugin 类是插件的核心，也是你编写插件的入口

_属性：_

`name` 插件名

`priority` 插件优先级

`block` 是否阻断后续其他插件触发。

`build_event` event 的构建方法

如果你不想在任务函数内使用原始的 event,你也可以自建 event 类,然后在创建 plugin 实例时注入 build_event 方法。

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

@plugin.handle(["测试"],["user_id"])
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

**直接调用**

_参数：_

`message` 类型 `str` 插件需要响应的消息

_返回值：_

`list[tuple[Handle, Event]] | None` 返回此插件响应的任务和需要适配器注入参数的事件列表

元祖内的 Event 实例需要经过适配器处理后才会传入 Handle 实例的 func 方法

**ready**

准备插件。Leaf 实例启动时会对每个插件都调用一次 ready 方法。

_参数：_

无

_返回值：_

`bool` 如果当前插件没有响应任务，则返回 False，否则返回 True。

**handle_warpper**

构建插件的原始 event->result 响应

_参数：_

函数

_返回值：_

函数

**commands_register**

指令注册器

_参数：_

`commands` 指令

`key` 响应器的 key

`priority` 优先级

_返回值：_

`None`

**handle**

注册插件指令响应器

_参数：_

`command` 触发任务的指令。

`properties` 声明需要的参数。

`rule` 响应的触发的规则。

`priority` 插件内部指令-响应任务的优先级。

`block` 如果本任务有响应，是否阻断插件内后续任务触发。

_返回值：_

装饰器

**temp_handle**

_参数：_

`key` 临时任务 key 如果这个 key 被注册过，即使之前的任务没有超时也没有结束，那么也会被新注册的任务覆盖。

`properties` 声明需要的参数。

`timeout` 临时指令的过期时间

`rule` 响应的触发的规则。

`block` 如果本任务有响应，是否阻断插件内后续任务触发。

_返回值：_

装饰器

**startup**

装饰器

注册一个启动任务

**shutdown**

装饰器

注册一个结束任务

### plugin.Plugin.Rule

_属性：_

`checker` 函数列表

    - 此列表内的函数的返回值必须是布尔值
    - 如果列表内的任意函数返回值为 False，则此任务不会被执行
    - 列表内函数的参数是 build_event 的返回值，如果 build_event 为 None，则此参数为原始 Event 实例

**check**

函数装饰器，为 handle.func 添加检查

### plugin.Plugin.Finish

结束临时任务的类，作为参数传入临时任务函数中，表示本任务结束。

直接调用是结束任务，调用 `delay` 方法并传入秒数可以相应延长任务超时时间

下面是示例：

```python

@plugin.temp_handle("test", timeout=10)
async def _(event: Event, finish: plugin.Plugin.Finish):
    # do something
    if condition:
        finish() # 结束任务
    else:
        finish.delay(10) # 不结束任务并且延长任务超时时间

```

# config

在我们写插件，适配器，或其他任何场景我们需要用到配置时。

除了 json，数据库，乃至系统环境变量等方法外，我们还可以使用此模块内的配置类来进行配置的存取。

配置类是一个字典的子类，所以你可以把它当做字典随意使用。

当然我们也可以让每个插件都遵循一定的规则。

下面是推荐的规则：

```python
from pydantic import BaseModel

class Config(BaseModel):
    # 定义一些属性

from clovers.config import config as clovers_config

config_key = __package__ # 或者你自定义的任何配置键名
config_data = Config.model_validate(clovers_config.get(config_key, {})) # 从 clovers_config 获取配置字典并规范成 Config 类型
clovers_config[config_key] = config_data.model_dump() # 将规范配置存回 clovers_config
```

## config.Config

配置类，为字典的子类

_属性：_

`path` 定义调用 save() 方法时配置文件保存在哪个位置。

**load**

类方法

_参数：_

`path` 从这个地址加载配置文件，并将其保存到 self.path 属性中

_返回值：_

`Config` 实例

**save**

保存配置文件
_参数：_

无

_返回值：_

`None`

## config.config

运行时的配置文件实例

这个实例的文件位置从环境变量中的 `clovers_config_file` 读取，如果没有找到，则使用 `clovers.toml` 作为默认配置文件。

# logger

## logger.logger

默认的日志记录器

# tools

**load_module**

加载模块

_参数：_

`name` 模块名

`attr` 模块的属性名,如果此项是 None 则返回模块本身

_返回值：_

加载到的东西

**list_modules**

列出模块名

_参数：_

`path` 把此路径下的模块转换成包名

_返回值：_

`list[str]` 包名列表
