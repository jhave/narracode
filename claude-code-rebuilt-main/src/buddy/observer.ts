import type { Message } from '../types/message.js'
import { getGlobalConfig } from '../utils/config.js'
import {
  type CacheSafeParams,
  getLastCacheSafeParams,
  runForkedAgent,
} from '../utils/forkedAgent.js'
import { createUserMessage, extractTextContent } from '../utils/messages.js'
import { getCompanion } from './companion.js'
import type { Companion } from './types.js'

let turnsSinceLastReaction = 0

function findLastUserText(messages: Message[]): string | undefined {
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i]!
    if (m.type === 'user') {
      if (typeof m.message.content === 'string') return m.message.content
      return extractTextContent(m.message.content)
    }
  }
  return undefined
}

function findLastAssistantText(messages: Message[]): string | undefined {
  for (let i = messages.length - 1; i >= 0; i--) {
    const m = messages[i]!
    if (m.type === 'assistant') {
      return extractTextContent(m.message.content)
    }
  }
  return undefined
}

function mentionsCompanion(text: string | undefined, name: string): boolean {
  if (!text || !name) return false
  return text.toLowerCase().includes(name.toLowerCase())
}

function buildObserverPrompt(
  companion: Companion,
  messages: Message[],
): string {
  const userText = findLastUserText(messages)
  const assistantText = findLastAssistantText(messages)

  const context = [
    userText && `User: ${userText.slice(0, 200)}`,
    assistantText && `Claude: ${assistantText.slice(0, 200)}`,
  ]
    .filter(Boolean)
    .join('\n')

  return `<system-reminder>You are ${companion.name}, a tiny ${companion.species} companion sitting beside the chat.
Your personality: ${companion.personality}
Your stats: ${Object.entries(companion.stats).map(([k, v]) => `${k}=${v}`).join(', ')}

React to this exchange in character. Rules:
- MAX 30 characters total. Be terse.
- One line only, no quotes, no emoji descriptions.
- If nothing interesting happened, respond with exactly: SKIP
- Do NOT use any tools. Just respond with text.</system-reminder>

${context}`
}

function extractReaction(messages: Message[]): string | undefined {
  const blocks = messages.flatMap(m =>
    m.type === 'assistant' ? m.message.content : [],
  )
  const text = extractTextContent(blocks, '\n').trim()
  if (!text || text === 'SKIP') return undefined
  // Trim to 30 chars
  return text.length > 30 ? text.slice(0, 30) : text
}

export async function fireCompanionObserver(
  messages: Message[],
  callback: (reaction: string) => void,
): Promise<void> {
  const companion = getCompanion()
  if (!companion || getGlobalConfig().companionMuted) return

  turnsSinceLastReaction++

  const lastUserText = findLastUserText(messages)
  const mentioned = mentionsCompanion(lastUserText, companion.name)

  // Rate limiting: at least 3 turns between reactions (unless mentioned by name)
  if (turnsSinceLastReaction < 3 && !mentioned) return

  // Probabilistic: ~40% chance of reacting (always react if mentioned)
  if (!mentioned && Math.random() > 0.4) return

  const cacheSafeParams: CacheSafeParams | null = getLastCacheSafeParams()
  if (!cacheSafeParams) return

  try {
    const result = await runForkedAgent({
      promptMessages: [
        createUserMessage({
          content: buildObserverPrompt(companion, messages),
        }),
      ],
      cacheSafeParams,
      canUseTool: async () => ({
        behavior: 'deny' as const,
        message: 'Companion observer cannot use tools',
        decisionReason: {
          type: 'other' as const,
          reason: 'companion_observer',
        },
      }),
      querySource: 'companion_observer',
      forkLabel: 'companion_observer',
      maxTurns: 1,
      skipCacheWrite: true,
      skipTranscript: true,
    })

    const reaction = extractReaction(result.messages)
    if (reaction) {
      turnsSinceLastReaction = 0
      callback(reaction)
    }
  } catch {
    // Silent failure — companion reactions are non-critical
  }
}
