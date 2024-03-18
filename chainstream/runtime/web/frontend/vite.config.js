import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    port: 3000,
    url: 'http://localhost:3000',
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:6677',    //实际请求地址
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, '')
          // rewrite: path => path.replace(['^' + import.meta.env.VITE_C], '')
        },
      }
    },
  // devServer: {
  //   proxy: {
  //     '/api': {
  //       target: 'http://localhost:6677',
  //       changeOrigin: true,
  //       rewrite: (path) => path.replace(/^\/api/, '')
  //     },
  //   }
  // }

})
