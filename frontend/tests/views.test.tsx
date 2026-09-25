import { afterEach, expect, it, vi } from 'vitest'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { type ReactNode } from 'react'
import Submit from '../src/pages/Submit'
import Dashboard from '../src/pages/Dashboard'
import Stats from '../src/pages/Stats'
import ErrorBoundary from '../src/components/ErrorBoundary'

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
  vi.restoreAllMocks()
})

function reply(status: number, body: unknown, headers: Record<string, string> = {}): Response {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: new Headers(headers),
    json: async () => body,
  } as Response
}

const complaint = {
  id: '00000000-0000-4000-8000-000000000001',
  text: 'The street light has been out for days.',
  location: 'Ward 2',
  reporter_contact: null,
  category: 'streetlights',
  priority: 'high',
  status: 'open',
  ai_summary: 'Street light outage',
  triaged_by: 'rules:fallback',
  triage_latency_ms: 12,
  created_at: '2026-09-25T12:00:00Z',
  updated_at: '2026-09-25T12:00:00Z',
}

function fillSubmit(text = 'The street light is broken.', location = 'Ward 2') {
  fireEvent.change(screen.getByLabelText('Complaint'), { target: { value: text } })
  fireEvent.change(screen.getByLabelText('Location'), { target: { value: location } })
}

it('refuses short text and location before sending a request', () => {
  const fetchMock = vi.fn()
  vi.stubGlobal('fetch', fetchMock)
  render(<Submit />)
  fillSubmit('123456789', 'AB')
  fireEvent.click(screen.getByRole('button', { name: 'Submit complaint' }))
  expect(screen.getByText('Complaint must be 10–2000 characters.')).toBeTruthy()
  expect(screen.getByText('Location must be 3–200 characters.')).toBeTruthy()
  expect(fetchMock).not.toHaveBeenCalled()
})

it('shows honest loading until the response and renders the server triage values', async () => {
  let finish!: (response: Response) => void
  const pending = new Promise<Response>((resolve) => { finish = resolve })
  vi.stubGlobal('fetch', vi.fn(() => pending))
  render(<Submit />)
  fillSubmit()
  fireEvent.click(screen.getByRole('button', { name: 'Submit complaint' }))
  expect(screen.getByRole('status').textContent).toContain('classifying')
  expect(screen.queryByText('Street light outage')).toBeNull()
  finish(reply(201, complaint))
  expect(await screen.findByText('Street light outage')).toBeTruthy()
  expect(screen.getByText('rules:fallback')).toBeTruthy()
  expect(screen.queryByRole('status')).toBeNull()
})

it('renders server field-level 400 validation after client validation accepted', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => reply(400, {
    error: { code: 'validation_error', message: 'Invalid request',
      details: [{ field: 'location', message: 'Location is outside the service area' }] },
  })))
  render(<Submit />)
  fillSubmit()
  fireEvent.click(screen.getByRole('button', { name: 'Submit complaint' }))
  expect(await screen.findByText('Location is outside the service area')).toBeTruthy()
})

it('shows the server Retry-After seconds when complaint submission is rate limited', async () => {
  vi.stubGlobal('fetch', vi.fn(async () => reply(429, {
    error: { code: 'rate_limited', message: 'Too many complaint submissions' },
  }, { 'Retry-After': '37' })))
  render(<Submit />)
  fillSubmit()
  fireEvent.click(screen.getByRole('button', { name: 'Submit complaint' }))
  expect(await screen.findByText('Too many complaint submissions Retry after 37 seconds.')).toBeTruthy()
})

it('shows a 409 message verbatim and leaves the previous status visible', async () => {
  const fetchMock = vi.fn()
    .mockResolvedValueOnce(reply(200, { items: [complaint], total: 1, page: 1, page_size: 20 }))
    .mockResolvedValueOnce(reply(409, {
      error: { code: 'invalid_transition', message: 'Cannot move open to resolved' },
    }))
  vi.stubGlobal('fetch', fetchMock)
  render(<Dashboard />)
  const status = await screen.findByLabelText(`Status for complaint ${complaint.id}`)
  fireEvent.change(status, { target: { value: 'resolved' } })
  expect(await screen.findByText('Cannot move open to resolved')).toBeTruthy()
  expect((status as HTMLSelectElement).value).toBe('open')
  expect(fetchMock).toHaveBeenCalledTimes(2)
})

it('combines dashboard filters and moves to the next page', async () => {
  const fetchMock = vi.fn(async () => reply(200, {
    items: [complaint], total: 21, page: 1, page_size: 20,
  }))
  vi.stubGlobal('fetch', fetchMock)
  render(<Dashboard />)
  await screen.findByText('The street light has been out for days.')
  fireEvent.change(screen.getByLabelText('Category'), { target: { value: 'streetlights' } })
  fireEvent.change(screen.getByLabelText('Priority'), { target: { value: 'high' } })
  fireEvent.change(screen.getByLabelText('Status'), { target: { value: 'open' } })
  await waitFor(() => {
    const path = String(fetchMock.mock.lastCall?.[0])
    expect(path).toContain('category=streetlights')
    expect(path).toContain('priority=high')
    expect(path).toContain('status=open')
  })
  fireEvent.click(screen.getByRole('button', { name: 'Next' }))
  await waitFor(() => expect(String(fetchMock.mock.lastCall?.[0])).toContain('page=2'))
})

it('ignores an older list response after the operator changes a filter', async () => {
  let finishInitial!: (response: Response) => void
  let finishFiltered!: (response: Response) => void
  const initial = new Promise<Response>((resolve) => { finishInitial = resolve })
  const filtered = new Promise<Response>((resolve) => { finishFiltered = resolve })
  const fetchMock = vi.fn().mockReturnValueOnce(initial).mockReturnValueOnce(filtered)
  vi.stubGlobal('fetch', fetchMock)
  render(<Dashboard />)
  fireEvent.change(screen.getByLabelText('Category'), { target: { value: 'water' } })
  await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2))
  await act(async () => {
    finishFiltered(reply(200, { items: [{ ...complaint, text: 'Filtered water complaint' }],
      total: 1, page: 1, page_size: 20 }))
  })
  expect(screen.getByText('Filtered water complaint')).toBeTruthy()
  await act(async () => {
    finishInitial(reply(200, { items: [complaint], total: 1, page: 1, page_size: 20 }))
  })
  expect(screen.getByText('Filtered water complaint')).toBeTruthy()
  expect(screen.queryByText(complaint.text)).toBeNull()
})

it.each(['HIT', 'MISS', null] as const)('shows the X-Cache state %s from the response', async (cache) => {
  vi.stubGlobal('fetch', vi.fn(async () => reply(200, {
    total: 5, by_category: { water: 3, roads: 2 }, by_priority: { high: 1, normal: 4 },
  }, cache ? { 'X-Cache': cache } : {})))
  render(<Stats />)
  expect(await screen.findByText('water')).toBeTruthy()
  expect(screen.getByText('3')).toBeTruthy()
  expect(screen.getByText(cache ?? 'Unknown')).toBeTruthy()
})

it('error boundary catches a render error and shows a fallback', () => {
  function Broken(): ReactNode {
    throw new Error('render failed')
  }
  const quietExpectedError = (event: ErrorEvent) => event.preventDefault()
  window.addEventListener('error', quietExpectedError)
  vi.spyOn(console, 'error').mockImplementation(() => undefined)
  try {
    render(<ErrorBoundary><Broken /></ErrorBoundary>)
    expect(screen.getByRole('alert').textContent).toContain('Something went wrong')
  } finally {
    window.removeEventListener('error', quietExpectedError)
  }
})
