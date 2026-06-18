import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 5173,
    host: '127.0.0.1',
    watch: {
      awaitWriteFinish: {
        stabilityThreshold: 800,
        pollInterval: 100
      }
    }
  }
})
