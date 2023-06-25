import { defineConfig } from 'vite'
import { resolve } from 'node:path'
import { fileURLToPath, URL } from 'node:url'
import vue from '@vitejs/plugin-vue'

export default defineConfig(({ mode }) => {
  return {
    plugins: [vue()],
    root: resolve('./'),
    base: mode === 'production' ? '/static/dist/' : '/',
    appType: 'mpa',
    build: {
      target: 'esnext',
      outDir: resolve('./static/dist'),
      assetsDir: '',
      manifest: true,
      sourcemap: true,
      publicDir: false,
      emptyOutDir: true,
      rollupOptions: {
        input: {
          home: resolve(__dirname, 'src/pages/home/home.js'),
          login: resolve(__dirname, 'src/pages/login/login.js'),
          signup: resolve(__dirname, 'src/pages/register/register.js'),
          dashboard: resolve(__dirname, 'src/pages/dashboard/dashboard.js'),
        },
      },
    },
    server: {
      host: 'localhost',
      port: 5173,
      strictPort: true,
      open: false,
      origin: 'http://localhost:8000',
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})
