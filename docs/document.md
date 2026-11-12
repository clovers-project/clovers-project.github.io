# base

## Module Attributes

文件级属性

### kwfilter

```python
def kwfilter(func: AdapterMethod) -> AdapterMethod
```

方法参数过滤器

## Info

```python
class Info(ABC)
```

### info

```python
@property
@abstractmethod
def info() -> dict[str, Any]
```

信息

## Adapter

```python
class Adapter(Info)
```

适配器类

**Attributes**:

- `sends_lib` _AdapterMethodLib_ - 发送方法
- `calls_lib` _AdapterMethodLib_ - 调用方法

### property_method

```python
def property_method(method_name: str)
```

添加一个获取参数方法

**Arguments**:

- `method_name` _str_ - 方法名

**Returns**:

(AdapterMethod) -> AdapterMethod: 属性方法装饰器

### send_method

```python
def send_method(method_name: str)
```

添加一个发送消息方法

**Arguments**:

- `method_name` _str_ - 方法名

**Returns**:

(AdapterMethod) -> AdapterMethod: 发送方法装饰器

### call_method

```python
def call_method(method_name: str)
```

添加一个调用方法

**Arguments**:

- `method_name` _str_ - 方法名

**Returns**:

(AdapterMethod) -> AdapterMethod: 调用方法装饰器

### mixin

```python
def mixin(adapter: "Adapter")
```

混合其他兼容方法

**Arguments**:

- `adapter` _Adapter_ - 其他适配器实例

## EventType

```python
class EventType(Protocol)
```

基础事件协议类型，本类型仅用作描述 Event

**Attributes**:

- `message` _str_ - 触发消息
- `args` _Sequence[str]_ - 指令参数
- `properties` _dict[str, Any]_ - 需要的额外属性，由插件声明

## Event

```python
class Event(Info)
```

触发响应的事件

**Attributes**:

- `message` _str_ - 触发插件的消息原文
- `args` _Sequence[str]_ - 指令参数
- `properties` _dict[str, Any]_ - 需要的额外属性，由插件声明

### send

```python
def send(key: str, message: Any)
```

执行适配器发送方法

**Arguments**:

- `key` _str_ - 适配器方法名
- `message` _Any_ - 适配器方法参数

**Returns**:

Coro[None] | None: 适配器发送方法的 Coro，如 key 不存在则返回 None

### call

```python
def call(key: str, *args)
```

执行适配器调用方法，只接受位置参数

**Arguments**:

- `key` _str_ - 适配器方法名
- `*args` - 适配器方法参数

**Returns**:

Coro[Any] | None: 适配器调用方法的 Coro，如 key 不存在则返回 None

## Result

```python
class Result()
```

插件响应结果

**Attributes**:

- `key` _str_ - 响应方法
- `data` _Any_ - 响应数据

## BaseHandle

```python
class BaseHandle(Info)
```

插件任务基类

**Attributes**:

- `func` _EventHandler_ - 处理器函数
- `properties` _set[str]_ - 声明属性
- `block` _tuple[bool, bool]_ - 是否阻止后续插件, 是否阻止后续任务

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

**Returns**:

- `config` _Config_ - 配置对象

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

## AdapterCore

```python
class AdapterCore(Adapter, ModuleLoader[Adapter])
```

适配器核心

**Attributes**:

- `name` _str_ - 项目名
- `adapters` _list[Adapter]_ - 项目管理的适配器列表

## PluginLoader

```python
class PluginLoader(Info, ModuleLoader[Plugin])
```

插件加载器

**Attributes**:

- `name` _str_ - 项目名
- `plugins` _list[Plugin]_ - 项目管理的插件列表

## CloversCoreInterface

```python
class CloversCoreInterface(Info)
```

clovers 适配器基类

## CloversCore

```python
class CloversCore(CloversCoreInterface)
```

clovers 响应处理器基类

**Arguments**:

- `name` _str_ - 项目名
- `temp_handles` _dict[int, list[TempHandle]], optional_ - 临时响应器存储位置. Defaults to {}.

### load_adapter

```python
def load_adapter(adapter_list: list[str] | None = None,
                 adapter_dirs: list[str] | None = None)
```

加载 clovers 适配器

会把目标适配器的方法注册到 self 中，如已有同名方法则忽略

**Arguments**:

- `adapter_list` _list[str]_ - 适配器的包名列表
- `adapter_dirs` _list[str]_ - 适配器的目录列表

### load_plugin

```python
def load_plugin(plugin_list: list[str] | None = None,
                plugin_dirs: list[str] | None = None)
```

加载 clovers 插件, 注意适配器须在加载插件前优先加载，否则插件不会经适配器的协议检查

**Arguments**:

- `plugin_list` _list[str]_ - 插件的包名列表
- `plugin_dirs` _list[str]_ - 插件的目录列表

### startup

```python
async def startup()
```

启动 clovers 核心

### shutdown

```python
async def shutdown()
```

关闭 clovers 核心

### extract_message

```python
@abstractmethod
def extract_message(**extra) -> str | None
```

提取消息

根据传入的事件参数提取消息

**Arguments**:

- `**extra` - 额外的参数

**Returns**:

- `Optional[str]` - 消息

### invoke_handler

```python
async def invoke_handler(handle: BaseHandle, event: Event, extra: dict)
```

使用适配器响应任务

**Arguments**:

- `handle` _BaseHandle_ - 触发的插件任务
- `event` _Event_ - 触发响应的事件
- `extra` _dict_ - 适配器需要的额外参数

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

### dispatch

```python
def dispatch(**extra) -> asyncio.Task[int] | None
```

响应事件

根据传入的事件参数响应事件。

**Arguments**:

- `**extra` - 额外的参数

## CloversMultCore

```python
class CloversMultCore(CloversCoreInterface)
```

多核 clovers 框架

# logger

## Module Attributes

文件级属性

### logger

clovers 全局日志记录器

# plugin

## Handle

```python
class Handle(BaseHandle)
```

指令任务

**Attributes**:

- `command` _Matchable_ - 触发命令
- `properties` _set[str]_ - 声明属性
- `priority` _int_ - 任务优先级
- `block` _tuple[bool, bool]_ - 是否阻止后续插件, 是否阻止后续任务
- `func` _EventHandler_ - 处理器函数

### match

```python
def match(message: str) -> Sequence[str] | None
```

匹配指令

**Arguments**:

- `message` _str_ - 待匹配的消息

**Returns**:

- `Oprtional[Sequence[str]]` - 如果匹配到则返回从 message 提取的参数，如果没有匹配则返回 None

### register

```python
def register(command: Matchable) -> Iterable[str] | re.Pattern | None
```

注册指令

**Arguments**:

- `command` _Matchable_ - 命令

## TempHandle

```python
class TempHandle(BaseHandle)
```

临时任务

**Attributes**:

- `timeout` _float_ - 超时时间
- `func` _EventHandler_ - 处理器函数
- `properties` _set[str]_ - 声明属性
- `block` _tuple[bool, bool]_ - 是否阻止后续插件, 是否阻止后续任务

### delay

```python
def delay(timeout: float | int = 30.0)
```

延长任务

### finish

```python
def finish()
```

结束任务

## Plugin

```python
class Plugin()
```

插件类

**Attributes**:

- `name` _str, optional_ - 插件名称. Defaults to "".
- `priority` _int, optional_ - 插件优先级. Defaults to 0.
- `block` _bool, optional_ - 是否阻止后续任务. Defaults to False.
- `build_event` _EventBuilder, optional_ - 构建事件. Defaults to None.
- `build_result` _ResultBuilder, optional_ - 构建结果. Defaults to None.
- `handles` _set[Handle]_ - 已注册的响应器
- `protocol` _CloversProtocol_ - 同名类型协议

### require

```python
def require(plugin_name: str)
```

声明依赖的插件

**Arguments**:

- `plugin_name` _str_ - 插件名称

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

### run_startup

```python
def run_startup()
```

运行启动任务

### run_shutdown

```python
def run_shutdown()
```

运行结束任务

## Rule

```python
class Rule()
```

响应器规则

### check

```python
def check(func: RawEventHandler) -> RawEventHandler
```

对函数进行检查装饰

### handle_wrapper

```python
def handle_wrapper(rule: Rule.Ruleable | Rule | None = None)
```

构建插件的原始event->result响应

### handle

```python
def handle(command: Matchable,
           properties: Iterable[str] = [],
           rule: Rule[EventType].Ruleable | Rule[EventType] | None = None,
           priority: int = 0,
           block: bool | tuple[bool, bool] = True)
```

注册插件指令响应器

**Arguments**:

- `command` _Matchable_ - 指令
- `properties` _Iterable[str]_ - 声明需要额外参数
- `rule` _Rule.Ruleable | Rule | None_ - 响应规则
- `priority` _int_ - 优先级
- `block` _bool | tuple[bool, bool]_ - 是否阻断后续响应器

### temp_handle

```python
def temp_handle(properties: Iterable[str] = [],
                timeout: float | int = 30.0,
                rule: Rule[EventType].Ruleable | Rule[EventType] | None = None,
                block: bool | tuple[bool, bool] = True,
                state: Any | None = None)
```

创建插件临时响应器

**Arguments**:

- `properties` _Iterable[str]_ - 声明需要额外参数
- `timeout` _float | int_ - 临时指令的持续时间
- `rule` _Rule.Ruleable | Rule | None_ - 响应规则
- `block` _bool | tuple[bool, bool]_ - 是否阻断后续响应器
- `state` _Any | None_ - 传递给临时指令的额外参数
