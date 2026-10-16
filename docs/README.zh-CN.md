# ChatGPT Exporter Personal

[English](../README.md)

在 [ChatGPT Exporter](https://github.com/pionxzh/chatgpt-exporter) 基础上维护的一组轻量增强，主要面向 Markdown 对话归档、北京时间显示和 Windows 文件名兼容。

这是非官方构建，原项目的导出框架、图片下载、批量导出与其他格式仍由上游维护。

## 与官方版本的区别

| 功能 | 官方版本 | 此版本 |
| --- | --- | --- |
| Markdown 图片 | Base64 直接内嵌、ZIP 中的独立图片、忽略图片 | 多一种引用式单文件模式：正文短引用，Base64 定义统一放在文末 |
| 消息时间 | 可选显示系统本地时间，精确到分钟 | 北京时间，精确到秒，日期变化时显示年月日 |
| 对话日期 | 可在元数据中使用时间变量，HTML 标题下显示导出时间 | Markdown 标题后增加创建时间，HTML 标题下改为创建时间 |
| 文件名 | 自定义模板 | 时间变量使用北京时间，进一步清理 Windows 不支持的字符 |

官方的 HTML、JSON、截图、引用、临时对话、批量导出等功能均保留。

短引用格式示例：

```md
![image][img-001]

[img-001]: data:image/png;base64,...
```

图片依然保存在**同一个 Markdown 文件**中，不依赖旁边的 `assets/` 目录。它改善正文的可读性，不代表一定压缩文件；部分 Markdown 阅读器不支持这种形式的 `data:` 图片引用，可切换为官方的“内嵌”或“独立图片文件”模式。

## 安装

1. 安装 [Tampermonkey](https://www.tampermonkey.net/)。
2. 打开 [ChatGPT_Exporter_Personal.user.js](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js) 并安装。
3. 如已安装官方 ChatGPT Exporter，先将其禁用，避免重复菜单，然后刷新 ChatGPT。
4. 在脚本设置中选择图片模式；如需时间戳，手动开启“Conversation Timestamp”及相应的导出选项。

新安装时图片默认选择短引用模式；**消息时间戳仍默认关闭**。

**自动更新：** 公开版构建会将 `@updateURL`、`@downloadURL` 指向此公开仓库的已验证脚本。先安装一次公开版，之后由 Tampermonkey 按其更新检查设置获取新版本。请禁用原先的私有构建或官方版本，避免重复菜单。

## 本地构建

Windows 需要 Git、Python 3 和带 Corepack 的 Node.js 22.16+。在仓库根目录运行：

```bat
Build.cmd
```

构建器会在 `upstream/` 拉取官方源码、应用补丁、安装依赖并执行测试；生成文件为 `dist/ChatGPT_Exporter_Personal.user.js`。

[GitHub Actions](../.github/workflows/sync-and-build.yml) 每日检查上游变化，通过编译和测试后才发布新版本；上游代码与补丁不兼容时会中止，不会自动修改不匹配的代码。

实现与维护说明见 [DEVELOPMENT.md](DEVELOPMENT.md)，导出验收项见 [TESTING.md](TESTING.md)，参与维护请阅读 [CONTRIBUTING.md](../CONTRIBUTING.md)。

## 已知限制

- 时区固定为北京时间，与设备所在地无关。
- 短引用模式仅影响 Markdown。
- 长对话中的消息采用虚拟滚动，当前可见的第一条消息可能被当作日期段的起点。
- 官方脚本与此构建的设置不一定共用，切换前请保留备份。

## 许可

项目使用 [MIT License](../LICENSE)。原项目作者为 [pionxzh](https://github.com/pionxzh)，用户脚本成品保留其版权与许可证声明。
