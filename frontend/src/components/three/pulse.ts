import type { Priority } from '../../api/client'

type Listener = (priority: Priority) => void
const listeners = new Set<Listener>()

/** Tell the city backdrop that a complaint was triaged, so it can send out a pulse. */
export function emitPulse(priority: Priority): void {
  for (const listener of listeners) listener(priority)
}

export function onPulse(listener: Listener): () => void {
  listeners.add(listener)
  return () => { listeners.delete(listener) }
}
