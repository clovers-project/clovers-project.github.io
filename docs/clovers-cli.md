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
      "/casts/install.cast",
      document.getElementById("install"),
      asciinema_config
    );
    window.AsciinemaPlayer.create(
      "/casts/install as plugin.cast",
      document.getElementById("install as plugin"),
      asciinema_config
    );
  };
</script>
<div align="center">
<a href="https://clovers-project.github.io/"><img src="./icon.svg" width="200" height="200" alt="clovers" /></a>

<b><font size="6">Clovers CLI</font></b>

✨ Clovers 控制台应用 ✨

</div>

# 介绍

本项目是一个 [Poetry](https://python-poetry.org/) 插件，用于创建 Clovers 项目。

使用 Clovers CLI 创建的项目会自动使用 Poetry 创建虚拟环境。

# 安装

<details open>

<summary> 直接安装（推荐） </summary>

```bash
pipx install poetry-clovers-plugin
```

<div id="install" style="width: 50vw"></div>

_为了防止 poetry-clovers-plugin 把你的 poetry 搞崩所以推荐这种方式。_

</details>

<details>

<summary> 作为 poetry 插件安装 </summary>

作为 poetry 插件安装

```bash
pipx inject poetry poetry-clovers-plugin
```

<div id="install as plugin" style="width: 50vw"></div>

</details>

# 指令

## create

创建一个 Clovers 项目

```bash
clovers create <name>
```

- `<name>`: 项目名称

## run

运行当前路径的 `bot.py`

```bash
clovers run
```

## update

更新当前项目的插件

## plugin

管理 Clovers 项目中的插件

在 Clovers 项目路径下执行

1. 安装插件

```bash
clovers plugin add <name>
```

2. 删除插件

```bash
clovers plugin remove <name>
```

- `<name>`: PyPI 包名

## new

创建一个 Clovers 插件/适配器/客户端

1. 创建一个插件

```bash
clovers plugin new plugin <name>
```

2. 创建一个适配器

```bash
clovers plugin new adapter <name>
```

3. 创建一个客户端

```bash
clovers plugin new client <name>
```

- `<name>`: 创建的插件/适配器/客户端名称

可选参数

- `--namespace` 插件的命名空间，如果创建命名空间包则需指定
- `--flat` 使用平铺项目布局
- `--add-depend` `-d` 添加模板的依赖
