# ChatGPT Exporter Personal

[English](../README.md) · [安装脚本](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)

基于 [ChatGPT Exporter](https://github.com/pionxzh/chatgpt-exporter) 的定制版本，主要调整对话时间的显示与导出方式，方便按原始时间整理、归档聊天记录。原项目的导出能力仍然保留。

## 与原版的区别

- **消息时间戳：** 按北京时间（`Asia/Shanghai`）显示，精确到秒。每天第一条消息显示完整日期和时间，同一天后续消息只显示时分秒；启用后应用于 ChatGPT 网页以及 Markdown、HTML 导出。
- **对话创建时间：** 在 Markdown 和 HTML 的标题下显示对话创建时间，取代 HTML 原先标注的导出时间。
- **导出文件名：** 默认使用 `{title}-{create_time}`，时间取自**对话创建时刻**，不是最后更新时间或下载时间。日期按北京时间转换，文件名时间格式为 `YYYY-MM-DD_HH-MM-SS`，兼容 Windows。
- **Markdown 图片：** 额外提供 *Reference* 模式，将内嵌的 Base64 图片数据集中放到文件末尾，正文使用短引用。图片仍保存在同一个 Markdown 文件中；这种方式是为了更便于编辑源码，并不减少文件大小。

另外调整了文本文件的编码和 Windows 文件名兼容性。批量导出、其他格式、截图等功能仍主要沿用原项目。

## 安装

1. 安装 [Tampermonkey](https://www.tampermonkey.net/)。
2. 点击 [安装 ChatGPT Exporter Personal](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)。
3. 如果同时装有原版或其他版本的 Exporter，先禁用重复脚本，再刷新 ChatGPT 页面。

消息时间戳需要在设置中开启。新安装默认使用 Reference 图片模式，仍可切换为原版的 **Embed** 或 **Files**。如果之前保存过其他文件名模板，可以在设置中点击“恢复本版默认命名（对话创建时间）”。

## 更新与构建

GitHub Actions 每天检查原项目源码，应用定制补丁，编译和测试成功后才发布新脚本；如果上游变更导致补丁不兼容，就停止发布，保留此前可用的版本。Tampermonkey 通过仓库中的 `@updateURL` 检查更新。

仓库保存的是定制补丁，不另行维护一整份原版源码。在 Windows 下安装 Git、Python 3、Node.js 22.16+ 和 Corepack 后，运行：

```bat
Build.cmd
```

开发和构建细节见 [DEVELOPMENT.md](DEVELOPMENT.md)，浏览器导出检查项见 [TESTING.md](TESTING.md)。

## 注意事项

- 时间显示固定采用北京时间，不跟随设备时区。
- 部分 Markdown 阅读器不支持引用式 `data:` 图片链接，遇到这种情况可改用 **Embed** 或 **Files**。
- ChatGPT 长对话存在虚拟滚动，网页上的跨天日期标记可能受当前加载的消息影响。无法获取对话创建时间时，脚本不会自动将下载时间冒充创建时间。

这是 ChatGPT Exporter 的非官方定制版本，保留原作者版权声明，采用 [MIT License](../LICENSE)。
