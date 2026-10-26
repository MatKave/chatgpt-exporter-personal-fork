# ChatGPT Exporter Personal

[English](../README.md) · [安装脚本](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)

基于 [ChatGPT Exporter](https://github.com/pionxzh/chatgpt-exporter) 的轻量定制，主要为了更方便地保存和整理 Markdown 对话记录。

官方已经可以把图片以 Base64 内嵌到 Markdown，但一张图片就可能在正文里占据很长的一行。这个版本将图片数据统一放到文末，正文只保留短引用；另外统一了北京时间显示、创建时间和 Windows 文件名格式。

## 导出效果

官方 **Embed** 模式：

```md
![image](data:image/png;base64,iVBORw0KGgo...)
```

新增的 **Reference** 模式：

```md
![image][img-001]

[img-001]: data:image/png;base64,iVBORw0KGgo...
```

两种格式都把图片保存在**同一个 Markdown 文件**里。短引用的好处是正文更容易阅读和编辑，同一图片重复出现时也能复用定义；并不意味着文件一定更小。

其余定制：
- **消息时间：** 固定按北京时间（`Asia/Shanghai`）显示，精确到秒，跨天时附带年月日。
- **对话创建时间：** Markdown 标题下方添加创建时间；HTML 标题下方由导出时间改为创建时间。
- **文件名：** 默认采用 `{title}-{update_time}`（对话最后更新时间，北京时间），自动清理 Windows 不支持的字符。之前自行设置的其他命名模板会保留。

批量导出、HTML、JSON、截图、其他图片模式和 ChatGPT 页面兼容性仍主要由官方项目维护。

## 安装

1. 安装 [Tampermonkey](https://www.tampermonkey.net/)。
2. 点击 **[安装 ChatGPT Exporter Personal](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)**。
3. 如已安装官方版或之前的私有定制版，先禁用旧脚本，以免菜单重复；然后刷新 ChatGPT。
4. 在导出设置里选择图片模式。新安装默认使用短引用；消息时间戳仍需自行开启。

公开版带有 `@updateURL`，Tampermonkey 会按其更新检查设置获取新版本。GitHub Actions 每天检查官方源码；只有补丁仍兼容且编译、测试通过时，才会发布新脚本。若上游修改导致补丁失效，则保留之前可用的版本，等待人工维护。

## 构建

仓库只保存定制补丁，不复制整套官方源码。

Windows 需要 Git、Python 3、Node.js 22.16+ 及 Corepack；在项目根目录运行：

```bat
Build.cmd
```

源码补丁和构建流程见 [DEVELOPMENT.md](DEVELOPMENT.md)，导出验收项目见 [TESTING.md](TESTING.md)。

## 已知限制

有些 Markdown 阅读器不支持引用式的 `data:` 图片链接，可使用官方的 **Embed** 或 **Files** 模式代替；Reference 只影响 Markdown。长对话使用虚拟滚动，网页时间戳的跨天日期可能取决于当时可见的消息。

本项目为非官方定制，原作者版权声明保留，使用 [MIT License](../LICENSE)。
