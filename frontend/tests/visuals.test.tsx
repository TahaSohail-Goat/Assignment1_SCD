import { afterEach, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import App from '../src/App'
import Stats from '../src/pages/Stats'
import Submit from '../src/pages/Submit'
import { canRender3D } from '../src/components/three/capabilities'
import { onPulse } from '../src/components/three/pulse'

afterEach(() => {
  cleanup()
  delete document.documentElement.dataset.theme
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

function reply(status: number, body: unknown, headers: Record<string, string> = {}): Response {
  return { ok: status >= 200 && status < 300, status, headers: new Headers(headers), json: async () => body } as Response
}

function stubWebGL(reducedMotion: boolean, renderer = 'ANGLE (NVIDIA GeForce RTX 3060 Direct3D11)') {
  vi.stubGlobal('WebGLRenderingContext', function WebGLRenderingContext() {})
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockReturnValue({
    getExtension: (name: string) => (name === 'WEBGL_debug_renderer_info' ? { UNMASKED_RENDERER_WEBGL: 37446 } : null),
    getParameter: (parameter: number) => (parameter === 37446 ? renderer : null),
  } as unknown as RenderingContext)
  vi.stubGlobal('matchMedia', vi.fn((query: string) => ({
    matches: query.includes('reduced-motion') ? reducedMotion : false,
  })))
}

it('renders the static backdrop without a canvas when WebGL is unavailable, keeping the form usable', () => {
  vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: false })))
  render(<App />)
  const backdrop = document.querySelector('.backdrop')
  expect(backdrop?.getAttribute('aria-hidden')).toBe('true')
  expect(backdrop?.getAttribute('data-mode')).toBe('static')
  expect(document.querySelector('canvas')).toBeNull()
  const input = screen.getByLabelText('Complaint') as HTMLTextAreaElement
  fireEvent.change(input, { target: { value: 'Streetlight out on Canal Road' } })
  expect(input.value).toBe('Streetlight out on Canal Road')
})

it('enables 3D only when WebGL exists and reduced motion is not requested', () => {
  expect(canRender3D()).toBe(false)
  stubWebGL(false)
  expect(canRender3D()).toBe(true)
  vi.restoreAllMocks()
  stubWebGL(true)
  expect(canRender3D()).toBe(false)
})

it('keeps the static presentation on software WebGL renderers', () => {
  stubWebGL(false, 'ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero)), SwiftShader driver)')
  expect(canRender3D()).toBe(false)
  vi.restoreAllMocks()
  stubWebGL(false, 'llvmpipe (LLVM 15.0.7, 256 bits)')
  expect(canRender3D()).toBe(false)
})

it('never throws when the browser capability APIs throw', () => {
  vi.stubGlobal('WebGLRenderingContext', function WebGLRenderingContext() {})
  vi.spyOn(HTMLCanvasElement.prototype, 'getContext').mockImplementation(() => { throw new Error('blocked') })
  vi.stubGlobal('matchMedia', () => { throw new Error('blocked') })
  expect(canRender3D()).toBe(false)
})

it('sends a city pulse with the triaged priority after a successful submission', async () => {
  const pulses: string[] = []
  const stop = onPulse((priority) => pulses.push(priority))
  vi.stubGlobal('fetch', vi.fn(async () => reply(201, {
    id: '00000000-0000-4000-8000-000000000009', text: 'Burst water main flooding Street 12',
    location: 'Street 12', reporter_contact: null, category: 'water', priority: 'high', status: 'open',
    ai_summary: 'Burst water main', triaged_by: 'rules', triage_latency_ms: 2,
    created_at: '2026-09-29T12:00:00Z', updated_at: '2026-09-29T12:00:00Z',
  })))
  render(<Submit />)
  fireEvent.change(screen.getByLabelText('Complaint'), { target: { value: 'Burst water main flooding Street 12' } })
  fireEvent.change(screen.getByLabelText('Location'), { target: { value: 'Street 12' } })
  fireEvent.click(screen.getByRole('button', { name: 'Submit complaint' }))
  expect(await screen.findByText('Burst water main')).toBeTruthy()
  expect(pulses).toEqual(['high'])
  stop()
})

it('does not send a pulse when the submission fails', async () => {
  const pulses: string[] = []
  const stop = onPulse((priority) => pulses.push(priority))
  vi.stubGlobal('fetch', vi.fn(async () => reply(503, { error: { code: 'unavailable', message: 'Service unavailable' } })))
  render(<Submit />)
  fireEvent.change(screen.getByLabelText('Complaint'), { target: { value: 'Burst water main flooding Street 12' } })
  fireEvent.change(screen.getByLabelText('Location'), { target: { value: 'Street 12' } })
  fireEvent.click(screen.getByRole('button', { name: 'Submit complaint' }))
  expect(await screen.findByText('Service unavailable')).toBeTruthy()
  expect(pulses).toEqual([])
  stop()
})

it('shows accessible counts with one bar per group and no 3D chart without WebGL', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => reply(200, {
    total: 6, by_category: { water: 4, roads: 2 }, by_priority: { high: 1, normal: 3, low: 2 },
  }, { 'X-Cache': 'HIT' })))
  render(<Stats />)
  expect(await screen.findByText('roads')).toBeTruthy()
  expect(screen.getByText('6')).toBeTruthy()
  expect(document.querySelectorAll('.stat-bar')).toHaveLength(5)
  expect(screen.queryByRole('group', { name: 'Chart grouping' })).toBeNull()
  expect(document.querySelector('canvas')).toBeNull()
})

it('moves between views with the animated navigation and marks the current page', async () => {
  vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: false })))
  vi.stubGlobal('fetch', vi.fn(async () => reply(200, { total: 0, by_category: {}, by_priority: {} })))
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Stats' }))
  expect(await screen.findByRole('heading', { name: 'Community statistics' })).toBeTruthy()
  expect(screen.getByRole('button', { name: 'Stats' }).getAttribute('aria-current')).toBe('page')
  expect(screen.getByRole('button', { name: 'Submit' }).getAttribute('aria-current')).toBeNull()
})
