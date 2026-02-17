import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // Разрешает доступ по IP (важно для Docker)
    port: 5173,
    watch: {
      usePolling: true // Обязательно для Windows, чтобы видеть изменения файлов
    },
    proxy: {
      '/api': {
        target: 'http://backend:8000', // Имя сервиса бэкенда в docker-compose
        changeOrigin: true
      }
    }
  }
})