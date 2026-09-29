import { lazy, Suspense, useState } from 'react'
import type { Theme } from '../../theme'
import ErrorBoundary from '../ErrorBoundary'
import { canRender3D } from './capabilities'

const CityScene = lazy(() => import('./CityScene'))

/**
 * Decorative animated city behind the app. It is hidden from assistive technology, never
 * receives pointer events, and falls back to a CSS gradient without WebGL or with reduced motion.
 */
export default function CityBackdrop({ theme }: { theme: Theme }) {
  const [enabled] = useState(canRender3D)
  return (
    <div className="backdrop" aria-hidden="true" data-mode={enabled ? '3d' : 'static'}>
      <div className="backdrop-glow" />
      {enabled && (
        <ErrorBoundary fallback={null}>
          <Suspense fallback={null}>
            <CityScene theme={theme} />
          </Suspense>
        </ErrorBoundary>
      )}
      <div className="backdrop-fade" />
    </div>
  )
}
