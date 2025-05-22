# clovers

## Leaf

```python
class Leaf(CloversCore)
```

clovers 响应处理器基类

**Attributes**:

- `adapter` _Adapter_ - 对接响应的适配器

### load_adapter

```python
def load_adapter(name: str | Path, is_path=False)
```

加载 clovers 适配器

会把目标适配器的方法注册到 self.adapter 中，如有适配器中已有同名方法则忽略

**Arguments**:

- `name` _str | Path_ - 适配器的包名或路径
- `is_path` _bool, optional_ - 是否为路径

### response_message

```python
async def response_message(message: str, **extra)
```

响应消息

**Arguments**:

- `message` _str_ - 消息内容
- `**extra` - 额外的参数

**Returns**:

- `int` - 响应数量

### extract_message

```python
@abc.abstractmethod
def extract_message(**extra) -> str | None
```

提取消息

根据传入的事件参数提取消息

**Arguments**:

- `**extra` - 额外的参数

**Returns**:

str | None: 消息

### response

```python
async def response(**extra) -> int
```

响应事件

根据传入的事件参数响应事件。

如果提取到了消息，则触发消息响应，如果提取到了事件，则触发事件响应。

否则不会触发响应。

**Arguments**:

- `**extra` - 额外的参数

**Returns**:

- `int` - 响应数量

## Client

```python
class Client(CloversCore)
```

clovers 客户端基类

**Attributes**:

- `wait_for` _list[RunningTask]_ - 运行中的任务列表
- `running` _bool_ - 客户端运行状态

### startup

```python
async def startup()
```

启动客户端

如不在 async with 上下文中则要手动调用 startup() 方法，

### shutdown

```python
async def shutdown()
```

关闭客户端

如不在 async with 上下文中则要手动调用 shutdown() 方法，

### run

```python
@abc.abstractmethod
async def run() -> None
```

运行 Clovers Client ，需要在子类中实现。

.. code-block:: python3
'''
async with self:
while self.running:
pass
'''

## LeafClient

```python
class LeafClient(Leaf, Client)
```

单适配器响应客户端

# config

## Module Attributes

文件级属性

### CONFIG_FILE

默认 clovers 配置文件路径，从环境变量 CLOVERS_CONFIG_FILE 获取

## Config

```python
class Config(dict)
```

clovers 配置类

### load

```python
@classmethod
def load(cls, path: str | Path = CONFIG_FILE)
```

加载配置文件

配置文件为 toml 格式

**Arguments**:

- `path` _str | Path, optional_ - 配置文件路径. Defaults to CONFIG_FILE.

### save

```python
def save(path: str | Path = CONFIG_FILE)
```

保存配置文件

将配置保存为 toml 文件

**Arguments**:

- `path` _str | Path, optional_ - 配置文件路径. Defaults to CONFIG_FILE.

### environ

```python
@classmethod
@cache
def environ(cls)
```

获取默认配置

# core

## Module Attributes

文件级属性

### kwfilter

```python
def kwfilter(func: Method) -> Method
```

方法参数过滤器

## Info

```python
class Info(abc.ABC)
```

### info

```python
@property
@abc.abstractmethod
def info() -> dict[str, Any]
```

信息

## Result

```python
class Result(Info)
```

插件响应结果

**Attributes**:

- `key` _str_ - 响应方法
- `data` _Any_ - 响应数据

## Event

```python
class Event(Info)
```

触发响应的事件

**Attributes**:

- `message` _str_ - 触发插件的消息原文
- `args` _list[str]_ - 参数
- `properties` _dict_ - 需要的额外属性，由插件声明
- `calls` _MethodLib_ - 响应此插件的适配器提供的 call 方法
- `extra` _dict_ - 额外数据储存位置，仅在事件链内传递

### call

```python
def call(key, *args)
```

执行适配器调用方法，只接受位置参数

## BaseHandle

```python
class BaseHandle(Info)
```

插件任务基类

**Attributes**:

- `func` _Handler_ - 处理器函数
- `properties` _set[str]_ - 声明属性
- `block` _tuple[bool, bool]_ - 是否阻止后续插件, 是否阻止后续任务

## Handle

```python
class Handle(BaseHandle)
```

指令任务

**Attributes**:

- `commands` _PluginCommands_ - 触发命令
- `priority` _int_ - 任务优先级
- `func` _Handler_ - 处理器函数
- `properties` _set[str]_ - 声明属性
- `block` _tuple[bool, bool]_ - 是否阻止后续插件, 是否阻止后续任务

## TempHandle

```python
class TempHandle(BaseHandle)
```

临时任务

**Attributes**:

- `timeout` _float_ - 超时时间
- `func` _Handler_ - 处理器函数
- `properties` _set[str]_ - 声明属性
- `block` _tuple[bool, bool]_ - 是否阻止后续插件, 是否阻止后续任务

### finish

```python
def finish()
```

结束任务

### delay

```python
def delay(timeout: float | int = 30.0)
```

延长任务

## Plugin

```python
class Plugin(Info)
```

插件类

**Attributes**:

- `name` _str, optional_ - 插件名称. Defaults to "".
- `priority` _int, optional_ - 插件优先级. Defaults to 0.
- `block` _bool, optional_ - 是否阻止后续任务. Defaults to False.
- `build_event` _Callable[[Event], Any], optional_ - 构建事件. Defaults to None.
- `build_result` _Callable[[Any], Result], optional_ - 构建结果. Defaults to None.

### startup

```python
def startup(func: Task)
```

注册一个启动任务

### shutdown

```python
def shutdown(func: Task)
```

注册一个结束任务

### handle_warpper

```python
def handle_warpper(rule: Rule.Ruleable | Rule | None = None)
```

构建插件的原始 event->result 响应

### handle

```python
def handle(commands: PluginCommand,
           properties: Iterable[str] = [],
           rule: Rule.Ruleable | Rule | None = None,
           priority: int = 0,
           block: bool = True)
```

注册插件指令响应器

**Arguments**:

- `commands` _PluginCommands_ - 指令
- `properties` _Iterable[str]_ - 声明需要额外参数
- `rule` _Rule.Ruleable | Rule | None_ - 响应规则
- `priority` _int_ - 优先级
- `block` _bool_ - 是否阻断后续响应器

### temp_handle

```python
def temp_handle(properties: Iterable[str] = [],
                timeout: float | int = 30.0,
                rule: Rule.Ruleable | Rule | None = None,
                block: bool = True)
```

创建插件临时响应器

**Arguments**:

- `properties` _Iterable[str]_ - 声明需要额外参数
- `timeout` _float | int_ - 临时指令的持续时间
- `rule` _Rule.Ruleable | Rule | None_ - 响应规则
- `block` _bool_ - 是否阻断后续响应器

## Plugin.Rule

```python
class Rule()
```

响应器规则

**Attributes**:

- `checker` _Plugin.Rule.Ruleable_ - 响应器检查器

### check

```python
def check(func: Callable[..., Coroutine]) -> Callable[..., Coroutine]
```

对函数进行检查装饰

## Adapter

```python
class Adapter(Info)
```

响应器类

**Attributes**:

- `name` _str, optional_ - 响应器名称. Defaults to "".
- `properties_lib` _MethodLib_ - 获取参数方法库
- `sends_lib` _MethodLib_ - 发送消息方法库
- `calls_lib` _MethodLib_ - 调用方法库

### property_method

```python
def property_method(method_name: str)
```

添加一个获取参数方法

### send_method

```python
def send_method(method_name: str)
```

添加一个发送消息方法

### call_method

```python
def call_method(method_name: str)
```

添加一个调用方法

### update

```python
def update(adapter: "Adapter")
```

更新兼容方法

### remix

```python
def remix(adapter: "Adapter")
```

混合其他兼容方法

### send

```python
def send(result: Result, **extra)
```

执行适配器发送方法

### response

```python
async def response(handle: BaseHandle, event: Event, extra: dict)
```

使用适配器响应任务

**Arguments**:

- `handle` _BaseHandle_ - 触发的插件任务
- `event` _Event_ - 触发响应的事件
- `extra` _dict_ - 适配器需要的额外参数

## CloversCore

```python
class CloversCore(Info)
```

四叶草核心

此处管理插件的加载和准备，是各种实现的基础

**Attributes**:

- `name` _str_ - 项目名
- `plugins` _list[Plugin]_ - 项目管理的插件列表

### load_plugin

```python
def load_plugin(name: str | Path, is_path=False)
```

加载 clovers 插件

**Arguments**:

- `name` _str | Path_ - 插件的包名或路径
- `is_path` _bool, optional_ - 是否为路径

### handles_filter

```python
def handles_filter(handle: BaseHandle) -> bool
```

任务过滤器

**Arguments**:

- `handle` _Handle_ - 响应任务

**Returns**:

- `bool` - 是否通过过滤

### plugins_filter

```python
def plugins_filter(plugin: Plugin) -> bool
```

插件过滤器

**Arguments**:

- `plugin` _Plugin_ - 插件

**Returns**:

- `bool` - 是否通过过滤

### initialize_plugins

```python
def initialize_plugins()
```

初始化插件

# logger

## Module Attributes

文件级属性

### logger

clovers 全局日志记录器

# utils

## Module Attributes

文件级属性

### import_path

```python
def import_path(path: str | Path)
```

将路径转换成导入名

### list_modules

```python
def list_modules(path: str | Path) -> list[str]
```

获取路径下的模块名
