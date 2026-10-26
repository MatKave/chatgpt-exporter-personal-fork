# ChatGPT Exporter Personal

[简体中文](docs/README.zh-CN.md) · [Install userscript](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)

A small customization of [ChatGPT Exporter](https://github.com/pionxzh/chatgpt-exporter) for saving conversations as readable Markdown files.

The original exporter can embed images in Markdown, but a Base64 image URL can fill an entire line with thousands of characters. This build moves those URLs into reference definitions at the end of the file. It also shows timestamps in Beijing time and makes exported filenames friendlier to Windows.

## Example

Upstream **Embed** mode:

```md
![image](data:image/png;base64,iVBORw0KGgo...)
```

This build's **Reference** mode:

```md
![image][img-001]

[img-001]: data:image/png;base64,iVBORw0KGgo...
```

Both modes keep the image data in a single Markdown file. Reference mode keeps the text easier to edit, and repeated images share one definition; it does not generally reduce file size.

Other changes:
- **Timestamps:** `Asia/Shanghai`, including seconds and a date when the displayed day changes.
- **Conversation creation time:** shown under the Markdown title and in place of the HTML export-time label.
- **Filenames:** Default to `{title}-{create_time}` (conversation creation time in Beijing time) with Windows-safe filenames. Existing custom formats are preserved, except previously shipped upstream/incorrect defaults, which migrate to the corrected default.

Batch export, HTML, JSON, screenshots, the other image modes and ChatGPT compatibility are inherited from upstream.

## Install

1. Install [Tampermonkey](https://www.tampermonkey.net/).
2. **[Install ChatGPT Exporter Personal](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js)**.
3. If you already use the original exporter or a local build of this fork, disable that script to avoid duplicate menus. Refresh ChatGPT.
4. Select an image mode in the export settings. Reference mode is the default on a new installation; conversation timestamps are opt-in.

Tampermonkey checks this repository's `@updateURL` for updates. GitHub Actions checks upstream daily and publishes a new script only if the existing patches still apply and the build and tests pass. It **does not** rewrite incompatible patches.

## Build

This repository stores the customizations rather than a full copy of the upstream source.

On Windows, install Git, Python 3 and Node.js 22.16+ with Corepack, then run:

```bat
Build.cmd
```

See [development](docs/DEVELOPMENT.md) for the patch/build process and [testing](docs/TESTING.md) for export checks.

## Limitations

Some Markdown renderers do not display reference-style `data:` images; switch back to upstream's **Embed** or **Files** mode if needed. The reference option changes Markdown only. Date separators on a long, virtualized conversation may reflect the messages currently visible in the page.

This is an independent build, not an official release from the upstream maintainers. Licensed under [MIT](LICENSE), with the original copyright notice preserved.
