import * as React from 'react'
import { useEffect, useState } from 'react'
import { useInterval } from 'usehooks-ts'
import { SpinnerGlyph } from '../../components/Spinner/SpinnerGlyph.js'
import { Box, Text } from '../../ink.js'
import { useSetAppState } from '../../state/AppState.js'
import type {
  LocalJSXCommandCall,
  LocalJSXCommandOnDone,
} from '../../types/command.js'
import {
  getCompanion,
  companionUserId,
  roll,
} from '../../buddy/companion.js'
import { renderSprite, renderFace } from '../../buddy/sprites.js'
import {
  RARITY_STARS,
  RARITY_COLORS,
  STAT_NAMES,
  type Companion,
  type CompanionBones,
} from '../../buddy/types.js'
import { saveGlobalConfig, getGlobalConfig } from '../../utils/config.js'
import {
  getLastCacheSafeParams,
  runForkedAgent,
} from '../../utils/forkedAgent.js'
import {
  createUserMessage,
  extractTextContent,
} from '../../utils/messages.js'

// ── Soul generation via forked agent ────────────────────────────

function buildHatchPrompt(
  bones: CompanionBones,
  inspirationSeed: number,
): string {
  const statsStr = Object.entries(bones.stats)
    .map(([k, v]) => `${k}: ${v}`)
    .join(', ')

  return `<system-reminder>You are a naming engine for a virtual companion creature. Generate a name and personality for this companion.

Species: ${bones.species}
Rarity: ${bones.rarity}
Eye style: ${bones.eye}
Hat: ${bones.hat}
Shiny: ${bones.shiny}
Stats: ${statsStr}
Inspiration seed: ${inspirationSeed}

Rules:
- Name: 1-2 words, max 15 characters, creative and fitting the species
- Personality: one sentence, max 60 characters, reflects the stats
- High CHAOS → unpredictable; High SNARK → sarcastic; High WISDOM → thoughtful
- High PATIENCE → calm; High DEBUGGING → detail-oriented

Respond with ONLY valid JSON, no markdown fences:
{"name": "...", "personality": "..."}</system-reminder>`
}

function parseSoulResponse(
  messages: Array<{ type: string; message?: { content: unknown[] } }>,
): { name: string; personality: string } | null {
  const blocks = messages.flatMap(m =>
    m.type === 'assistant' && m.message ? m.message.content : [],
  )
  let text = extractTextContent(blocks as { type: string }[], '\n').trim()
  if (!text) return null

  // Strip markdown code fences if present
  text = text.replace(/^```(?:json)?\s*/i, '').replace(/\s*```\s*$/, '')

  try {
    const parsed = JSON.parse(text)
    if (
      typeof parsed.name === 'string' &&
      typeof parsed.personality === 'string'
    ) {
      return {
        name: parsed.name.slice(0, 15),
        personality: parsed.personality.slice(0, 60),
      }
    }
  } catch {
    // Regex fallback
    const nameMatch = text.match(/"name"\s*:\s*"([^"]+)"/)
    const persMatch = text.match(/"personality"\s*:\s*"([^"]+)"/)
    if (nameMatch?.[1] && persMatch?.[1]) {
      return {
        name: nameMatch[1].slice(0, 15),
        personality: persMatch[1].slice(0, 60),
      }
    }
  }
  return null
}

async function generateSoul(
  bones: CompanionBones,
  inspirationSeed: number,
): Promise<{ name: string; personality: string }> {
  const cacheSafeParams = getLastCacheSafeParams()
  if (!cacheSafeParams) {
    // Fallback if no prior query — use a deterministic name
    return {
      name: `${bones.species.charAt(0).toUpperCase()}${bones.species.slice(1)}`,
      personality: 'A mysterious companion.',
    }
  }

  const result = await runForkedAgent({
    promptMessages: [
      createUserMessage({
        content: buildHatchPrompt(bones, inspirationSeed),
      }),
    ],
    cacheSafeParams,
    canUseTool: async () => ({
      behavior: 'deny' as const,
      message: 'Soul generation cannot use tools',
      decisionReason: { type: 'other' as const, reason: 'buddy_hatch' },
    }),
    querySource: 'buddy_hatch',
    forkLabel: 'buddy_hatch',
    maxTurns: 1,
    skipCacheWrite: true,
    skipTranscript: true,
  })

  return (
    parseSoulResponse(result.messages) ?? {
      name: `${bones.species.charAt(0).toUpperCase()}${bones.species.slice(1)}`,
      personality: 'A mysterious companion.',
    }
  )
}

// ── Stat bar rendering ──────────────────────────────────────────

function StatBar({
  name,
  value,
  color,
}: {
  name: string
  value: number
  color: string
}) {
  const barWidth = 15
  const filled = Math.round((value / 100) * barWidth)
  const bar = '\u2588'.repeat(filled) + '\u2591'.repeat(barWidth - filled)
  const label = name.padEnd(9)
  const numStr = String(value).padStart(3)
  return (
    <Text>
      {'  '}
      <Text dimColor>{label}</Text>{' '}
      <Text color={color}>{bar}</Text>{' '}
      <Text bold>{numStr}</Text>
    </Text>
  )
}

// ── Companion card ──────────────────────────────────────────────

function CompanionCard({
  companion,
  onDone,
}: {
  companion: Companion
  onDone: LocalJSXCommandOnDone
}) {
  const color = RARITY_COLORS[companion.rarity]
  const stars = RARITY_STARS[companion.rarity]
  const sprite = renderSprite(companion, 0)
  const face = renderFace(companion)

  const handleKeyDown = React.useCallback(
    (e: { key: string; ctrl?: boolean; preventDefault: () => void }) => {
      if (
        e.key === 'escape' ||
        e.key === 'return' ||
        (e.ctrl && (e.key === 'c' || e.key === 'd'))
      ) {
        e.preventDefault()
        onDone(undefined, { display: 'skip' })
      }
    },
    [onDone],
  )

  return (
    <Box
      flexDirection="column"
      paddingX={1}
      paddingY={1}
      tabIndex={0}
      autoFocus={true}
      onKeyDown={handleKeyDown}
    >
      <Text bold color={color}>
        {stars} {companion.rarity}{companion.shiny ? ' \u2728' : ''}
      </Text>
      <Text> </Text>
      {sprite.map((line, i) => (
        <Text key={i} color={color}>
          {'  '}{line}
        </Text>
      ))}
      <Text> </Text>
      <Text bold>
        {'  '}{face} "{companion.name}" the {companion.species}
      </Text>
      <Text italic dimColor>
        {'  '}{companion.personality}
      </Text>
      <Text> </Text>
      {STAT_NAMES.map(stat => (
        <StatBar
          key={stat}
          name={stat}
          value={companion.stats[stat]}
          color={color}
        />
      ))}
      <Text> </Text>
      <Text dimColor>
        {'  '}Press Escape to close. Try /buddy pet!
      </Text>
    </Box>
  )
}

// ── Hatching animation ──────────────────────────────────────────

const HATCH_FRAMES = [
  '    ___   \n   /   \\  \n  |     | \n  |     | \n   \\___/  ',
  '    ___   \n   / . \\  \n  |     | \n  |     | \n   \\___/  ',
  '   _/\\_   \n  / .  \\  \n |      | \n |      | \n  \\____/  ',
  '  _/ \\_   \n /  .  \\  \n|   *   | \n \\     /  \n  \\___/   ',
  ' *       *\n  _/ \\_   \n /     \\  \n|  !!!  | \n  \\   /   ',
]

function HatchingView({
  bones,
  inspirationSeed,
  onHatched,
}: {
  bones: CompanionBones
  inspirationSeed: number
  onHatched: (companion: Companion) => void
}) {
  const [frame, setFrame] = useState(0)
  const [generating, setGenerating] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useInterval(
    () => setFrame(f => f + 1),
    generating && frame < HATCH_FRAMES.length - 1 ? 400 : null,
  )

  useEffect(() => {
    let cancelled = false
    setGenerating(true)

    void generateSoul(bones, inspirationSeed).then(
      soul => {
        if (cancelled) return
        const stored = {
          name: soul.name,
          personality: soul.personality,
          hatchedAt: Date.now(),
        }
        saveGlobalConfig(cfg => ({ ...cfg, companion: stored }))
        // Re-read to merge bones + soul
        const companion = getCompanion()
        if (companion) {
          onHatched(companion)
        }
      },
      err => {
        if (cancelled) return
        setError(err instanceof Error ? err.message : String(err))
      },
    )

    return () => {
      cancelled = true
    }
  }, [])

  const color = RARITY_COLORS[bones.rarity]
  const eggFrame = HATCH_FRAMES[Math.min(frame, HATCH_FRAMES.length - 1)]!

  if (error) {
    return (
      <Box flexDirection="column" paddingX={1}>
        <Text color="red">Hatching failed: {error}</Text>
        <Text dimColor>Press Escape to close.</Text>
      </Box>
    )
  }

  return (
    <Box flexDirection="column" paddingX={1} paddingY={1}>
      <Box>
        <SpinnerGlyph />
        <Text bold color={color}>
          {' '}Hatching your companion...
        </Text>
      </Box>
      <Text> </Text>
      {eggFrame.split('\n').map((line, i) => (
        <Text key={i} color={color}>
          {line}
        </Text>
      ))}
    </Box>
  )
}

// ── Main command component ──────────────────────────────────────

function BuddyMain({
  onDone,
}: {
  onDone: LocalJSXCommandOnDone
}) {
  const [companion, setCompanion] = useState<Companion | undefined>(
    getCompanion,
  )
  const [hatching, setHatching] = useState(!companion)

  if (hatching && !companion) {
    const userId = companionUserId()
    const { bones, inspirationSeed } = roll(userId)
    return (
      <HatchingView
        bones={bones}
        inspirationSeed={inspirationSeed}
        onHatched={c => {
          setCompanion(c)
          setHatching(false)
        }}
      />
    )
  }

  if (!companion) {
    onDone(undefined, { display: 'skip' })
    return null
  }

  return <CompanionCard companion={companion} onDone={onDone} />
}

function BuddyPet({ onDone }: { onDone: LocalJSXCommandOnDone }) {
  const setAppState = useSetAppState()
  useEffect(() => {
    setAppState(prev => ({ ...prev, companionPetAt: Date.now() }))
    const companion = getCompanion()
    onDone(
      companion ? `You pet ${companion.name}!` : 'No companion to pet.',
      { display: 'system' },
    )
  }, [])
  return null
}

function BuddyMute({
  onDone,
  mute,
}: {
  onDone: LocalJSXCommandOnDone
  mute: boolean
}) {
  useEffect(() => {
    saveGlobalConfig(cfg => ({ ...cfg, companionMuted: mute }))
    onDone(mute ? 'Companion muted.' : 'Companion unmuted.', {
      display: 'system',
    })
  }, [])
  return null
}

function BuddyRename({ onDone }: { onDone: LocalJSXCommandOnDone }) {
  const [companion, setCompanion] = useState<Companion | undefined>(
    getCompanion,
  )
  const [renaming, setRenaming] = useState(true)

  useEffect(() => {
    if (!companion) {
      onDone('No companion to rename. Use /buddy first.', {
        display: 'system',
      })
      return
    }

    let cancelled = false
    const { bones, inspirationSeed } = roll(companionUserId())

    void generateSoul(bones, inspirationSeed + Date.now()).then(
      soul => {
        if (cancelled) return
        saveGlobalConfig(cfg => ({
          ...cfg,
          companion: {
            ...(cfg.companion ?? { hatchedAt: Date.now() }),
            name: soul.name,
            personality: soul.personality,
          },
        }))
        const updated = getCompanion()
        if (updated) setCompanion(updated)
        setRenaming(false)
      },
      () => {
        if (cancelled) return
        onDone('Rename failed. Try again.', { display: 'system' })
      },
    )

    return () => {
      cancelled = true
    }
  }, [])

  if (renaming) {
    return (
      <Box paddingX={1}>
        <SpinnerGlyph />
        <Text> Renaming companion...</Text>
      </Box>
    )
  }

  if (!companion) return null
  return <CompanionCard companion={companion} onDone={onDone} />
}

// ── Entry point ─────────────────────────────────────────────────

export const call: LocalJSXCommandCall = async (onDone, _context, args) => {
  const subcommand = args.trim().toLowerCase()

  switch (subcommand) {
    case 'pet':
      return <BuddyPet onDone={onDone} />
    case 'mute':
      return <BuddyMute onDone={onDone} mute={true} />
    case 'unmute':
      return <BuddyMute onDone={onDone} mute={false} />
    case 'rename':
      return <BuddyRename onDone={onDone} />
    default:
      return <BuddyMain onDone={onDone} />
  }
}
