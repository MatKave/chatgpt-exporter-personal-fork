# ChatGPT Exporter Personal

[简体中文](docs/README.zh-CN.md)

A small set of enhancements for [ChatGPT Exporter](https://github.com/pionxzh/chatgpt-exporter), built from upstream source. It focuses on readable Markdown archives, consistent Beijing-time timestamps, and Windows-friendly exports.

This is an independent community build, not an official release by the upstream maintainer.

## What changes?

| | Upstream | This build |
| --- | --- | --- |
| Markdown images | Embed data URLs, put images in a ZIP, or omit them | Adds a reference-style mode: short links in the text, Base64 definitions at the end of the same file |
| Message timestamps | Optional local-time display, to the minute | Beijing time, seconds, and a date when the displayed day changes |
| Conversation dates | Export metadata and an HTML export-time label | Adds creation time below the Markdown title and replaces the HTML export-time label with creation time |
| Filenames | Customizable patterns | Beijing-time substitutions and additional Windows filename sanitization |

The original image modes, batch export, HTML, JSON, screenshots, citations, and temporary-chat support come from upstream and remain available.

Reference-style images look like this:

```md
![image][img-001]

[img-001]: data:image/png;base64,...
```

Unlike a separate `assets/` directory, the result is still one Markdown file. The Base64 data is not removed; some Markdown readers do not render `data:` URLs in reference definitions. Choose upstream's **Embed** or **Files** mode if your reader has trouble.

## Install

1. Install [Tampermonkey](https://www.tampermonkey.net/).
2. Open [ChatGPT_Exporter_Personal.user.js](https://raw.githubusercontent.com/MatKave/chatgpt-exporter-personal-fork/main/dist/ChatGPT_Exporter_Personal.user.js) and install the userscript.
3. Disable the original ChatGPT Exporter if it is installed, then refresh ChatGPT.
4. In Exporter settings, choose the image mode and enable conversation timestamps if needed.

The default image mode for a new installation is **reference-style**. Timestamps remain opt-in.

**Updates:** The public build includes `@updateURL` and `@downloadURL` pointing to this repository's verified userscript. Install the public script once, and Tampermonkey can check for newer versions. Disable any previously installed private or upstream exporter to avoid duplicate menus.

## Build

The repository contains patches, not a copy of the upstream source.

On Windows, with Git, Python 3 and Node.js 22.16+ installed (including Corepack):

```bat
Build.cmd
```

The script checks out upstream into `upstream/`, applies the patch, installs dependencies, and runs the build and tests. The output is `dist/ChatGPT_Exporter_Personal.user.js`.

The [CI workflow](.github/workflows/sync-and-build.yml) checks upstream daily and only publishes a build when compilation and tests pass. Incompatible source changes stop the build instead of silently applying a broken patch.

See [development notes](docs/DEVELOPMENT.md), [test checklist](docs/TESTING.md), and [contribution guidelines](CONTRIBUTING.md).

## Notes

- Displayed times are fixed to `Asia/Shanghai` rather than your device's local time.
- The image-reference mode affects Markdown only; other export formats retain their upstream behavior.
- On long conversations, virtualized messages can affect where the first visible full date appears.
- Keep a copy of your existing scripts and settings before switching builds.

## License

MIT — see [LICENSE](LICENSE). ChatGPT Exporter is developed by [pionxzh](https://github.com/pionxzh); the original copyright notice is retained in the distributed userscript.
