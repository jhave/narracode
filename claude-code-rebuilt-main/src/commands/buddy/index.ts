import type { Command } from '../../commands.js'

const buddy = {
  type: 'local-jsx',
  name: 'buddy',
  description: 'Meet your coding companion',
  immediate: true,
  isHidden: false,
  load: () => import('./buddy.js'),
} satisfies Command

export default buddy
