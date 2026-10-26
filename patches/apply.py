#!/usr/bin/env python3
"""Fail-closed source patcher for pionxzh/chatgpt-exporter 2.37.x.
Runs against a clean checkout of upstream (not a prebuilt old userscript).
"""
from pathlib import Path
import json, sys

base=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path('upstream').resolve()
if not (base/'src/exporter/markdown.ts').is_file():
    raise SystemExit('Expected upstream repository checkout as first argument')
root=Path(__file__).resolve().parents[1]

def edit(rel, transforms):
    path=base/rel
    body=path.read_text(encoding='utf-8')
    for old,new in transforms:
        n=body.count(old)
        if n!=1:
            raise RuntimeError(f'Upstream mismatch in {rel}: expected 1 anchor, got {n}: {old[:100]!r}')
        body=body.replace(old,new)
    path.write_text(body,encoding='utf-8')
    print('patched',rel)

def patch(rel, old, new):edit(rel,[(old,new)])

personal=base/'src/personal'
personal.mkdir(exist_ok=True)
(personal/'beijing.ts').write_text((root/'patches/beijing.ts').read_text(encoding='utf-8'),encoding='utf-8')
(personal/'mdReferences.ts').write_text((root/'patches/mdReferences.ts').read_text(encoding='utf-8'),encoding='utf-8')

edit('src/utils/utils.ts', [
("export function noop() {}", "import { formatBeijing, formatBeijingFileTime } from '../personal/beijing'\n\nexport function noop() {}"),
("""export function dateStr(date: Date = new Date()) {
    const year = date.getFullYear()
    const month = String(date.getMonth() + 1).padStart(2, '0')
    const day = String(date.getDate()).padStart(2, '0')
    return `${year}-${month}-${day}`
}

export function timestamp() {
    return new Date().toISOString().replace(/:/g, '-').replace(/\\..+/, '')
}""", """export function dateStr(date: Date = new Date()) {
    return formatBeijing(date).slice(0, 10)
}

export function timestamp() {
    return formatBeijingFileTime(new Date())
}""")
])
edit('src/utils/download.ts', [
("import { dateStr, timestamp, unixTimestampToISOString } from './utils'", "import { dateStr, timestamp } from './utils'\nimport { formatBeijingFileTime } from '../personal/beijing'"),
("const _createTime = unixTimestampToISOString(createTime)\n    const _updateTime = unixTimestampToISOString(updateTime)", "const _createTime = formatBeijingFileTime(new Date(createTime * 1000))\n    const _updateTime = formatBeijingFileTime(new Date(updateTime * 1000))"),
("""const blob = content instanceof Blob ? content : new Blob([content], { type })""", """const blob = content instanceof Blob ? content : new Blob([typeof content === 'string' && /^text\/(?:plain|html|markdown)(?:;|$)/i.test(type) ? '\\uFEFF' : '', content], { type })"""),
("""a.download = filename\n    document.body.appendChild(a)\n    a.click()\n    document.body.removeChild(a)\n    setTimeout""", """a.download = sanitize(filename, { replacement: '-' })\n    document.body.appendChild(a)\n    a.click()\n    document.body.removeChild(a)\n    setTimeout"""),
("""    return format
        .replace('{title}', _title)""", """    return sanitize(format
        .replace('{title}', _title)"""),
("""        .concat(`.${ext}`)
}""", """        .concat(`.${ext}`), { replacement: '-' })
}""")
])
# Keep metadata timezone-aware ISO 8601, not the filename-safe representation.
edit('src/exporter/meta.ts', [
    ("import { dateStr, timestamp, unixTimestampToISOString } from '../utils/utils'", "import { dateStr, timestamp } from '../utils/utils'\nimport { formatBeijingAttribute } from '../personal/beijing'"),
    ("create_time: unixTimestampToISOString(createTime),", "create_time: createTime ? formatBeijingAttribute(new Date(createTime * 1000)) : '',"),
    ("update_time: unixTimestampToISOString(updateTime),", "update_time: updateTime ? formatBeijingAttribute(new Date(updateTime * 1000)) : '',")
])
edit('src/ui/SettingContext.tsx',[
("const defaultFormat = 'ChatGPT-{title}'", "export const defaultFormat = '{title}-{create_time}'"),
("const [format, setFormat] = useGMStorage(KEY_FILENAME_FORMAT, defaultFormat)", """const [storedFormat, setFormat] = useGMStorage(KEY_FILENAME_FORMAT, defaultFormat)
    // Only migrate the old upstream default; leave custom filename formats unchanged.
    const format = (storedFormat === 'ChatGPT-{title}' || storedFormat === '{title}-{update_time}') ? defaultFormat : storedFormat"""),
("""export type ImageMode = 'embed' | 'omit' | 'files'""", """export type ImageMode = 'embed' | 'omit' | 'files' | 'reference'"""),
("""export const defaultImageMode: ImageMode = 'embed'""", """export const defaultImageMode: ImageMode = 'reference'""")
])
patch('src/utils/imageFiles.ts', "return ScriptStorage.get<ImageMode>(KEY_IMAGE_MODE) ?? 'embed'", "return ScriptStorage.get<ImageMode>(KEY_IMAGE_MODE) ?? 'reference'")
# Keep the filename's conversation creation time accurate for single JSON-like exports.
# Upstream previously omitted timestamps, so a filename token fell back to download time.
edit('src/exporter/json.ts', [
    ("""        title: rawConversation.title || 'ChatGPT Conversation',
        chatId,
    })""", """        title: rawConversation.title || 'ChatGPT Conversation',
        chatId,
        createTime: rawConversation.create_time,
        updateTime: rawConversation.update_time,
    })"""),
    ("""getFileNameWithFormat(`${fileNameFormat}.tavern`, 'jsonl', { title: conversation.title, chatId })""",
     """getFileNameWithFormat(`${fileNameFormat}.tavern`, 'jsonl', { title: conversation.title, chatId, createTime: conversation.createTime, updateTime: conversation.updateTime })"""),
    ("""getFileNameWithFormat(`${fileNameFormat}.ooba`, 'json', { title: conversation.title, chatId })""",
     """getFileNameWithFormat(`${fileNameFormat}.ooba`, 'json', { title: conversation.title, chatId, createTime: conversation.createTime, updateTime: conversation.updateTime })"""),
])

edit('src/ui/SettingDialog.tsx', [
    ("import { timestamp as _timestamp, dateStr, unixTimestampToISOString } from '../utils/utils'", "import { timestamp as _timestamp, dateStr } from '../utils/utils'\nimport { formatBeijingAttribute } from '../personal/beijing'"),
    ("title={unixTimestampToISOString(createTime)}", "title={createTime ? formatBeijingAttribute(new Date(createTime * 1000)) : ''}"),
    ("title={unixTimestampToISOString(updateTime)}", "title={updateTime ? formatBeijingAttribute(new Date(updateTime * 1000)) : ''}")
])
patch('src/ui/SettingDialog.tsx', '<option value="embed">{t(\'Images Embed\')}</option>', '<option value="reference">单文件 Markdown（图片短引用，推荐）</option>\n                                    <option value="embed">{t(\'Images Embed\')}</option>')
edit('src/exporter/markdown.ts',[
("import JSZip from 'jszip'", "import JSZip from 'jszip'\nimport { formatBeijingAttribute, formatBeijingDateTime, getTimestampDisplayFormatter } from '../personal/beijing'\nimport { compactImageReferences } from '../personal/mdReferences'"),
("""const markdown = standardizeLineBreaks(conversationToMarkdown(conversation, metaList, imageMode))""", """const exportedMarkdown = standardizeLineBreaks(conversationToMarkdown(conversation, metaList, imageMode))
    const markdown = imageMode === 'reference' ? compactImageReferences(exportedMarkdown) : exportedMarkdown"""),
("""const content = conversationToMarkdown(conversation, metaList, imageMode)
        zip.file(fileName, content)""", """const content = conversationToMarkdown(conversation, metaList, imageMode)
        zip.file(fileName, imageMode === 'reference' ? compactImageReferences(content) : content)"""),
("""const content = conversationNodes.map(({ message, thinking }) => {""", """const formatTimestampDisplay = getTimestampDisplayFormatter(!timeStamp24H)
    const content = conversationNodes.map(({ message, thinking }) => {"""),
("""const conversationTime = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: !timeStamp24H })
            timestampHtml = `<time datetime="${date.toISOString()}" title="${date.toLocaleString()}">${conversationTime}</time>\\n\\n`""", """const conversationTime = formatTimestampDisplay(date)
            timestampHtml = `<time datetime="${formatBeijingAttribute(date)}" title="${formatBeijingDateTime(date, !timeStamp24H)}">${conversationTime}</time>\\n\\n`"""),
("""const markdown = `${frontMatter}# ${title}\\n\\n${content}`""", """const created = conversation.createTime ? `Created at ${formatBeijingDateTime(new Date(conversation.createTime * 1000))}\\n\\n` : ''
    const markdown = `${frontMatter}# ${title}\\n\\n${created}${content}`""")
])
edit('src/exporter/html.ts',[
("import JSZip from 'jszip'", "import JSZip from 'jszip'\nimport { formatBeijingAttribute, formatBeijingDateTime, getTimestampDisplayFormatter } from '../personal/beijing'"),
("""const conversationHtml = conversationNodes.map(({ message, thinking }) => {""", """const formatTimestampDisplay = getTimestampDisplayFormatter(!timeStamp24H)
    const conversationHtml = conversationNodes.map(({ message, thinking }) => {"""),
("""conversationTime = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: !timeStamp24H })
            timestampHtml = `<time class="time" datetime="${date.toISOString()}" title="${date.toLocaleString()}">${conversationTime}</time>`""", """conversationTime = formatTimestampDisplay(date)
            timestampHtml = `<time class="time" datetime="${formatBeijingAttribute(date)}" title="${formatBeijingDateTime(date, !timeStamp24H)}">${conversationTime}</time>`"""),
("""        title: escapeHtml(title),
        date,""", """        title: escapeHtml(title),
        create_time_display: conversation.createTime ? formatBeijingDateTime(new Date(conversation.createTime * 1000)) : '',
        date,""")
])
patch('src/template.html', '''<p>Exported by
                <a href="https://github.com/pionxzh/chatgpt-exporter.git">ChatGPT Exporter</a>
                at {{time}}</p>''', '''<p>Created at {{create_time_display}}</p>''')

edit('src/main.tsx',[
("import { render } from 'preact'", "import { render } from 'preact'\nimport { dateKey, formatBeijingAttribute, formatBeijingDateTime, formatBeijingTime } from './personal/beijing'"),
("""unit.append(createTimestamp(createTime))""", """unit.append(createTimestamp(createTime))
        refreshTimestampLabels()"""),
("""timestamp.dateTime = date.toISOString()
    timestamp.title = date.toLocaleString()""", """timestamp.dateTime = formatBeijingAttribute(date)
    timestamp.title = formatBeijingDateTime(date)
    timestamp.dataset.epoch = String(createTime)"""),
("""hour12.textContent = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })""", """hour12.textContent = formatBeijingTime(date, true)"""),
("""hour24.textContent = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: false })""", """hour24.textContent = formatBeijingTime(date, false)"""),
("""function getMenuContainer() {""", """/** Re-evaluate dates after virtualized message blocks mount. */
function refreshTimestampLabels() {
    let previous = ''
    for (const stamp of Array.from(document.querySelectorAll<HTMLElement>('time[data-ce-timestamp]'))) {
        const date = new Date(Number(stamp.dataset.epoch) * 1000)
        if (!Number.isFinite(date.getTime())) continue
        const key = dateKey(date)
        const firstOfDay = previous !== key
        previous = key
        for (const format of ['12', '24'] as const) {
            const text = stamp.querySelector<HTMLElement>(`[data-time-format="${format}"]`)
            if (text) text.textContent = (firstOfDay ? `${key} ` : '') + formatBeijingTime(date, format === '12')
        }
    }
}

function getMenuContainer() {""")
])

# Keep official coverage, adjust assertions to the intentional personal formats.
edit('tests/meta.test.ts', [
    ("create_time: '1970-01-01T00:00:01.000Z',", "create_time: '1970-01-01T08:00:01+08:00',"),
    (r"expect(variables.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}$/)",
     r"expect(variables.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$/)")
])
edit('tests/html-template.test.ts', [
    ("const names = ['title', 'date', 'time', 'source', 'lang', 'theme', 'avatar', 'details', 'content']",
     "const names = ['title', 'date', 'time', 'source', 'lang', 'theme', 'avatar', 'details', 'content', 'create_time_display']")
])
edit('tests/image-modes.test.ts', [
    ("""    it('embeds data uris by default', async () => {
        const zip = await exportZip([conversation('a', { upload: PNG })])
        expect(await zip.file('a.md')!.async('string')).toContain(`![image](${PNG})`)
    })""", """    it('uses compact single-file image references by default', async () => {
        const zip = await exportZip([conversation('a', { upload: PNG })])
        const markdown = await zip.file('a.md')!.async('string')
        expect(markdown).toContain('![image][img-001]')
        expect(markdown).toContain(`[img-001]: ${PNG}`)
    })

    it('still supports the original inline base64 image option', async () => {
        settings.imageMode = 'embed'
        const zip = await exportZip([conversation('a', { upload: PNG })])
        expect(await zip.file('a.md')!.async('string')).toContain(`![image](${PNG})`)
    })""")
])

# Regression: ISO metadata and Windows-safe filenames must remain independent.
(base/'tests/personal-filetime.test.ts').write_text("""import { describe, expect, it } from 'vitest'
import { unixTimestampToISOString } from '../src/utils/utils'
import { getFileNameWithFormat } from '../src/utils/download'
import { readFileSync } from 'node:fs'

describe('Personal date and filename compatibility', () => {
    it('defaults to conversation creation time, not last-update time', () => {
        const defaultFormat = '{title}-{create_time}'
        const source = readFileSync(new URL('../src/ui/SettingContext.tsx', import.meta.url), 'utf8')
        expect(source).toContain("export const defaultFormat = '{title}-{create_time}'")
        expect(source).toContain("storedFormat === 'ChatGPT-{title}' || storedFormat === '{title}-{update_time}'")
        expect(source).not.toContain('conversationNodes[index')
        const name = getFileNameWithFormat(defaultFormat, 'md', {
            title: 'example', createTime: 1, updateTime: 3661,
        })
        expect(name).toBe('example-1970-01-01_09-01-01.md')
    })
    it('preserves standard ISO timestamps used in metadata', () => {
        expect(unixTimestampToISOString(1)).toBe('1970-01-01T00:00:01.000Z')
        expect(unixTimestampToISOString(0)).toBe('')
    })
    it('uses Windows-safe local times only for filename substitutions', () => {
        const name = getFileNameWithFormat('{create_time}--{update_time}', 'md', {
            title: 'x', createTime: 1, updateTime: 1,
        })
        expect(name).toBe('1970-01-01_08-00-01--1970-01-01_08-00-01.md')
    })
})
""", encoding='utf-8')

# Package identity must not downgrade or impersonate the official GreasyFork script.
pkg=base/'package.json'
p=json.loads(pkg.read_text(encoding='utf-8'))
p['title']=p['title:zh-CN']=p['title:zh-TW']='ChatGPT Exporter Personal'
p['author']='ChatGPT Exporter Personal Community Fork'
p['description']='Upstream ChatGPT Exporter with optional Beijing timestamps and single-file Markdown image references'
p['description:zh-CN']='基于官方版；保留北京时间、创建时间和 Markdown 单文件图片短引用等定制'
p['description:zh-TW']=p['description:zh-CN']
pkg.write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Source patches OK; official tests & pnpm build must still pass.')
