<template>
  <div class="min-h-screen bg-gray-50 text-gray-900">
    <header class="border-b border-gray-200 bg-white">
      <nav class="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <RouterLink to="/" class="text-lg font-semibold text-primary">FastAPI + Vue Template</RouterLink>
        <div class="flex items-center gap-4">
          <RouterLink to="/dashboard" class="hover:text-primary">Dashboard</RouterLink>
          <RouterLink to="/settings" class="hover:text-primary">Settings</RouterLink>
          <button v-if="isAuthenticated" class="hover:text-primary" @click="handleLogout">Logout</button>
          <RouterLink v-else to="/login" class="btn-primary">Login</RouterLink>
        </div>
      </nav>
    </header>
    <main class="mx-auto max-w-4xl px-6 py-10">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

const isAuthenticated = computed(() => auth.isAuthenticated)

const handleLogout = async () => {
  await auth.logout()
}
</script>
