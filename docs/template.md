# 插件模板

[插件模板](https://github.com/clovers-project/poetry-clovers-plugin/tree/master/poetry_clovers_plugin/core/template/plugin)

示例插件的结构如下，下面的例子会有较为完整的类型提示

```bash
└─template
    clovers.py
    config.py
    __init__.py
```

这里是配置文件，使用 pydantic 进行验证

```python
# config.py

from pydantic import BaseModel
from clovers.config import Config as CloversConfig


class Config(BaseModel):
    random_value: int = 80
    default_flag: bool = True

    @classmethod
    def sync_config(cls):
        """获取 `CloversConfig.environ()[__package__]` 配置并将默认配置同步到全局配置中。"""
        __config_dict__: dict = CloversConfig.environ().setdefault(__package__, {})
        __config_dict__.update((__config__ := cls.model_validate(__config_dict__)).model_dump())
        return __config__
```

创建插件,设置协议,设置返回值构建函数

```python
# clovers.py

from typing import Protocol, overload, Literal
from clovers import EventProtocol, Plugin, Result


class Event(EventProtocol, Protocol):
    user_id: str
    group_id: str | None
    nickname: str
    to_me: bool
    permission: Literal[0, 1, 2, 3]

    @overload
    async def call(self, key: Literal["user_id"]) -> str: ...

    @overload
    async def call(self, key: Literal["group_id"]) -> str | None: ...

    @overload
    async def call(self, key: Literal["nickname"]) -> str: ...

    @overload
    async def call(self, key: Literal["text"], message: str): ...


# 规则的类型提示

type Rule = Plugin.Rule.Checker[Event]


def build_result(result):
    if isinstance(result, Result):
        return result
    if isinstance(result, str):
        return Result("text", result)
    if isinstance(result, bytes):
        return Result("image", result)
    if isinstance(result, list):
        return Result("list", [build_result(seg) for seg in result if seg])


plugin = Plugin(build_result=build_result)
plugin.set_protocol("properties", Event)
```

读取配置，具体指令响应任务的实现

```python
from .clovers import Event, Rule, plugin
from .config import Config

__config__ = Config.sync_config()

# 读取配置

random_value = __config__.random_value
default_flag = __config__.default_flag


permission_check: Rule = lambda e: e.permission > 0
to_me_check: Rule = lambda e: e.to_me


# 应用规则，声明参数
@plugin.handle(["测试", "test"], ["user_id", "group_id", "nickname", "to_me"], rule=to_me_check)
async def _(event: Event):
    return f"UID: {event.user_id}\nGID: {event.group_id}\n昵称: {event.nickname}"


# 应用多个规则
@plugin.handle(["管理员指令"], ["to_me", "permission"], rule=[to_me_check, permission_check])
async def _(event: Event):
    return f"你的权限为：{event.permission}\n配置：\nrandom_value:{random_value}\ndefault_flag:{default_flag}"


# 不声明，但是通过调用获取参数
@plugin.handle(["发送信息"])
async def _(event: Event):
    user_id = await event.call("user_id")
    await event.call("text", f"UID: {user_id}")
    nickname = await event.call("group_id")
    await event.call("text", f"GID: {nickname}")
    nickname = await event.call("nickname")
    await event.call("text", f"昵称: {nickname}")
    return "发送完毕"
```

# 适配器模板

[NoneBotClovers 客户端内置适配器](https://github.com/clovers-project/nonebot-plugin-clovers/tree/master/nonebot_plugin_clovers/adapters)

[Clovers 客户端内置适配器](https://github.com/clovers-project/clovers-client/tree/master/clovers_client)

# 客户端模板

[Clovers 官方客户端](https://github.com/clovers-project/clovers-client)
