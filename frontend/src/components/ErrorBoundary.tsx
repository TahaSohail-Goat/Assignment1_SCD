import { Component, type ErrorInfo, type ReactNode } from 'react'

/** `fallback` replaces the default alert, e.g. `null` for purely decorative content. */
type Props = { children: ReactNode; fallback?: ReactNode }
type State = { failed: boolean }

export default class ErrorBoundary extends Component<Props, State> {
  state: State = { failed: false }

  static getDerivedStateFromError(): State {
    return { failed: true }
  }

  componentDidCatch(error: Error, info: ErrorInfo): void {
    // Keep diagnostics local to the browser; never include citizen complaint content.
    console.error('CivicPulse view failed to render', error.name, info.componentStack)
  }

  render(): ReactNode {
    if (this.state.failed) {
      if (this.props.fallback !== undefined) return this.props.fallback
      return (
        <section role="alert">
          <h2>Something went wrong</h2>
          <p>Please reload the page to try again.</p>
        </section>
      )
    }
    return this.props.children
  }
}
