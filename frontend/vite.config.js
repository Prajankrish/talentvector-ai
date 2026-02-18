import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // No proxy needed - frontend calls directly to http://localhost:8000
    // Backend CORS is already configured to accept all requests
  }
})
