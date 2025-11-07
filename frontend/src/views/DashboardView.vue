<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-semibold">Dashboard</h1>
      <p class="text-gray-500">You are logged in as {{ userEmail }}</p>
    </div>
    <section class="grid gap-4 sm:grid-cols-2">
      <div class="card">
        <h2 class="text-lg font-medium">Environment</h2>
        <p class="text-sm text-gray-500">API base URL: {{ apiBaseUrl }}</p>
      </div>
      <div class="card">
        <h2 class="text-lg font-medium">Next steps</h2>
        <ul class="list-disc pl-5 text-sm text-gray-600">
          <li>Connect protected API calls using the shared Axios client.</li>
          <li>Extend Pinia stores for domain-specific state.</li>
          <li>Customize styles via <code>uno.config.ts</code>.</li>
        </ul>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const userEmail = computed(() => auth.user?.email ?? 'unknown user')
const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'
</script>
