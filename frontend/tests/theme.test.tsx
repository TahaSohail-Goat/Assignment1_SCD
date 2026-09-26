import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import App from '../src/App'

beforeEach(() => {
  const saved = new Map<string, string>()
  vi.stubGlobal('localStorage', {
    getItem: vi.fn((key: string) => saved.get(key) ?? null),
    setItem: vi.fn((key: string, value: string) => { saved.set(key, value) }),
  })
  vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: false })))
})

afterEach(() => {
  cleanup()
  delete document.documentElement.dataset.theme
  vi.unstubAllGlobals()
})

it('switches both ways with an icon-only accessible control, preserving form input', () => {
  render(<App />)
  const input = screen.getByLabelText('Complaint') as HTMLTextAreaElement
  fireEvent.change(input, { target: { value: 'Water is leaking outside the library.' } })
  const toggle = screen.getByRole('button', { name: 'Switch to dark mode' })
  expect(toggle.textContent).toBe('')
  expect(toggle.querySelector('svg')?.getAttribute('aria-hidden')).toBe('true')
  fireEvent.click(toggle)
  expect(document.documentElement.dataset.theme).toBe('dark')
  expect(localStorage.getItem('civicpulse-theme')).toBe('dark')
  expect(input.value).toBe('Water is leaking outside the library.')
  fireEvent.click(screen.getByRole('button', { name: 'Switch to light mode' }))
  expect(document.documentElement.dataset.theme).toBe('light')
  expect(localStorage.getItem('civicpulse-theme')).toBe('light')
})

it('uses the system theme initially without saving an implicit preference', () => {
  vi.stubGlobal('matchMedia', vi.fn(() => ({ matches: true })))
  render(<App />)
  expect(document.documentElement.dataset.theme).toBe('dark')
  expect(localStorage.setItem).not.toHaveBeenCalled()
})

it('restores the explicit preference on remount even when the system differs', () => {
  const first = render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Switch to dark mode' }))
  first.unmount()
  render(<App />)
  expect(document.documentElement.dataset.theme).toBe('dark')
})

it('ignores an invalid stored preference', () => {
  localStorage.setItem('civicpulse-theme', 'invalid')
  render(<App />)
  expect(document.documentElement.dataset.theme).toBe('light')
})

it('still switches when browser storage is unavailable', () => {
  vi.stubGlobal('localStorage', {
    getItem: () => { throw new Error('Storage blocked') },
    setItem: () => { throw new Error('Storage blocked') },
  })
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Switch to dark mode' }))
  expect(document.documentElement.dataset.theme).toBe('dark')
})
