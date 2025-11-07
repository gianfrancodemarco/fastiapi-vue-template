import { VueQueryPlugin } from '@tanstack/vue-query'
import { createPinia } from 'pinia'
import { createApp } from 'vue'

import App from './App.vue'
import router from './router'

import '@unocss/reset/tailwind.css'
import 'uno.css'

const app = createApp(App)

app.use(createPinia())
app.use(VueQueryPlugin)
app.use(router)

app.mount('#app')


