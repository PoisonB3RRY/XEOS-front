import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'rewrite-to-ops',
      configureServer(server) {
        server.middlewares.use((req, res, next) => {
          if (req.url === '/' || req.url === '/index.html' || req.url === '/PCMP/home/index') {
            req.url = '/ops.html'
          }
          next()
        })
      }
    }
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    port: 3001,
    open: true
  },
  build: {
    outDir: 'dist-ops',
    rollupOptions: {
      input: path.resolve(__dirname, 'ops.html')
    }
  }
})
