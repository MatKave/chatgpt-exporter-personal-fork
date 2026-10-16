# Development

This project follows upstream releases through a small source overlay. It does not maintain a forked copy of the entire ChatGPT Exporter codebase.

## Repository layout

```text
.
├── patches/
│   ├── apply.py           # apply checked source/test replacements to upstream
│   ├── beijing.ts         # timezone and timestamp formatting
│   ├── mdReferences.ts    # Markdown image reference conversion
│   └── finalize.py        # userscript metadata and license notice
├── tests/
│   └── features.test.mjs  # standalone tests for personal features
├── docs/
├── dist/
│   └── ChatGPT_Exporter_Personal.user.js
├── Build.cmd / Build.ps1  # Windows build
└── .github/workflows/
    └── sync-and-build.yml
```

`upstream/` is a local checkout created during the build and ignored by Git.

## Build pipeline

```text
pionxzh/chatgpt-exporter (master)
             │
             ▼
     patches/apply.py
             │
             ├── source changes (timestamp, image mode, export layout)
             └── adjusted upstream tests and filename regression tests
             │
             ▼
       pnpm build / test
             │
             ├── tests/features.test.mjs
             ▼
     patches/finalize.py
             │
             ▼
      validated .user.js
```

`apply.py` uses exact, single-occurrence string anchors. An upstream change that removes or duplicates an anchor fails the build. This is intentional: the script should not guess how to patch changed upstream code.

`mdReferences.ts` converts `data:image/*;base64,` image links in Markdown into reference definitions. Existing reference IDs are reserved before allocating `img-001`, `img-002`, etc. Non-data image URLs are left alone. The image fetching and cache behavior is upstream's.

`beijing.ts` formats display timestamps in `Asia/Shanghai`. Metadata uses offset-aware ISO-8601 strings; filename substitutions use colon-free timestamps.

## Continuous integration

The workflow runs on pull requests, matching changes to the main branch, manual dispatch, and a daily schedule.

The build job checks out upstream with read-only permissions, applies the patch, runs the upstream TypeScript/Vitest suite, and checks the personal features. If validation succeeds, the publish job retrieves the tested artifact and commits it to `dist/`. The publish job alone has repository write permissions.

A source fingerprint avoids rebuilding when upstream and patch inputs are unchanged. Failed runs do not replace the last successful userscript.

Public repository builds include `@updateURL` and `@downloadURL` for the raw userscript in `dist/`. Private builds intentionally omit them. CI tests the generated JavaScript but cannot exercise a real ChatGPT session; test installation and exports in Tampermonkey before relying on an update.

## Local builds

For Windows, run `Build.cmd`. The PowerShell runner reuses an existing upstream checkout and checks for partial patches before continuing. Unlike CI, it does **not** update an existing upstream checkout automatically. For a clean upstream sync, use the GitHub workflow or start with a clean upstream checkout.

Linux/macOS development can use a fresh checkout of upstream:

```sh
git clone https://github.com/pionxzh/chatgpt-exporter.git upstream
corepack enable
python3 patches/apply.py upstream
cd upstream
corepack pnpm install --frozen-lockfile
corepack pnpm build
corepack pnpm test
cd ..
node --experimental-strip-types tests/features.test.mjs
python3 patches/finalize.py upstream/dist/chatgpt.user.js dist/ChatGPT_Exporter_Personal.user.js --revision 1
node --check dist/ChatGPT_Exporter_Personal.user.js
```

## Updating the patch

Keep the patch narrowly scoped to behavior not covered by upstream. Before replacing an anchor, inspect the current upstream implementation and update tests for the intended behavior. Review the produced userscript header and test a real image-containing conversation according to [TESTING.md](TESTING.md). Do not add conversation exports or credentials to test fixtures.

This is an independent build of an MIT-licensed upstream project; retain its copyright notice when distributing.
