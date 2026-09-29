import { createContext } from 'react'
import type { Category, Priority } from './api/client'

export type Theme = 'light' | 'dark'

/** Current colour theme, shared with the decorative 3D scenes. */
export const ThemeContext = createContext<Theme>('light')

/** Colours used by badges, bars and 3D charts. Mirrors the CSS tokens in app.css. */
export const categoryColor: Record<Category, string> = {
  water: '#3b9cf0',
  electricity: '#f2b632',
  sanitation: '#5fbf73',
  roads: '#a47cf0',
  streetlights: '#ff8f4d',
  other: '#8fa3b8',
}

export const priorityColor: Record<Priority, string> = {
  high: '#ef4f5f',
  normal: '#f2b632',
  low: '#3fb3d9',
}

export const scenePalette = {
  light: {
    fog: '#e3eeec', ground: '#d3e3df', grid: '#a9c7c0', building: '#f4f9f8', buildingTop: '#8fd0c4',
    glow: '#0fa192', sky: '#ffffff', ambient: 0.75, sun: 1.25, sparkle: '#0fa192',
  },
  dark: {
    fog: '#08131a', ground: '#0b1a22', grid: '#1b3a45', building: '#15303c', buildingTop: '#23596a',
    glow: '#5ee6d3', sky: '#6fb6ff', ambient: 0.4, sun: 0.7, sparkle: '#9df5e8',
  },
} as const
