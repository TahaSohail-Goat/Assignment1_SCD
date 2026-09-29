import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  build: {
    // three.js and React Three Fiber form one large chunk that is only fetched through the lazy
    // CityScene/StatsChart3D imports (rich mode); the initial bundle stays small.
    chunkSizeWarningLimit: 1000,
  },
  server: {
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
    },
  },
})
