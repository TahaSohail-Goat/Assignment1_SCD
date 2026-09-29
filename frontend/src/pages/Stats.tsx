import { lazy, Suspense, useContext, useEffect, useState } from 'react'
import { motion } from 'motion/react'
import { getStats, type Stats as StatsData } from '../api/client'
import CountUp from '../components/CountUp'
import ErrorBoundary from '../components/ErrorBoundary'
import { canRender3D } from '../components/three/capabilities'
import { categoryColor, priorityColor, ThemeContext } from '../theme'

const StatsChart3D = lazy(() => import('../components/three/StatsChart3D'))

type Snapshot = { stats: StatsData; cache: 'HIT' | 'MISS' | null }
type Dimension = 'category' | 'priority'

const fallbackColor = '#8fa3b8'
function colorFor(dimension: Dimension, name: string): string {
  const palette: Record<string, string> = dimension === 'category' ? categoryColor : priorityColor
  return palette[name] ?? fallbackColor
}

function Breakdown({ title, dimension, counts }: {
  title: string
  dimension: Dimension
  counts: Record<string, number>
}) {
  const entries = Object.entries(counts)
  const max = Math.max(1, ...entries.map(([, count]) => count))
  return (
    <section className="breakdown">
      <h3>{title}</h3>
      <dl>{entries.map(([name, count], index) => (
        <div key={name}>
          <dt><span className="swatch" style={{ background: colorFor(dimension, name) }} aria-hidden="true" />{name}</dt>
          <dd>{count}<motion.span className="stat-bar" aria-hidden="true"
            style={{ background: colorFor(dimension, name) }}
            initial={{ scaleX: 0 }} animate={{ scaleX: count / max }}
            transition={{ delay: 0.15 + index * 0.06, type: 'spring', stiffness: 110, damping: 20 }} /></dd>
        </div>
      ))}</dl>
    </section>
  )
}

export default function Stats() {
  const theme = useContext(ThemeContext)
  const [rich] = useState(canRender3D)
  const [dimension, setDimension] = useState<Dimension>('category')
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

  const chartCounts = snapshot
    ? (dimension === 'category' ? snapshot.stats.by_category : snapshot.stats.by_priority)
    : {}
  const chartData = Object.entries(chartCounts).map(([name, value]) => (
    { name, value, color: colorFor(dimension, name) }
  ))

  return (
    <section aria-labelledby="stats-heading" className="panel">
      <h2 id="stats-heading">Community statistics</h2>
      {loading && (
        <div className="loading-block">
          <p role="status" className="muted">Loading statistics…</p>
          <div className="skeleton-tiles" aria-hidden="true"><span /><span /></div>
        </div>
      )}
      {failure && <p role="alert" className="banner-error">{failure}</p>}
      {snapshot && (
        <>
          <div className="tiles">
            <motion.div className="tile" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
              <p>Total complaints: <strong className="tile-number"><CountUp value={snapshot.stats.total} /></strong></p>
            </motion.div>
            <motion.div className="tile" initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.08 }}>
              <p>Cache: <motion.strong key={snapshot.cache ?? 'none'}
                className={`cache-badge cache-${(snapshot.cache ?? 'unknown').toLowerCase()}`}
                initial={{ scale: 0.6, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}
                transition={{ type: 'spring', stiffness: 380, damping: 16, delay: 0.2 }}>
                {snapshot.cache ?? 'Unknown'}
              </motion.strong></p>
              <p className="tile-note">Stats are cached for 30 seconds and cleared on every write.</p>
            </motion.div>
          </div>

          {rich && chartData.length > 0 && (
            <div className="chart-card">
              <div className="chart-toolbar">
                <h3>At a glance</h3>
                <div className="segmented" role="group" aria-label="Chart grouping">
                  {(['category', 'priority'] as const).map((option) => (
                    <button key={option} type="button" aria-pressed={dimension === option}
                      onClick={() => setDimension(option)}>
                      {dimension === option && (
                        <motion.span layoutId="segment-pill" className="segment-pill" aria-hidden="true" />
                      )}
                      <span className="nav-label">By {option}</span>
                    </button>
                  ))}
                </div>
              </div>
              <div className="chart-stage" aria-hidden="true">
                <ErrorBoundary fallback={null}>
                  <Suspense fallback={<div className="chart-loading" />}>
                    <StatsChart3D key={dimension} data={chartData} theme={theme} />
                  </Suspense>
                </ErrorBoundary>
              </div>
            </div>
          )}

          <div className="stat-grid">
            <Breakdown title="By category" dimension="category" counts={snapshot.stats.by_category} />
            <Breakdown title="By priority" dimension="priority" counts={snapshot.stats.by_priority} />
          </div>
        </>
      )}
    </section>
  )
}
