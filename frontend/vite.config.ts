import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import Unocss from 'unocss/vite'
import { presetAttributify, presetIcons, presetUno } from 'unocss'

export default defineConfig({
  plugins: [
    vue(),
    Unocss({
      presets: [presetUno(), presetAttributify(), presetIcons()],
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
  },
  preview: {
    port: 4173,
  },
})


