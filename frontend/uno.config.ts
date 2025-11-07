import { defineConfig, presetAttributify, presetIcons, presetUno } from 'unocss'

export default defineConfig({
  presets: [presetUno(), presetAttributify(), presetIcons()],
  shortcuts: {
    'btn-primary': 'px-4 py-2 rounded-lg bg-primary text-white font-semibold hover:bg-primary-dark disabled:opacity-50 disabled:cursor-not-allowed',
    card: 'rounded-xl border border-gray-200 shadow-sm bg-white p-6',
  },
  theme: {
    colors: {
      primary: '#2563eb',
      'primary-dark': '#1d4ed8',
    },
  },
})


