import { useCallback, useEffect, useRef, useState } from 'react'
import { motion } from 'motion/react'
import {
  ApiError, listComplaints, updateStatus,
  type Category, type ComplaintPage, type Priority, type Status,
} from '../api/client'

const categories: Category[] = ['water', 'electricity', 'sanitation', 'roads', 'streetlights', 'other']
const priorities: Priority[] = ['high', 'normal', 'low']
const statuses: Status[] = ['open', 'in_progress', 'resolved', 'rejected']
const pageSize = 20

export default function Dashboard() {
  const [category, setCategory] = useState<Category | ''>('')
  const [priority, setPriority] = useState<Priority | ''>('')
  const [status, setStatus] = useState<Status | ''>('')
  const [page, setPage] = useState(1)
  const [result, setResult] = useState<ComplaintPage | null>(null)
  const [loading, setLoading] = useState(true)
  const [failure, setFailure] = useState('')
  const [rowError, setRowError] = useState<Record<string, string>>({})
  const [updating, setUpdating] = useState<string | null>(null)
  const requestVersion = useRef(0)
  const requestController = useRef<AbortController | null>(null)

  const load = useCallback(async () => {
    requestController.current?.abort()
    const controller = new AbortController()
    requestController.current = controller
    const version = ++requestVersion.current
    setLoading(true)
    setFailure('')
    setResult(null)
    try {
      const nextResult = await listComplaints({
        page,
        page_size: pageSize,
        category: category || undefined,
        priority: priority || undefined,
        status: status || undefined,
      }, controller.signal)
      if (version === requestVersion.current) {
        const lastPage = Math.max(1, Math.ceil(nextResult.total / pageSize))
        if (page > lastPage) {
          setPage(lastPage)
        } else {
          setResult(nextResult)
        }
      }
    } catch (error) {
      if (!controller.signal.aborted && version === requestVersion.current)
        setFailure(error instanceof Error ? error.message : 'Could not load complaints.')
    } finally {
      if (version === requestVersion.current) setLoading(false)
    }
  }, [category, priority, status, page])

  useEffect(() => {
    void load()
    return () => {
      requestController.current?.abort()
      requestVersion.current += 1
    }
  }, [load])

  async function changeStatus(id: string, next: Status) {
    setUpdating(id)
    setRowError((current) => ({ ...current, [id]: '' }))
    try {
      await updateStatus(id, next)
      await load() // use the server's current row; never infer a transition locally
    } catch (error) {
      setRowError((current) => ({
        ...current,
        [id]: error instanceof ApiError ? error.message : 'Could not change status.',
      }))
    } finally {
      setUpdating(null)
    }
  }

  const totalPages = Math.max(1, Math.ceil((result?.total ?? 0) / pageSize))

  return (
    <section aria-labelledby="dashboard-heading" className="panel">
      <div className="panel-head">
        <h2 id="dashboard-heading">Operations dashboard</h2>
        {result && <p className="summary">{result.total} complaints · Page {page} of {totalPages}</p>}
      </div>
      <div className="filters">
        <label>Category
          <select value={category} onChange={(event) => { setCategory(event.target.value as Category | ''); setPage(1) }}>
            <option value="">All categories</option>
            {categories.map((item) => <option key={item} value={item}>{item}</option>)}
          </select>
        </label>
        <label>Priority
          <select value={priority} onChange={(event) => { setPriority(event.target.value as Priority | ''); setPage(1) }}>
            <option value="">All priorities</option>
            {priorities.map((item) => <option key={item} value={item}>{item}</option>)}
          </select>
        </label>
        <label>Status
          <select value={status} onChange={(event) => { setStatus(event.target.value as Status | ''); setPage(1) }}>
            <option value="">All statuses</option>
            {statuses.map((item) => <option key={item} value={item}>{item.replace('_', ' ')}</option>)}
          </select>
        </label>
      </div>
      {loading && (
        <div className="loading-block">
          <p role="status" className="muted">Loading complaints…</p>
          <div className="skeleton-list" aria-hidden="true">
            {[0, 1, 2].map((index) => <div key={index} className="skeleton-card"><span /><span /><span /></div>)}
          </div>
        </div>
      )}
      {failure && (
        <div className="banner-error">
          <p role="alert">{failure}</p>
          <button type="button" onClick={() => void load()}>Retry loading complaints</button>
        </div>
      )}
      {result && (
        <>
          {result.items.length === 0 ? <p className="empty">No complaints match these filters.</p> : (
            <div className="complaint-list">
              {result.items.map((item, index) => (
                <motion.article key={item.id} className={`complaint priority-${item.priority}`}
                  initial={{ opacity: 0, y: 18 }} animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: Math.min(index, 10) * 0.045, duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
                  whileHover={{ y: -3 }}>
                  <div className="complaint-top">
                    <h3>
                      <span className={`badge cat-${item.category}`}>{item.category}</span>
                      <span className={`badge prio-${item.priority}`}>{item.priority}</span>
                    </h3>
                    <span className="chip" title="Triage provider">{item.triaged_by}</span>
                  </div>
                  <p className="complaint-text">{item.text}</p>
                  <p className="meta">{item.location} · {new Date(item.created_at).toLocaleString()}</p>
                  <label className={`status-control status-${item.status}`}>Status
                    <select aria-label={`Status for complaint at ${item.location}: ${item.text}`}
                      value={item.status} disabled={updating === item.id}
                      onChange={(event) => void changeStatus(item.id, event.target.value as Status)}>
                      {statuses.map((choice) => (
                        <option key={choice} value={choice}>{choice.replace('_', ' ')}</option>
                      ))}
                    </select>
                  </label>
                  {rowError[item.id] && (
                    <motion.p role="alert" className="field-error" initial={{ opacity: 0, x: -6 }}
                      animate={{ opacity: 1, x: [0, -5, 5, -2, 0] }} transition={{ duration: 0.35 }}>
                      {rowError[item.id]}
                    </motion.p>
                  )}
                </motion.article>
              ))}
            </div>
          )}
          <nav aria-label="Complaint pages" className="pagination">
            <motion.button type="button" disabled={page <= 1} onClick={() => setPage(page - 1)}
              whileTap={{ scale: 0.95 }}>Previous</motion.button>
            <span className="page-dots" aria-hidden="true">{page} / {totalPages}</span>
            <motion.button type="button" disabled={page >= totalPages} onClick={() => setPage(page + 1)}
              whileTap={{ scale: 0.95 }}>Next</motion.button>
          </nav>
        </>
      )}
    </section>
  )
}
