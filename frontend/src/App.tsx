import { useEffect, useState } from 'react'
import Dashboard from './pages/Dashboard'
import Stats from './pages/Stats'
import Submit from './pages/Submit'
import ErrorBoundary from './components/ErrorBoundary'
import './app.css'

type View = 'submit' | 'dashboard' | 'stats'
type Theme = 'light' | 'dark'
const themeKey = 'civicpulse-theme'

function initialTheme(): Theme {
  try {
    const saved = window.localStorage.getItem(themeKey)
    if (saved === 'light' || saved === 'dark') return saved
  } catch {
    // Storage may be disabled; the toggle still works for this visit.
  }
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export default function App() {
  const [view, setView] = useState<View>('submit')
  const [theme, setTheme] = useState<Theme>(initialTheme)
  useEffect(() => {
    document.documentElement.dataset.theme = theme
  }, [theme])

  function toggleTheme() {
    const next = theme === 'light' ? 'dark' : 'light'
    setTheme(next)
    try {
      window.localStorage.setItem(themeKey, next)
    } catch {
      // A browser storage restriction must not prevent changing the theme.
    }
  }

  const themeAction = `Switch to ${theme === 'light' ? 'dark' : 'light'} mode`
  return (
    <div className="shell">
      <header>
        <div>
          <p className="eyebrow">CivicPulse</p>
          <h1>Make your neighbourhood better</h1>
        </div>
        <div className="header-actions">
        <nav aria-label="Main navigation">
          <button type="button" aria-current={view === 'dashboard' ? 'page' : undefined}
            onClick={() => setView('dashboard')}>Dashboard</button>
          <button type="button" aria-current={view === 'submit' ? 'page' : undefined}
            onClick={() => setView('submit')}>Submit</button>
          <button type="button" aria-current={view === 'stats' ? 'page' : undefined}
            onClick={() => setView('stats')}>Stats</button>
        </nav>
        <button type="button" className="theme-toggle" onClick={toggleTheme}
          aria-label={themeAction} title={themeAction}>
          <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor"
            strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
            {theme === 'light' ? <path d="M20.9 13A9 9 0 0 1 11 3.1 9 9 0 1 0 20.9 13Z" /> : (
              <>
                <circle cx="12" cy="12" r="4" />
                <path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
              </>
            )}
          </svg>
        </button>
        </div>
      </header>
      <main><ErrorBoundary>
        {view === 'submit' && <Submit />}
        {view === 'dashboard' && <Dashboard />}
        {view === 'stats' && <Stats />}
      </ErrorBoundary></main>
    </div>
  )
}
