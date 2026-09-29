import { useEffect, useState } from 'react'
import { motion, MotionConfig } from 'motion/react'
import Dashboard from './pages/Dashboard'
import Stats from './pages/Stats'
import Submit from './pages/Submit'
import ErrorBoundary from './components/ErrorBoundary'
import CityBackdrop from './components/three/CityBackdrop'
import { prefersReducedMotion } from './components/three/capabilities'
import { ThemeContext, type Theme } from './theme'
import './app.css'

type View = 'submit' | 'dashboard' | 'stats'
const themeKey = 'civicpulse-theme'
const views: { id: View; label: string }[] = [
  { id: 'dashboard', label: 'Dashboard' },
  { id: 'submit', label: 'Submit' },
  { id: 'stats', label: 'Stats' },
]

function initialTheme(): Theme {
  try {
    const saved = window.localStorage.getItem(themeKey)
    if (saved === 'light' || saved === 'dark') return saved
  } catch {
    // Storage may be disabled; the toggle still works for this visit.
  }
  return window.matchMedia?.('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

function PulseMark() {
  return (
    <svg className="brand-mark" viewBox="0 0 40 40" width="40" height="40" aria-hidden="true" focusable="false">
      <circle cx="20" cy="20" r="18" className="brand-ring" />
      <motion.path d="M5 21h8l3-8 5 15 4-11 2 4h8" fill="none" strokeWidth="2.6"
        strokeLinecap="round" strokeLinejoin="round" className="brand-line"
        initial={{ pathLength: 0 }} animate={{ pathLength: 1 }}
        transition={{ duration: 1.4, ease: 'easeInOut', repeat: Infinity, repeatDelay: 2.2 }} />
    </svg>
  )
}

export default function App() {
  const [view, setView] = useState<View>('submit')
  const [theme, setTheme] = useState<Theme>(initialTheme)
  // Motion is told the preference explicitly, so it never needs its own media-query listener.
  const [reduced] = useState(prefersReducedMotion)
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
    <ThemeContext.Provider value={theme}>
      <MotionConfig reducedMotion={reduced ? 'always' : 'never'}>
        <CityBackdrop theme={theme} />
        <div className="shell">
          <motion.header initial={{ opacity: 0, y: -18 }} animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}>
            <div className="brand">
              <PulseMark />
              <div>
                <p className="eyebrow">CivicPulse</p>
                <h1>Make your neighbourhood better</h1>
                <p className="tagline">Report an issue in your own words. AI triage routes it to the right team.</p>
              </div>
            </div>
            <div className="header-actions">
              <nav aria-label="Main navigation" className="main-nav">
                {views.map((item) => (
                  <button key={item.id} type="button" aria-current={view === item.id ? 'page' : undefined}
                    onClick={() => setView(item.id)}>
                    {view === item.id && (
                      <motion.span layoutId="nav-pill" className="nav-pill" aria-hidden="true"
                        transition={{ type: 'spring', stiffness: 420, damping: 34 }} />
                    )}
                    <span className="nav-label">{item.label}</span>
                  </button>
                ))}
              </nav>
              <motion.button type="button" className="theme-toggle" onClick={toggleTheme}
                aria-label={themeAction} title={themeAction}
                whileHover={{ scale: 1.08 }} whileTap={{ scale: 0.92 }}>
                <motion.svg key={theme} viewBox="0 0 24 24" width="22" height="22" fill="none"
                  stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"
                  aria-hidden="true" focusable="false"
                  initial={{ rotate: -90, scale: 0.4, opacity: 0 }} animate={{ rotate: 0, scale: 1, opacity: 1 }}
                  transition={{ type: 'spring', stiffness: 300, damping: 18 }}>
                  {theme === 'light' ? <path d="M20.9 13A9 9 0 0 1 11 3.1 9 9 0 1 0 20.9 13Z" /> : (
                    <>
                      <circle cx="12" cy="12" r="4" />
                      <path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.9 4.9l1.4 1.4m11.4 11.4 1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
                    </>
                  )}
                </motion.svg>
              </motion.button>
            </div>
          </motion.header>
          <main>
            <ErrorBoundary>
              <motion.div key={view} className="view"
                initial={{ opacity: 0, y: 22, scale: 0.985 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                transition={{ duration: 0.5, ease: [0.16, 1, 0.3, 1] }}>
                {view === 'submit' && <Submit />}
                {view === 'dashboard' && <Dashboard />}
                {view === 'stats' && <Stats />}
              </motion.div>
            </ErrorBoundary>
          </main>
          <footer className="site-footer">CivicPulse · AI-assisted civic triage with a rules fallback</footer>
        </div>
      </MotionConfig>
    </ThemeContext.Provider>
  )
}
