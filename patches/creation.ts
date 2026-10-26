/** Interpret ChatGPT conversation timestamps without ever substituting the export time. */
export type TimeValue = number | string | null | undefined

export function toUnixSeconds(value: TimeValue): number {
    if (value == null || value === '') return 0
    if (typeof value === 'number' || /^\d+(?:\.\d+)?$/.test(value.trim())) {
        const n = Number(value)
        if (!Number.isFinite(n) || n <= 0) return 0
        return n > 1e11 ? n / 1000 : n
    }
    const millis = Date.parse(value)
    return Number.isFinite(millis) && millis > 0 ? millis / 1000 : 0
}

export interface ConversationWithTimes {
    create_time?: TimeValue
    update_time?: TimeValue
    mapping?: Record<string, {
        message?: {
            create_time?: TimeValue
            author?: { role?: string }
        }
    }>
}

export function conversationCreateTime(conversation: ConversationWithTimes): number {
    const direct = toUnixSeconds(conversation.create_time)
    if (direct) return direct

    // Older/shared API results can omit the conversation-level field.
    // A user's first message is the best available creation-time surrogate.
    const messages = Object.values(conversation.mapping ?? {})
        .map(node => node.message)
        .filter(message => message && (message.author?.role === 'user' || message.author?.role === 'assistant'))
    const firstUser = messages.filter(m => m?.author?.role === 'user')
        .map(m => toUnixSeconds(m?.create_time))
        .filter(Boolean)
    if (firstUser.length) return Math.min(...firstUser)
    const times = messages.map(m => toUnixSeconds(m?.create_time)).filter(Boolean)
    return times.length ? Math.min(...times) : 0
}

export function conversationUpdateTime(conversation: ConversationWithTimes): number {
    return toUnixSeconds(conversation.update_time) || conversationCreateTime(conversation)
}
