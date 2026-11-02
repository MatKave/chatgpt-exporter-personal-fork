# ChatGPT Exporter Personal

[简体中文](docs/README.zh-CN.md) · [Install userscript](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)

A customized build of [ChatGPT Exporter](https://github.com/pionxzh/chatgpt-exporter), focused on conversation timestamps and making exported chats easier to archive. It keeps the upstream export features, with a few changes to how dates, filenames, and Markdown are handled.

## Changes from upstream

- **Message timestamps:** Show messages in Beijing time (`Asia/Shanghai`), down to the second. The first message of each day includes the full date; subsequent messages on the same day show only the time. Available on the ChatGPT page and in Markdown/HTML exports when timestamps are enabled.
- **Conversation creation time:** Show the creation time beneath the conversation title in Markdown and HTML, rather than an HTML export-time label.
- **File naming:** Default to `{title}-{create_time}`—the conversation's creation time, **not** its last update or the time of export. Dates use Beijing time and the Windows-safe `YYYY-MM-DD_HH-MM-SS` format.
- **Markdown images:** An additional *Reference* mode keeps embedded Base64 image data at the end of the Markdown file, leaving short references in the text. The file stays self-contained; this option is about editing the Markdown source, not reducing its size.

Text exports also include Windows-friendly encoding and filename handling. Other formats, batch export, and screenshots remain based on the upstream exporter.

## Install

1. Install [Tampermonkey](https://www.tampermonkey.net/).
2. [Install ChatGPT Exporter Personal](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js).
3. Disable any other installed copy of ChatGPT Exporter to avoid duplicate menus, then refresh ChatGPT.

Message timestamps are optional and can be enabled in the export settings. Reference-style images are the default for a new installation; upstream's **Embed** and **Files** image options remain available. If you have a saved filename pattern from an earlier installation, the settings include a control to restore this build's default.

## Updates and building

GitHub Actions checks the latest upstream source daily, applies the custom patches, and publishes an updated userscript only after the build and tests pass. A change to upstream that breaks a patch stops that publication; it isn't automatically rewritten. Tampermonkey uses this repository's `@updateURL` to check for released updates.

This repository keeps the customization patches rather than a full copy of the upstream source. On Windows, install Git, Python 3, Node.js 22.16+ and Corepack, then run:

```bat
Build.cmd
```

See [development](docs/DEVELOPMENT.md) for the build process and [testing](docs/TESTING.md) for checks to run in ChatGPT.

## Notes

- Time displays in this build use `Asia/Shanghai`, regardless of your device's timezone.
- Some Markdown renderers cannot display reference-style `data:` image links. Use **Embed** or **Files** if that happens.
- ChatGPT virtualizes long conversations, so day separators on the page may depend on which messages are currently mounted. If a conversation's original creation time is unavailable, the exporter will not silently substitute the download time.

Independent, unofficial customization of ChatGPT Exporter. Licensed under [MIT](LICENSE); upstream copyright notices are retained.
