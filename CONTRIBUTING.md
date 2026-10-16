# Contributing

ChatGPT Exporter Personal is a small patch layer over [pionxzh/chatgpt-exporter](https://github.com/pionxzh/chatgpt-exporter). Fixes and compatibility reports are welcome.

For upstream bugs that also occur without these patches, please report them to the original project. This repository is intended for differences introduced by the Beijing-time and Markdown reference-image features.

## Before opening a pull request

1. Reproduce the issue with the current userscript and identify whether it affects the upstream build too.
2. Keep changes confined to the patch layer when possible. Do not copy the entire upstream source into this repository.
3. Add or update a regression test for formatting, image references, or filenames.
4. Run the checks described in [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md). For export behavior, follow [docs/TESTING.md](docs/TESTING.md).
5. Avoid submitting real exported conversations, credentials, session tokens, or screenshots containing private information.

The patch application is deliberately strict: if an upstream anchor changes, review the new upstream code and update the patch explicitly rather than relaxing the check.

By contributing, you agree that your changes are distributed under the MIT License, while the original upstream copyright remains intact.
