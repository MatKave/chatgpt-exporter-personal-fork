# Testing

The CI workflow covers compilation, upstream automated tests, and formatting/reference helpers. A live ChatGPT session is still needed to check export compatibility with the current website.

## Automated checks

- Upstream: `pnpm build` followed by `pnpm test` (TypeScript and Vitest).
- Personal features: `node --experimental-strip-types tests/features.test.mjs`.
- Final userscript: `node --check dist/ChatGPT_Exporter_Personal.user.js`.

The source patch also adds tests for timezone-aware metadata and filename substitutions. An incompatible upstream source anchor fails before any release is published.

## Browser smoke test

Use synthetic or non-sensitive conversations. Do not upload private chat exports to issues.

| Case | Check |
| --- | --- |
| Reference images | Export one chat with multiple images, including a repeated image. Verify short IDs, definitions at the end, and no duplicate image data. |
| Existing Markdown references | Include a literal `[img-001]` link in the original message. Its original target must not be changed by generated image references. |
| Other image modes | Check Embed, Files (ZIP with `assets/`), and Omit still work. |
| Batch Markdown | Export at least two chats. Each Markdown file in the ZIP must resolve its own image references. |
| Timestamps | Compare messages around midnight in Beijing, in 12-hour and 24-hour modes, on the page and in Markdown/HTML. |
| Metadata and filenames | Test `{create_time}` and `{update_time}` filename variables, ISO metadata with `+08:00`, and filenames containing Windows-invalid characters. |
| Other formats | Check HTML, JSON, Copy Text, and screenshot on a chat with formulas, code blocks, attachments, and citations. |
| Script coexistence | Disable the original exporter while using this build; check saved settings and menu duplication. |

Some Markdown readers reject `data:` reference definitions. If images do not render, try another reader or use upstream's Embed or Files mode. This alone is not evidence that the Base64 payload is missing.

## Reporting bugs

Include the userscript version, browser/Tampermonkey versions, export format, image mode, and reproducible steps. Share a small **sanitized** input/output example when possible. Never include access tokens, session cookies, or actual private conversations.
