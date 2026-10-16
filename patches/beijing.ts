/** Beijing-time formatting for conversation timestamps and exports. */
const TZ = 'Asia/Shanghai'
const df = new Intl.DateTimeFormat('sv-SE', {
    timeZone: TZ,
    year: 'numeric', month: '2-digit', day: '2-digit',
    hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false,
})
export function formatBeijing(date: Date) {
    const parts = Object.fromEntries(df.formatToParts(date).filter(p => p.type !== 'literal').map(p => [p.type, p.value]))
    return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second}`
}
export function dateKey(date: Date) { return formatBeijing(date).slice(0, 10) }
export function formatBeijingFileTime(date: Date) { return formatBeijing(date).replace(' ', '_').replace(/:/g, '-') }
export function formatBeijingAttribute(date: Date) { return formatBeijing(date).replace(' ', 'T') + '+08:00' }
export function formatBeijingTime(date: Date, hour12 = false) {
    if (hour12) return date.toLocaleTimeString('en-US', { timeZone: TZ, hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true })
    return formatBeijing(date).slice(11)
}
export function formatBeijingDateTime(date: Date, hour12 = false) {
    return dateKey(date) + ' ' + formatBeijingTime(date, hour12)
}
export function getTimestampDisplayFormatter(hour12 = false) {
    let previous = ''
    return (date: Date) => {
        const current = dateKey(date)
        const full = current !== previous
        previous = current
        return full ? formatBeijingDateTime(date, hour12) : formatBeijingTime(date, hour12)
    }
}
