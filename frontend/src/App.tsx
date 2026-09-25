import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Submit from './pages/Submit'
import './app.css'

type View = 'submit' | 'dashboard' | 'stats'

export default function App() {
  const [view, setView] = useState<View>('submit')
  return (
    <div className="shell">
      <header>
        <div>
          <p className="eyebrow">CivicPulse</p>
          <h1>Make your neighbourhood better</h1>
        </div>
        <nav aria-label="Main navigation">
          <button type="button" aria-current={view === 'submit' ? 'page' : undefined}
            onClick={() => setView('submit')}>Submit</button>
          <button type="button" aria-current={view === 'dashboard' ? 'page' : undefined}
            onClick={() => setView('dashboard')}>Dashboard</button>
          <button type="button" aria-current={view === 'stats' ? 'page' : undefined}
            onClick={() => setView('stats')}>Stats</button>
        </nav>
      </header>
      <main>
        {view === 'submit' && <Submit />}
        {view === 'dashboard' && <Dashboard />}
        {view === 'stats' && <section><h2>Stats</h2><p>Aggregate statistics will appear here.</p></section>}
      </main>
    </div>
  )
}
