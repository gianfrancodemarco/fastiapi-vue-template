<template>
  <div class="card space-y-6">
    <div>
      <h1 class="text-2xl font-semibold">Welcome back</h1>
      <p class="text-sm text-gray-500">Sign in to continue to your dashboard.</p>
    </div>
    <form class="space-y-4" @submit.prevent="onSubmit">
      <label class="block">
        <span class="text-sm font-medium">Email</span>
        <input
          v-model="form.email"
          type="email"
          required
          autocomplete="email"
          class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none"
        />
      </label>
      <label class="block">
        <span class="text-sm font-medium">Password</span>
        <input
          v-model="form.password"
          type="password"
          required
          autocomplete="current-password"
          class="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-primary focus:outline-none"
        />
      </label>
      <p v-if="errorMessage" class="text-sm text-red-500">{{ errorMessage }}</p>
      <button class="btn-primary w-full" :disabled="isLoading">{{ isLoading ? 'Signing in...' : 'Sign in' }}</button>
    </form>
    <p class="text-center text-sm text-gray-500">
      Don't have an account?
      <RouterLink class="text-primary" to="/register">Sign up</RouterLink>
    </p>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'

import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const form = reactive({
  email: '',
  password: '',
})

const isLoading = computed(() => auth.status === 'loading')
const errorMessage = computed(() => auth.errors.message)

const onSubmit = async () => {
  try {
    await auth.login({ ...form })
    const redirect = (route.query.redirect as string) ?? '/dashboard'
    await router.replace(redirect)
  } catch (error) {
    console.error(error)
  }
}
</script>
