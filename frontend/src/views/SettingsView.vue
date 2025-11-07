<template>
  <div class="space-y-6">
    <div>
      <h1 class="text-3xl font-semibold">Account settings</h1>
      <p class="text-gray-500">Manage your profile information and security preferences.</p>
    </div>
    <div class="card space-y-4">
      <h2 class="text-lg font-medium">Profile</h2>
      <p>Email: {{ auth.user?.email }}</p>
      <p>Full name: {{ auth.user?.full_name ?? 'Not set' }}</p>
      <p>Status: <span class="font-medium">{{ auth.user?.is_active ? 'Active' : 'Disabled' }}</span></p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
</script>
