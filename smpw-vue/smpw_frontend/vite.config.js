import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'), // 기존 기본값
      '@components': path.resolve(__dirname, 'src/components'), // 추가
      // 필요하다면 다른 폴더도 추가 가능
    }
  }
})
