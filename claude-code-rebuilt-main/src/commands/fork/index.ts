import type { Command } from '../../commands.js'
import { buildChildMessage } from '../../tools/AgentTool/forkSubagent.js'
import { isCoordinatorMode } from '../../coordinator/coordinatorMode.js'
import { getIsNonInteractiveSession } from '../../bootstrap/state.js'

const fork = {
  type: 'prompt',
  name: 'fork',
  description: 'Fork a background worker with a directive',
  argumentHint: '<directive>',
  context: 'fork',
  progressMessage: 'forking...',
  contentLength: 0,
  source: 'builtin',
  isEnabled: () => !isCoordinatorMode() && !getIsNonInteractiveSession(),
  async getPromptForCommand(args) {
    const directive = args?.trim()
    if (!directive) {
      throw new Error(
        'Usage: /fork <directive>\nProvide a directive for the forked worker.',
      )
    }
    return [{ type: 'text', text: buildChildMessage(directive) }]
  },
} satisfies Command

export default fork
