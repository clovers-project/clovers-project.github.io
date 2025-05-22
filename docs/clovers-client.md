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

# 介绍

[项目地址](https://github.com/clovers-project/clovers-client)

**注意：当前项目目前还十分简陋，在版本号更新到 0.1.0 之前不建议使用**

# 配置与使用方法

首先先安装本模块

<details open>
<summary>pip</summary>

```bash
pip install clovers-client
```

</details>

<details>
<summary>poetry</summary>

```bash
poetry add clovers-client
```

</details>

在一个新文件夹里创建一个 xxx.py 文件

```python
# bot.py
import asyncio
import logging
from clovers.logger import logger
from clovers.config import Config
from clovers_client.qq import Client as Client

logger.setLevel(level=logging.INFO)
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s][%(levelname)s]%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

Config.environ().save()
asyncio.run(Client().run())
```

运行后会在当前路径会创建一个 clovers.toml 文件

往里面填写配置后重新运行就可以使用了
