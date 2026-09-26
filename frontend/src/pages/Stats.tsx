import { useEffect, useState } from 'react'
import { getStats, type Stats as StatsData } from '../api/client'

type Snapshot = { stats: StatsData; cache: 'HIT' | 'MISS' | null }

export default function Stats() {
  const [snapshot, setSnapshot] = useState<Snapshot | null>(null)
  const [loading, setLoading] = useState(true)
  const [failure, setFailure] = useState('')

  useEffect(() => {
    let active = true
    getStats()
      .then((result) => { if (active) setSnapshot(result) })
      .catch((error: unknown) => {
        if (active) setFailure(error instanceof Error ? error.message : 'Could not load statistics.')
      })
      .finally(() => { if (active) setLoading(false) })
    return () => { active = false }
  }, [])

  return (
    <section aria-labelledby="stats-heading">
      <h2 id="stats-heading">Community statistics</h2>
      {loading && <p role="status">Loading statistics…</p>}
      {failure && <p role="alert">{failure}</p>}
      {snapshot && (
        <>
          <p>Total complaints: <strong>{snapshot.stats.total}</strong></p>
          <p>Cache: <strong>{snapshot.cache ?? 'Unknown'}</strong></p>
          <div className="stat-grid">
            <section>
              <h3>By category</h3>
              <dl>{Object.entries(snapshot.stats.by_category).map(([name, count]) => (
                <div key={name}><dt>{name}</dt><dd>{count}</dd></div>
              ))}</dl>
            </section>
            <section>
              <h3>By priority</h3>
              <dl>{Object.entries(snapshot.stats.by_priority).map(([name, count]) => (
                <div key={name}><dt>{name}</dt><dd>{count}</dd></div>
              ))}</dl>
            </section>
          </div>
        </>
      )}
    </section>
  )
}
