/** Single-file Markdown: short inline refs, Base64 resource definitions at end.
 * No remote request, no changes to author text/citations/other exports.
 * Source Markdown remains readable; compatible reader required for data: URLs.
 */
export function compactImageReferences(markdown: string): string {
    const fences: Array<[number, number]> = []
    const lines = /^ {0,3}(`{3,}|~{3,})[^\r\n]*(?:\r?\n|$)/gm
    let open: { start: number, ch: string, len: number } | null = null
    let m: RegExpExecArray | null
    while ((m = lines.exec(markdown))) {
        const marker = m[1]
        if (!open) open = { start: m.index, ch: marker[0], len: marker.length }
        else if (marker[0] === open.ch && marker.length >= open.len && !m[0].slice(m[0].indexOf(marker) + marker.length).trim()) {
            fences.push([open.start, lines.lastIndex])
            open = null
        }
    }
    if (open) fences.push([open.start, markdown.length])
    const refs = new Map<string, string>()
    // Existing user-authored reference labels must not be rebound to images.
    // Reserve both definitions and usages, case-insensitively.
    const usedLabels = new Set(Array.from(markdown.matchAll(/\[img-\d+\]/gi), match => match[0].slice(1, -1).toLowerCase()))
    let nextImageNumber = 1
    const definitions: string[] = []
    // Only data: images, not general URLs. Does not alter code fences or external sources.
    const image = /(!\[[^\]\r\n]*\])\((<?)(data:image\/[a-z0-9.+-]+;base64,[a-z0-9+\/_=-]+)(>?)\)/gi
    const output = markdown.replace(image, (whole, alt: string, openBracket: string, src: string, closeBracket: string, offset: number) => {
        if (fences.some(([start, end]) => offset >= start && offset < end)) return whole
        // Protect inline code spans (`image syntax`) without touching fenced code.
        const currentLine = markdown.slice(markdown.lastIndexOf('\n', offset - 1) + 1, offset)
        const ticks = Array.from(currentLine.matchAll(/(^|[^\\])(`+)/g))
        if (ticks.length % 2 === 1) return whole
        if (openBracket && closeBracket !== '>' || !openBracket && closeBracket) return whole
        let id = refs.get(src)
        if (!id) {
            do {
                id = `img-${String(nextImageNumber++).padStart(3, '0')}`
            } while (usedLabels.has(id))
            usedLabels.add(id)
            refs.set(src, id)
            definitions.push(`[${id}]: ${src}`)
        }
        return `${alt}[${id}]`
    })
    return definitions.length ? output + '\n\n' + definitions.join('\n\n') + '\n' : markdown
}
